# Planning Rules

> Detailed implementation rules for the fstrent-planning Skill.
> These rules are derived from Cursor's fstrent_spec_tasks system
> and maintain 100% cross-IDE compatibility.

## Overview

These rules provide comprehensive guidance for project planning using the fstrent_spec_tasks system. They cover PRD (Product Requirements Document) creation, feature management, scope validation, requirements gathering, and integration with the task management system.

## PRD Generation Rules

### PRD File Location

**Mandatory Location**: `.fstrent_spec_tasks/PLAN.md`

**Single File Rule**:
- One PLAN.md per project
- No multiple PRD files
- All project planning in single document
- Features get separate files in `features/` folder

### PRD Structure Requirements

**Required Sections** (in order):
1. Product Overview (title, version, summary)
2. Goals (business, user, non-goals)
3. User Personas (types, details, roles)
4. Features (core features, references)
5. User Experience (entry points, core flow, edge cases, UI/UX)
6. Narrative (user journey paragraph)
7. Success Metrics (user, business, technical)
8. Technical Considerations (subsystems, integration, data, scalability, challenges)
9. Milestones & Sequencing (estimate, team, phases)
10. User Stories (ID, description, acceptance criteria)

**Section Numbering**:
- Use hierarchical numbering (1, 1.1, 1.2, 2, 2.1, etc.)
- Consistent formatting throughout
- Clear section headers

**Content Guidelines**:
- Product summary: 2-3 paragraphs
- Goals: Bullet lists
- Personas: Brief descriptions
- Features: Hierarchical with priorities
- Narrative: Single paragraph
- User stories: Standard format with IDs

### PRD Creation Process

**Step 1: Gather Requirements**
- Use 27-question framework (see below)
- Ask mandatory scope questions
- Document assumptions
- Identify constraints

**Step 2: Create Initial Structure**
- Copy PRD template
- Fill in known information
- Mark TBD sections
- Add project-specific sections if needed

**Step 3: Populate Content**
- Write product overview
- Define goals and non-goals
- Create user personas
- List core features
- Document user experience
- Write success metrics
- Add technical considerations
- Plan milestones
- Create user stories

**Step 4: Review & Refine**
- Check all required sections present
- Verify consistency
- Validate against scope questions
- Ensure features link to user stories
- Confirm technical feasibility

**Step 5: Link to System**
- Create feature documents in `features/`
- Reference features in tasks
- Update PROJECT_CONTEXT.md
- Update SUBSYSTEMS.md

### PRD Update Rules

**When to Update**:
- Scope changes
- New features added
- Requirements clarified
- Technical approach changes
- Milestones adjusted

**Update Process**:
- Document change reason
- Update affected sections
- Increment version number
- Update related feature documents
- Notify team of changes

**Version Control**:
- Version format: Major.Minor (1.0, 1.1, 2.0)
- Major version: Significant scope/goal changes
- Minor version: Feature additions, clarifications
- Document version history in PRD

## Feature Management Rules

### Feature Folder Structure

**Location**: `.fstrent_spec_tasks/features/`

**Naming Convention**: `{feature-name}.md`
- Use lowercase with hyphens
- Descriptive, not generic
- Examples: `user-authentication.md`, `task-management.md`, `reporting-dashboard.md`

### Feature Document Format

**Required Sections**:
1. Feature: [Name] (title)
2. Overview (brief description)
3. Requirements (bullet list)
4. User Stories (with IDs)
5. Technical Considerations (subsystems, dependencies, integration)
6. Acceptance Criteria (checklist)
7. Related Tasks (links to TASKS.md)

**User Story Format**:
```markdown
- **US-001**: As a [persona], I want to [action] so that [benefit]
```

**Acceptance Criteria Format**:
```markdown
- [ ] Criterion 1
- [ ] Criterion 2
```

### Feature Lifecycle

