---
name: fstrent-planning
description: Create and manage project plans, PRDs, and feature documentation in .fstrent_spec_tasks/ folder. Use when planning projects, creating requirements documents, defining features, conducting scope validation, or gathering requirements. Triggers on requests mentioning plan, PRD, requirements, features, scope, or project planning. ENFORCES feature file creation for multi-task features (see FEATURE_GUIDELINES.md).
---

# fstrent Planning Skill

Create and manage comprehensive project plans, Product Requirements Documents (PRDs), and feature specifications using the fstrent_spec_tasks planning system. This Skill provides structured planning workflows that prevent over-engineering while ensuring thorough requirements gathering.

## System Overview

The fstrent_spec_tasks planning system uses:
- **PLAN.md**: `.fstrent_spec_tasks/PLAN.md` - Main Product Requirements Document
- **Features**: `.fstrent_spec_tasks/features/` - Individual feature specifications
- **Project Context**: `.fstrent_spec_tasks/PROJECT_CONTEXT.md` - Project goals and scope
- **Tasks**: Links to `.fstrent_spec_tasks/TASKS.md` for implementation tracking

## PRD Structure

### File Location
**Single mandatory file**: `.fstrent_spec_tasks/PLAN.md`

### 10-Section PRD Template

#### 1. Product Overview
- **1.1 Document title and version**: PRD title and version number
- **1.2 Product summary**: 2-3 paragraph overview

#### 2. Goals
- **2.1 Business goals**: Business objectives
- **2.2 User goals**: What users aim to achieve
- **2.3 Non-goals**: Explicitly out-of-scope items

#### 3. User Personas
- **3.1 Key user types**: Primary user categories
- **3.2 Basic persona details**: Brief persona descriptions
- **3.3 Role-based access**: Permissions and access levels

#### 4. Features
- **4.1 Core Features**: Feature list with priorities (High/Medium/Low)
- **4.2 Feature References**: Links to individual feature documents

#### 5. User Experience
- **5.1 Entry points & first-time user flow**: Initial access patterns
- **5.2 Core experience**: Main user workflows
- **5.3 Advanced features & edge cases**: Less common scenarios
- **5.4 UI/UX highlights**: Key design principles

#### 6. Narrative
Single paragraph describing user journey and benefits

#### 7. Success Metrics
- **7.1 User-centric metrics**: Task completion, satisfaction
- **7.2 Business metrics**: Conversion, revenue impact
- **7.3 Technical metrics**: Performance, error rates

#### 8. Technical Considerations
- **8.1 Affected subsystems**: Primary and secondary systems
- **8.2 Integration points**: External system interactions
- **8.3 Data storage & privacy**: Data handling, compliance
- **8.4 Scalability & performance**: Load expectations, targets
- **8.5 Potential challenges**: Risks and technical hurdles

#### 9. Milestones & Sequencing
- **9.1 Project estimate**: Small/Medium/Large with time estimate
- **9.2 Team size & composition**: Required team structure
- **9.3 Suggested phases**: Implementation phases with deliverables

#### 10. User Stories
Individual user stories with:
- **ID**: US-001, US-002, etc.
- **Description**: As a [persona], I want to [action] so that [benefit]
- **Acceptance Criteria**: Specific, measurable outcomes

## Feature Management

### Feature Document Structure
**Location**: `.fstrent_spec_tasks/features/{feature-name}.md`

**Template**:
```markdown
# Feature: [Feature Name]

## Overview
[Brief description of the feature]

## Requirements
- [Requirement 1]
- [Requirement 2]

## User Stories
- **US-001**: As a [persona], I want to [action] so that [benefit]
- **US-002**: As a [persona], I want to [action] so that [benefit]

## Technical Considerations
- **Subsystems**: [List affected subsystems]
- **Dependencies**: [List feature dependencies]
- **Integration Points**: [List integration requirements]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Related Tasks
- Links to tasks in TASKS.md that implement this feature
- Links to bugs in BUGS.md that affect this feature
```

### Feature Naming Convention
- Lowercase with hyphens: `user-authentication.md`, `payment-processing.md`
- Descriptive and specific
- Matches feature name in PLAN.md

### Feature-Task Integration
- Tasks reference features via `feature:` field in YAML
- Feature documents list implementing tasks
- Feature completion tracked through task completion
- **CRITICAL**: Feature files MUST be created when 2+ tasks share same feature (see FEATURE_GUIDELINES.md)

