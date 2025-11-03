# Parallel SubAgents Workflow Rules

**Purpose**: Define rules for coordinating multiple Claude Code SubAgents in parallel execution
**Applies To**: All SubAgent orchestration and parallel task execution
**Version**: 1.0
**Created**: 2025-10-27

---

## Core Principles

1. **Single Message = Parallel Execution**: Multiple agents in ONE message run in parallel
2. **Different Agent Types Only**: Cannot run same agent type on multiple tasks simultaneously
3. **Independent Tasks Only**: Parallelize tasks with no dependencies
4. **Clear Boundaries**: Each agent needs isolated, well-defined scope
5. **Optimal Count**: 3-5 agents in parallel is the sweet spot

---

## Rule 1: Single Message, Multiple Task Calls

### Requirement
To run agents in parallel, MUST send **single message** with **multiple Task tool calls**.

### ❌ Wrong (Sequential Execution)
```
Message 1: "Use backend-developer to implement Task A"
[Wait for completion]
Message 2: "Use frontend-developer to implement Task B"
```
**Result**: Agents run one after another (slow)

### ✅ Correct (Parallel Execution)
```
Message 1: "Run these in parallel:
- Use backend-developer to implement Task A
- Use frontend-developer to implement Task B"
```
**Result**: Both agents start simultaneously (fast)

### Rationale
Claude Code's Task tool launches agents in parallel when multiple Task calls are made in a single message. Sequential messages queue agents one at a time.

---

## Rule 2: Different Agent Types Only

### Requirement
Cannot run the SAME agent type on multiple tasks simultaneously. Each parallel track must use a DIFFERENT agent.

### ❌ Wrong
```
Parallel execution:
- backend-developer: Implement Task A
- backend-developer: Implement Task B  ← Same agent type!
```

### ✅ Correct
```
Parallel execution:
- backend-developer: Implement Task A
- full-stack-developer: Implement Task B  ← Different agent type
```

### Rationale
Each agent TYPE can only have one active instance. To parallelize backend work, use backend-developer for one task and full-stack-developer (which can also do backend) for another.

### Agent Substitutions
When you need multiple similar agents:
- **Backend work**: backend-developer, full-stack-developer, api-designer
- **Frontend work**: frontend-developer, full-stack-developer
- **Database work**: database-expert, full-stack-developer, backend-developer
- **Documentation**: technical-writer, api-designer

---

## Rule 3: Independent Tasks Only

### Requirement
Only parallelize tasks that have NO dependencies on each other.

### ❌ Wrong (Dependent Tasks)
```
Parallel execution:
- database-expert: Create user schema
- backend-developer: Implement endpoints using that schema  ← Depends on schema!
```
**Problem**: Backend developer starts before schema exists

### ✅ Correct (Independent Tasks)
```
Parallel execution:
- database-expert: Create user schema
- frontend-developer: Build login UI mockup  ← Independent!
```

### ✅ Also Correct (Sequential Then Parallel)
```
Phase 1 (Sequential):
- database-expert: Create user schema

Phase 2 (Parallel, after Phase 1):
- backend-developer: Implement endpoints
- frontend-developer: Build login UI
```

### Dependency Analysis Checklist
Before parallelizing, ask:
- ✓ Does Task B need output/artifacts from Task A?
- ✓ Do tasks modify the same files?
- ✓ Do tasks require each other's completion?

If YES to any → Run sequentially, not in parallel

---

## Rule 4: Clear Task Boundaries

### Requirement
Each agent must have an isolated, well-defined task with clear scope and deliverables.

### ❌ Wrong (Vague Boundaries)
```
- backend-developer: "Work on authentication"
- frontend-developer: "Also work on authentication"
```
**Problem**: Overlapping responsibilities, potential conflicts

### ✅ Correct (Clear Boundaries)
```
- backend-developer: "Implement POST /auth/login and POST /auth/register endpoints with JWT token generation"
- frontend-developer: "Build LoginForm and RegisterForm React components that call auth endpoints"
```