**Creation**:
1. Identify feature need
2. Create feature document
3. Link from PLAN.md
4. Create related tasks
5. Assign priority

**Development**:
1. Tasks reference feature
2. Track progress via tasks
3. Update acceptance criteria
4. Document technical decisions

**Completion**:
1. All acceptance criteria met
2. All related tasks completed
3. Feature tested and verified
4. Documentation updated

### Feature-Task Relationships

**Linking**:
- Tasks reference features in YAML: `feature: Feature Name`
- Feature documents list related tasks
- Bidirectional references maintained

**Tracking**:
- Feature completion = all tasks completed
- Feature progress = task completion percentage
- Feature blocked = any task blocked

## Scope Validation Rules

### Mandatory Scope Questions

**Ask BEFORE creating PRD**:

1. **User Context & Deployment**
   - Personal (1 user): Simple, file-based, minimal security
   - Small team (2-10): Basic sharing, simple user management
   - Broader (10+): Full authentication, role management, scalability

2. **Security Requirements**
   - Minimal: Basic validation, no authentication
   - Standard: User auth, session management, basic authorization
   - Enhanced: Role-based access, encryption, audit trails
   - Enterprise: SAML/SSO, compliance, advanced security

3. **Scalability Expectations**
   - Basic: Works for expected load, simple architecture
   - Moderate: Handles growth, some optimization
   - High: Speed-optimized, caching, efficient queries
   - Enterprise: Load balancing, clustering, horizontal scaling

4. **Feature Complexity**
   - Minimal: Core functionality, keep simple
   - Standard: Core plus reasonable conveniences
   - Feature-Rich: Comprehensive with advanced options
   - Enterprise: Full-featured with extensive configuration

5. **Integration Requirements**
   - Standalone: No external integrations
   - Basic: File import/export, basic API
   - Standard: REST API, webhooks, common integrations
   - Enterprise: Comprehensive API, message queues, enterprise systems

### Over-Engineering Prevention

**Default to Simplicity**:
- **Authentication**: Don't add role permissions unless requested
- **Database**: Use simple file-based unless DB explicitly requested
- **API**: Don't add comprehensive REST beyond required
- **Architecture**: Default monolith unless scale requires separation

**Red Flags**:
- Adding features "just in case"
- Building for scale not needed
- Complex architecture for simple problem
- Over-abstraction without clear benefit

**Validation**:
- Every feature must map to user story
- Every technical decision must have justification
- Complexity must be explicitly requested or clearly needed

## Planning Questionnaire Rules

### 27-Question Framework

**Purpose**: Comprehensive requirements gathering

**Usage**:
- Ask questions in order
- Document all answers
- Use answers to inform PRD
- Revisit if scope changes

**Question Categories**:
1. **Phase 1: Project Context** (Q1-Q7)
   - Problem definition
   - Success criteria
   - User identification
   - Usage patterns

2. **Phase 2: Technical Requirements** (Q8-Q16)
   - Deployment model
   - Integration needs
   - Data handling
   - Performance expectations

3. **Phase 3: Feature Scope** (Q17-Q22)
   - Essential features (MVP)
   - Nice-to-have features
   - Features to avoid
   - User experience priorities

4. **Phase 4: Timeline & Resources** (Q23-Q27)
   - Timeline drivers
   - Delivery preferences
   - Trade-offs
   - Constraints

**Documentation**:
- Record all questions and answers
- Store in PRD or separate document
- Reference during planning
- Update if answers change

### Question Adaptation

**Tailor to Project**:
- Skip irrelevant questions
- Add project-specific questions
- Adjust based on context
- Focus on unknowns

**Follow-Up Questions**:
- Ask "why" for key decisions
- Clarify ambiguous answers
- Explore edge cases
- Validate assumptions

## Codebase Analysis Rules

### Existing Project Analysis

**When to Analyze**:
- Initializing fstrent_spec_tasks in existing project
- Documenting legacy system
- Planning refactoring
- Onboarding new team members