## Scope Validation

### Mandatory Questions (Ask Before Creating PRD)

**Purpose**: Prevent over-engineering and clarify requirements

#### 1. User Context & Deployment
"Intended for personal use, small team, or broader deployment?"
- **Personal (1 user)**: Simple, file-based, minimal security
- **Small team (2-10)**: Basic sharing, simple user management
- **Broader (10+)**: Full authentication, role management, scalability

#### 2. Security Requirements
"Security expectations?"
- **Minimal**: Basic validation, no authentication
- **Standard**: User auth, session management, basic authorization
- **Enhanced**: Role-based access, encryption, audit trails
- **Enterprise**: SAML/SSO, compliance, advanced security

#### 3. Scalability Expectations
"Performance and scalability expectations?"
- **Basic**: Works for expected load, simple architecture
- **Moderate**: Handles growth, some optimization
- **High**: Speed-optimized, caching, efficient queries
- **Enterprise**: Load balancing, clustering, horizontal scaling

#### 4. Feature Complexity
"How much complexity comfortable with?"
- **Minimal**: Core functionality, keep simple
- **Standard**: Core plus reasonable conveniences
- **Feature-Rich**: Comprehensive with advanced options
- **Enterprise**: Full-featured with extensive configuration

#### 5. Integration Requirements
"Integration needs?"
- **Standalone**: No external integrations
- **Basic**: File import/export, basic API
- **Standard**: REST API, webhooks, common integrations
- **Enterprise**: Comprehensive API, message queues, enterprise systems

### Over-Engineering Prevention Rules

**Apply these defaults unless explicitly requested:**
- **Authentication**: Don't add role permissions unless requested
- **Database**: Use simple file-based unless DB explicitly requested
- **API**: Don't add comprehensive REST beyond required
- **Architecture**: Default monolith unless scale requires separation

## Planning Questionnaire

### 27-Question Framework

Use this comprehensive questionnaire for thorough requirements gathering. Ask questions progressively, not all at once.

#### Phase 1: Project Context (Q1-Q7)

**Q1**: Primary problem this system solves?
- Follow-up: Who experiences it, how handled today?

**Q2**: What does success look like?
- Follow-up: How measured, failure indicators?

**Q3**: Replacing existing or creating new?
- If replacing: pain points
- If new: why needed now?

**Q4**: Primary users?
- End users, Admins, Stakeholders, External

**Q5**: User count?
- Single, 2-10, 11-50, 51-200, 200+

**Q6**: Usage frequency?
- Occasional, Daily, Continuous, Peak periods

**Q7**: Access locations?
- Local, Office, Remote, Internet, Mobile

#### Phase 2: Technical Requirements (Q8-Q16)

**Q8**: Deployment?
- Local desktop, Local server, Cloud, Hybrid, No preference

**Q9**: Maintenance comfort?
- Minimal, Basic, Intermediate, Advanced

**Q10**: Integration needs?
- AD, Databases, Business apps, Monitoring, Backup

**Q11**: Data types?
- Public, Internal, PII, Financial, Healthcare, Regulated

**Q12**: Security requirements?
- Basic, Industry compliance, Government, Custom, None

**Q13**: Access control?
- All see all, Role-based, Department, Individual, External

**Q14**: Performance expectations?
- Basic seconds, Good <1s, High instant, Not critical

**Q15**: Data volume?
- Thousands, Hundreds of thousands, Millions, Billions, Growing

**Q16**: Peak usage?
- Consistent, Business hours, Month/quarter, Seasonal, Event-driven

#### Phase 3: Feature Scope (Q17-Q22)

**Q17**: Essential features (MVP)?
- List core features and deal-breakers

**Q18**: Nice-to-have features?
- List convenience and future enhancements

**Q19**: Features to avoid?
- Over-complexity, specific integrations, approaches

**Q20**: Priority: ease vs power?
- Ease, Power, Balanced, Depends on user

**Q21**: Interface examples you like?
- Reference apps, patterns, accessibility

**Q22**: User training investment?
- Self-explanatory, Brief, Formal, Complex OK

#### Phase 4: Timeline & Resources (Q23-Q27)

**Q23**: Timeline drivers?
- Business deadline, Budget, Competition, Regulatory, Personal