### Boundary Definition Checklist
Each task should specify:
- ✓ Exact deliverables (files to create/modify)
- ✓ Input requirements (what agent needs to start)
- ✓ Output artifacts (what agent produces)
- ✓ Success criteria (how to know it's done)
- ✓ File scope (which files agent will touch)

---

## Rule 5: Optimal Agent Count (3-5)

### Requirement
Run 3-5 agents in parallel for optimal performance. Avoid exceeding 5.

### ❌ Too Few (Underutilized)
```
Parallel execution:
- backend-developer: 5-day task
```
**Problem**: Not leveraging parallelism, wasting time

### ❌ Too Many (Overwhelming)
```
Parallel execution with 10 agents:
- backend-developer, frontend-developer, database-expert,
  test-runner, code-reviewer, security-auditor, devops-engineer,
  docker-specialist, technical-writer, api-designer
```
**Problem**: Hard to monitor, coordinate, and integrate

### ✅ Optimal (3-5 Agents)
```
Parallel execution:
- backend-developer: Backend APIs
- frontend-developer: UI components
- database-expert: Schema + migrations
- technical-writer: API documentation
```
**Sweet Spot**: Significant parallelism, manageable coordination

### Scaling Guidelines
- **Simple tasks (1-2 days)**: 2-3 agents
- **Medium tasks (3-5 days)**: 3-4 agents
- **Complex tasks (1-2 weeks)**: 4-5 agents
- **Very complex (2+ weeks)**: Multiple phases of 3-5 agents each

---

## Rule 6: Explicit Parallelism Language

### Requirement
Use explicit language to trigger parallel execution.

### Trigger Phrases
- "Run in parallel"
- "Execute simultaneously"
- "At the same time"
- "Use multiple agents"
- "Parallel tracks"

### Example Requests
✅ "Run these three agents IN PARALLEL: backend-developer on Task A, frontend-developer on Task B, database-expert on Task C"

✅ "Execute SIMULTANEOUSLY: code review, security audit, and test suite"

✅ "Work on Tasks 044-1, 044-4, and 044-7 AT THE SAME TIME"

---

## Rule 7: Progress Reporting

### Requirement
Agents must report back independently. Orchestrator tracks aggregate progress.

### Reporting Frequency
- **Fast tasks (<1 day)**: Hourly updates
- **Medium tasks (1-3 days)**: Every 4-6 hours
- **Long tasks (3+ days)**: Daily updates

### Report Format
```markdown
## Agent Status: [agent-name]

**Task**: [Description]
**Status**: [Pending/In Progress/Completed/Blocked]
**Progress**: [X%]
**ETA**: [Estimate]

**Completed**:
- [Item 1]
- [Item 2]

**In Progress**:
- [Current work]

**Blockers**:
- [Any blocking issues]
```

---

## Rule 8: Error Isolation

### Requirement
One agent's failure should NOT block other parallel agents.

### ❌ Wrong (Blocking Failure)
```
Track A fails → Abort all tracks
```

### ✅ Correct (Isolated Failure)
```
Track A fails → Continue Track B and C
               → Report Track A failure
               → Suggest recovery for Track A
               → User decides next steps
```

### Error Handling Protocol
1. Detect agent failure
2. Continue other parallel agents
3. Report failure immediately
4. Suggest recovery options:
   - Retry with same agent
   - Reassign to different agent
   - Mark as blocked, continue others
5. User chooses resolution

---

## Rule 9: Resource Conflict Detection

### Requirement
Check for file/resource conflicts BEFORE parallel execution.

### File Conflict Detection
```python
# Pseudo-code for conflict detection
task_a_files = ["src/auth.ts", "src/users.ts"]
task_b_files = ["src/users.ts", "src/profile.ts"]

conflict = set(task_a_files) & set(task_b_files)  # {"src/users.ts"}

if conflict:
    # Cannot parallelize - same file modified
    suggest_sequential_execution()
else:
    # Safe to parallelize
    execute_parallel()
```

### Common Conflicts
- **File modifications**: Two agents editing same file
- **Database migrations**: Two agents creating migrations
- **Environment changes**: Two agents modifying .env
- **Shared dependencies**: Two agents updating package.json

### Conflict Resolution
1. **Detect** potential conflicts during planning
2. **Warn** user of conflicts
3. **Suggest** sequential execution or task splitting
4. **Avoid** parallel execution on conflicting resources

---

## Rule 10: Synchronization Points

### Requirement
Define WHERE parallel tracks must sync up and converge.

### Synchronization Patterns

#### Pattern 1: Fan-Out, Fan-In
```
Phase 1 (Sequential):
  - solution-architect: Design architecture

Phase 2 (Parallel - Fan Out):
  ├─ backend-developer: Implement backend
  ├─ frontend-developer: Implement frontend
  └─ database-expert: Implement database

Phase 3 (Sync Point - Fan In):
  - Wait for ALL Phase 2 agents to complete

Phase 4 (Sequential):
  - test-runner: Integration testing
```

#### Pattern 2: Staged Parallelism
```
Stage 1 (Parallel):
  ├─ database-expert: Schema
  └─ solution-architect: API design

[SYNC POINT 1: Wait for both]

Stage 2 (Parallel):
  ├─ backend-developer: API implementation
  ├─ frontend-developer: UI components
  └─ technical-writer: Documentation

[SYNC POINT 2: Wait for all three]

Stage 3 (Sequential):
  - test-runner: Full test suite
```

#### Pattern 3: Rolling Completion
```
Parallel (Independent):
  ├─ Task A: 2 days
  ├─ Task B: 4 days
  └─ Task C: 6 days

No sync points - each reports as complete independently
User can start using results from A and B while C continues
```

### Sync Point Definition
Each sync point should specify:
- ✓ Which agents must complete
- ✓ What happens at sync (validation, integration, etc.)
- ✓ Next steps after sync
- ✓ Blocking vs non-blocking (can work continue elsewhere?)

---

## Exception Cases

### Case 1: Emergency Fixes
**Scenario**: Production down, need immediate fix

**Rule Exception**: May exceed 5 parallel agents for distributed investigation
```
Emergency parallel investigation (6 agents):
- debugger: Log analysis
- backend-developer: Code review
- database-expert: Database check
- devops-engineer: Infrastructure check
- security-auditor: Security breach check
- qa-engineer: Reproduction steps
```

### Case 2: Simple Refactoring
**Scenario**: Same agent type needed for multiple similar tasks

**Rule Exception**: Can run same agent sequentially in quick succession
```
Sequential (same agent):
1. code-reviewer: Review PR #123
2. code-reviewer: Review PR #124
3. code-reviewer: Review PR #125

Not parallel, but rapid sequential execution is acceptable
```

---

## Enforcement & Monitoring

### Pre-Execution Validation
Before launching parallel agents, check:
- [ ] Single message with multiple Task calls?
- [ ] All agents are different types?
- [ ] Tasks are independent (no dependencies)?
- [ ] Clear boundaries defined for each?
- [ ] Agent count is 3-5 (or justified exception)?
- [ ] Resource conflicts checked?
- [ ] Sync points defined?

### During Execution
Monitor for:
- Agent failures
- Blocking conditions
- Dependency violations
- Resource conflicts
- Progress stalls

### Post-Execution Review
Validate:
- All agents completed successfully
- No conflicts occurred
- Success criteria met
- Integration successful
- Time savings achieved

---

## Benefits of Following Rules

When rules are followed correctly:
- ✅ **30-50% time savings** through parallelization
- ✅ **Zero conflicts** from proper planning
- ✅ **Clear accountability** with defined boundaries
- ✅ **Easy monitoring** with independent tracking
- ✅ **Graceful error handling** through isolation
- ✅ **Predictable outcomes** from dependency management

---

## Related Documentation

- [Orchestrator Agent](../.claude/agents/orchestrator.md) - Uses these rules for coordination
- [PARALLEL_SUBAGENTS_GUIDE.md](../../docs/PARALLEL_SUBAGENTS_GUIDE.md) - User-facing parallel execution guide
- [CLAUDE_SUBAGENTS_GUIDE.md](../../docs/CLAUDE_SUBAGENTS_GUIDE.md) - Complete SubAgents system overview

---

**These rules are mandatory for parallel SubAgent execution. Violations will result in sequential execution, conflicts, or failures.**