**Analysis Process**:

1. **File Structure Analysis**
   - Scan directory structure
   - Identify main components
   - Map file organization
   - Document patterns

2. **Dependency Mapping**
   - Analyze imports/requires
   - Map component relationships
   - Identify coupling
   - Document dependencies

3. **Feature Extraction**
   - Identify user-facing features
   - Map code to features
   - Document feature boundaries
   - Create feature documents

4. **Subsystem Identification**
   - Group related functionality
   - Define subsystem boundaries
   - Document responsibilities
   - Update SUBSYSTEMS.md

5. **Integration Discovery**
   - Find external system connections
   - Document APIs used
   - Identify data flows
   - Map integration points

### PRD Generation from Code

**Automated Steps**:
1. Analyze codebase structure
2. Extract features and components
3. Generate initial PLAN.md
4. Create feature documents
5. Identify subsystems

**Manual Steps**:
1. Add business context
2. Define user personas
3. Write user stories
4. Add success metrics
5. Document goals and non-goals

## Integration Rules

### Task System Integration

**Feature-Task Linking**:
- Tasks reference features in YAML
- Features list related tasks
- Track feature progress via tasks
- Feature completion = all tasks done

**Dependencies**:
- Feature dependencies → task dependencies
- Task blocking → feature blocking
- Milestone planning uses feature grouping

### Bug System Integration

**Feature-Bug Linking**:
- Bugs reference affected features
- Features track related bugs
- Bug severity affects feature priority
- Feature fixes tracked via bug resolution

### File Organization Integration

**Folder Structure**:
```
.fstrent_spec_tasks/
├── PLAN.md              # Main PRD
├── features/            # Feature documents
│   ├── feature-a.md
│   ├── feature-b.md
│   └── feature-c.md
├── tasks/               # Task files (reference features)
└── PROJECT_CONTEXT.md   # High-level context
```

**Naming Consistency**:
- Feature files: lowercase-with-hyphens
- Feature names in PLAN.md match filenames
- Task YAML references match feature names

## Integration with Cursor

These rules maintain 100% compatibility with Cursor's fstrent_spec_tasks system:

- **File Format**: Identical PRD structure and feature format
- **File Locations**: Same directory structure
- **Naming Conventions**: Same feature naming patterns
- **Content Structure**: Same section organization
- **Integration**: Same feature-task-bug relationships

**Cursor Rules Source**: `.cursor/rules/fstrent_spec_tasks/rules/plans.mdc`

## Cross-References

- **Main Skill**: `SKILL.md` - Complete skill documentation
- **Reference Materials**: `reference/` - PRD templates, questionnaire, scope validation
- **Examples**: `examples/` - Sample PRDs and feature documents
- **Task Management**: See `fstrent-task-management` Skill
- **QA Integration**: See `fstrent-qa` Skill

## Usage Notes

### For Claude Code Users

Claude Code will use these rules automatically when the `fstrent-planning` Skill is triggered. The Skill is triggered by:
- User mentions "plan", "PRD", "requirements"
- User requests feature documentation
- User asks about project scope or goals
- User initiates planning process

### For Cursor Users

Cursor uses the equivalent rules from `.cursor/rules/fstrent_spec_tasks/rules/plans.mdc`. Both systems read and write the same `.fstrent_spec_tasks/` files, ensuring seamless collaboration.

### Best Practices

1. **Start with scope questions**: Prevent over-engineering
2. **Use the questionnaire**: Comprehensive requirements gathering
3. **Link everything**: Features → Tasks → Bugs
4. **Keep PLAN.md updated**: Living document, not one-time
5. **Create feature documents**: Don't put everything in PLAN.md
6. **Document assumptions**: Make implicit explicit
7. **Version your PRD**: Track changes over time

---

*These rules ensure consistent, comprehensive project planning across both Claude Code and Cursor environments.*