**Q24**: Delivery preference?
- Quick prototype, Phased, Complete, Iterative

**Q25**: Trade-offs?
- Core over polish, Polish over features, Speed over performance

**Q26**: Available resources?
- Dev time, Expertise, Budget, Third-party services

**Q27**: Hard constraints?
- Specific tech, No cloud, Budget limits, Policies

### Questionnaire Best Practices
- Ask 3-5 questions per message to avoid overwhelming
- Start with most important questions
- Follow up based on answers
- Conclude when clear sense of functionality emerges

## Codebase Analysis (Existing Projects)

### When to Use
When initializing fstrent_spec_tasks in existing projects with code

### Analysis Process

1. **File Structure Analysis**
   - Identify main components and modules
   - Determine project organization patterns
   - Map directory structure to functionality

2. **Dependency Mapping**
   - Map relationships between components
   - Identify external dependencies
   - Document integration points

3. **Feature Extraction**
   - Identify features from code patterns
   - Determine feature boundaries
   - Group related functionality

4. **Subsystem Identification**
   - Group related functionality into subsystems
   - Define subsystem boundaries
   - Document subsystem responsibilities

5. **Integration Discovery**
   - Find external system connections
   - Identify APIs and services used
   - Document data flows

### Analysis Outputs
- Generate PLAN.md based on current code structure
- Create feature documents for each major component
- Identify subsystems from code organization
- Document current architecture and integration points

## Planning Operations

### Create New PRD

**Process**:
1. Conduct scope validation (5 essential questions)
2. Optionally run planning questionnaire (27 questions)
3. Create `.fstrent_spec_tasks/PLAN.md` with 10-section template
4. Fill in all sections based on gathered requirements
5. Create feature documents in `features/` folder
6. Link features to PLAN.md

### Update Existing PRD

**Process**:
1. Read current PLAN.md
2. Identify sections to update
3. Make changes while preserving structure
4. Update version number
5. Update related feature documents if needed

### Create Feature Document

**Process**:
1. **Validation**: Check if feature file needed (see FEATURE_GUIDELINES.md decision tree)
   - Multiple tasks (2+) for same feature? → REQUIRED
   - Multi-component feature? → REQUIRED
   - Has user stories? → REQUIRED
   - Single isolated task? → SKIP
2. Determine feature name (lowercase-with-hyphens)
3. Create `.fstrent_spec_tasks/features/{feature-name}.md`
4. Use feature template from FEATURE_GUIDELINES.md (complete or minimal)
5. Fill in overview, requirements, user stories
6. Specify technical considerations
7. Add acceptance criteria
8. List all related tasks
9. Reference in PLAN.md section 4.1 (if creating from PRD)

**CRITICAL**: When creating tasks:
- Create feature file BEFORE marking first task as [📋]
- Update feature file as new tasks are added
- Keep task files and feature files synchronized

### View Project Plan

**Process**:
1. Read `.fstrent_spec_tasks/PLAN.md`
2. Display relevant sections
3. Optionally read related feature documents
4. Show project context from PROJECT_CONTEXT.md

## Integration with Other Systems

### Link to Tasks
- Tasks reference features via `feature:` YAML field
- Feature documents list implementing tasks
- Track feature progress through task completion

### Link to Bugs
- Bugs reference affected features
- Feature documents list related bugs
- Feature impact assessment through bug analysis

### Link to Project Context
- PLAN.md aligns with PROJECT_CONTEXT.md mission
- Features support project goals
- Scope boundaries defined in both documents

## File Organization

### Core Planning Files
- `.fstrent_spec_tasks/PLAN.md` - Main PRD
- `.fstrent_spec_tasks/features/` - Feature documents
- `.fstrent_spec_tasks/PROJECT_CONTEXT.md` - Project goals

### Auto-Creation
Automatically create missing folders and files:
- `.fstrent_spec_tasks/` directory
- `.fstrent_spec_tasks/features/` subdirectory
- `PLAN.md` with blank template if missing
- `PROJECT_CONTEXT.md` with template if missing

## Instructions

### Proactive Feature File Validation

When creating tasks, ALWAYS:

1. **Check Feature Field**: Look at task YAML `feature:` field
2. **Validate Feature File Exists**: Check if `.fstrent_spec_tasks/features/{feature-name}.md` exists
3. **Apply Decision Rules**:
   - If 2+ tasks share same feature AND no feature file → **CREATE FEATURE FILE NOW**
   - If multi-component feature AND no feature file → **CREATE FEATURE FILE NOW**
   - If task has user stories AND no feature file → **CREATE FEATURE FILE NOW**
   - If single isolated task → Feature file optional
4. **Create Before [📋]**: Feature file MUST exist before marking task as [📋]
5. **Update Synchronously**: When adding new tasks to existing feature, update feature file

### Feature File Creation Triggers

**Automatic triggers** (create feature file without asking):
- Creating 2+ tasks with same feature name
- Creating master task with sub-tasks
- Task references feature that doesn't exist yet

**Prompt user** (ask if feature file needed):
- Creating single task that might expand later
- Unclear if task is part of larger feature
- User mentions "might add more features later"

### Validation Messages

When creating feature file, inform user:
```
"Creating feature file: features/user-authentication-system.md
This feature has multiple related tasks, so a feature file is required
for coordination and tracking."
```

When feature file already exists:
```
"Feature file exists: features/user-authentication-system.md
Updating with new task reference."
```

When feature file NOT needed:
```
"Single isolated task - no feature file needed.
Using category tags only."
```

## Best Practices

### PRD Creation
1. Always conduct scope validation first
2. Use planning questionnaire for complex projects
3. Be specific about non-goals
4. Include concrete user stories
5. Define clear success metrics

### Feature Management
1. One feature per file
2. Clear, descriptive names
3. Link to implementing tasks
4. Track acceptance criteria
5. Update as requirements evolve
6. **CRITICAL**: Create feature file BEFORE marking first task as [📋]
7. Use decision tree in FEATURE_GUIDELINES.md to determine if feature file needed
8. Keep feature files and task files synchronized

### Scope Control
1. Apply over-engineering prevention rules
2. Default to simplicity
3. Add complexity only when justified
4. Document scope boundaries clearly
5. Regular scope reviews

### Requirements Gathering
1. Ask questions progressively
2. Validate assumptions
3. Clarify ambiguities
4. Document decisions
5. Get stakeholder buy-in

## Common Workflows

### Workflow: Create Task with Feature Validation

**NEW**: Enforced workflow to ensure feature files are created when needed

1. User requests: "Create tasks for implementing user authentication"
2. Analyze request to identify if feature file needed:
   - Will there be multiple tasks? → YES → Feature file REQUIRED
   - Multi-component (frontend + backend + database)? → YES → Feature file REQUIRED
   - Has user stories? → Check with user
3. If feature file needed:
   a. Create feature file FIRST: `.fstrent_spec_tasks/features/user-authentication-system.md`
   b. Fill in feature template (use minimal template for simpler features)
   c. Add overview, user stories, acceptance criteria
4. Create first task file in `.fstrent_spec_tasks/tasks/`
5. Add feature reference to task YAML: `feature: User Authentication System`
6. Update feature file "Related Tasks" section with first task
7. Mark first task as [📋] in TASKS.md
8. Create additional task files
9. Update feature file with each new task
10. Mark additional tasks as [📋]
11. Confirm all files created and synchronized

**Validation Prompts**:
- "This appears to be a multi-task feature. I'll create a feature file first."
- "Feature file created: features/user-authentication-system.md"
- "Task file references feature in YAML frontmatter"
- "Feature file updated with task in Related Tasks section"
- "Ready to mark as [📋]"

### Workflow: Create PRD for New Project

1. User requests: "Create a project plan for a task management app"
2. Ask scope validation questions (5 essential)
3. Optionally ask planning questionnaire questions
4. Create `.fstrent_spec_tasks/PLAN.md` with 10 sections
5. Fill in sections based on answers
6. Create feature documents for core features
7. Link features in PLAN.md section 4
8. Confirm PRD created

### Workflow: Add Feature to Existing Plan

1. User requests: "Add a reporting feature to the plan"
2. Read existing PLAN.md
3. Ask clarifying questions about feature
4. Create `.fstrent_spec_tasks/features/reporting.md`
5. Fill in feature template
6. Update PLAN.md section 4.1 to include new feature
7. Confirm feature added

### Workflow: Conduct Scope Validation

1. User requests: "Help me plan a new project"
2. Ask: "Intended for personal use, small team, or broader deployment?"
3. Ask: "Security expectations?"
4. Ask: "Performance and scalability expectations?"
5. Ask: "How much complexity comfortable with?"
6. Ask: "Integration needs?"
7. Summarize answers and recommend approach
8. Proceed with PRD creation

### Workflow: Analyze Existing Codebase

1. User requests: "Create a plan for this existing project"
2. Analyze file structure
3. Identify main components
4. Extract features from code
5. Map dependencies
6. Generate PLAN.md based on analysis
7. Create feature documents for major components
8. Confirm analysis complete

## Examples

### Example: Create Simple PRD

**User**: "Create a plan for a personal todo list app"

**Action**:
1. Conduct scope validation:
   - Personal use (1 user)
   - Minimal security
   - Basic performance
   - Minimal complexity
   - Standalone

2. Create `.fstrent_spec_tasks/PLAN.md`:

```markdown
# PRD: Personal Todo List App

## 1. Product overview
### 1.1 Document title and version
- PRD: Personal Todo List App
- Version: 1.0

### 1.2 Product summary
A simple, personal todo list application for managing daily tasks. The app allows a single user to create, organize, and track tasks with basic features like due dates and priorities. Designed for simplicity and ease of use without unnecessary complexity.

## 2. Goals
### 2.1 Business goals
- Provide personal productivity tool
- Maintain simplicity and ease of use
- Minimize maintenance overhead

### 2.2 User goals
- Quickly add and organize tasks
- Track task completion
- Set priorities and due dates
- View tasks at a glance

### 2.3 Non-goals
- Multi-user support
- Team collaboration features
- Complex project management
- Mobile apps (web only)
- Cloud sync

## 3. User personas
### 3.1 Key user types
- Individual user managing personal tasks

### 3.2 Basic persona details
- **Solo User**: Individual managing personal todo list for daily tasks and projects

### 3.3 Role-based access
- Single user with full access to all features

## 4. Features
### 4.1 Core Features
- **Task Management** (Priority: High)
  - Create, edit, delete tasks
  - Mark tasks as complete
  - Set due dates
  - Assign priorities (High/Medium/Low)

- **Task Organization** (Priority: Medium)
  - Group tasks by category
  - Filter by status, priority, due date
  - Search tasks

- **Task Persistence** (Priority: High)
  - Save tasks to local file
  - Load tasks on startup

### 4.2 Feature References
- task-management.md
- task-organization.md
- task-persistence.md

[Continue with remaining sections...]
```

3. Create feature documents in `features/`
4. Confirm: "Created PRD for Personal Todo List App with 3 core features"

### Example: Add Feature

**User**: "Add a recurring tasks feature"

**Action**:
1. Read existing PLAN.md
2. Create `.fstrent_spec_tasks/features/recurring-tasks.md`:

```markdown
# Feature: Recurring Tasks

## Overview
Allow users to create tasks that automatically repeat on a schedule (daily, weekly, monthly).

## Requirements
- Define recurrence pattern (daily, weekly, monthly)
- Automatically create new task instances
- Option to complete or skip individual instances
- Edit or delete recurring series

## User Stories
- **US-010**: As a user, I want to create recurring tasks so that I don't have to manually recreate regular tasks
- **US-011**: As a user, I want to modify recurrence patterns so that I can adjust schedules as needed

## Technical Considerations
- **Subsystems**: Task Management, Task Persistence
- **Dependencies**: Core task management feature
- **Integration Points**: Task creation, task storage

## Acceptance Criteria
- [ ] User can set recurrence pattern when creating task
- [ ] New task instances created automatically
- [ ] User can complete individual instances
- [ ] User can edit or delete entire series
- [ ] Recurrence data persisted correctly

## Related Tasks
- Task to implement recurrence UI
- Task to implement recurrence logic
- Task to update persistence layer
```

3. Update PLAN.md section 4.1:
```markdown
- **Recurring Tasks** (Priority: Medium)
  - Create tasks with recurrence patterns
  - Automatic task instance creation
  - Manage recurring series
```

4. Confirm: "Added Recurring Tasks feature to plan"

## Compatibility Notes

This Skill works with the same file format used by Cursor's fstrent_spec_tasks planning system. Plans and features created in Claude Code can be viewed and updated in Cursor, and vice versa. The system uses:

- Standard markdown format
- Consistent section structure
- Git-friendly plain text files
- Cross-IDE compatible templates

Teams can use both IDEs interchangeably for planning activities.

