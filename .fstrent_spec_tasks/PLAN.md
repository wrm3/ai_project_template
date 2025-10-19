# PRD: fstrent_spec_tasks Claude Code Adaptation

## 1. Product overview

### 1.1 Document title and version
- PRD: fstrent_spec_tasks Claude Code Adaptation
- Version: 1.0

### 1.2 Product summary
This project creates a Claude Code adaptation of the fstrent_spec_tasks task management system, enabling seamless cross-IDE compatibility. The adaptation translates Cursor's rule-based system into Claude Code's Skills/Agents/Commands architecture while maintaining 100% compatibility with shared task data files. This allows development teams to use Cursor or Claude Code interchangeably while working with the same project plans, tasks, and documentation.

## 2. Goals

### 2.1 Business goals
- Enable teams to use multiple AI IDEs without workflow disruption
- Preserve existing fstrent_spec_tasks investments for Cursor users
- Expand fstrent_spec_tasks adoption to Claude Code user base
- Demonstrate cross-IDE compatibility as a competitive advantage

### 2.2 User goals
- Switch between Cursor and Claude Code without losing context
- Maintain consistent task management across team members using different IDEs
- Access task management features regardless of IDE choice
- Learn one system that works everywhere

### 2.3 Non-goals
- Modifying the core fstrent_spec_tasks data structure
- Creating IDE-specific features that break compatibility
- Supporting IDEs other than Cursor and Claude Code (initially)
- Replacing existing Cursor rules system

## 3. User personas

### 3.1 Key user types
- Development teams using mixed IDEs
- Individual developers switching between IDEs
- Project managers tracking work across team members
- New users evaluating AI IDE options

### 3.2 Basic persona details
- **Mixed Team Developer**: Uses Cursor, but teammates use Claude Code; needs seamless collaboration
- **IDE Switcher**: Evaluating both IDEs; wants to maintain workflow regardless of choice
- **Project Manager**: Doesn't code but needs to view/update tasks and plans
- **New Adopter**: Learning fstrent_spec_tasks; wants simplest path to productivity

### 3.3 Role-based access
- **Developer**: Full read/write access to tasks, plans, and code
- **Project Manager**: Read/write access to plans and tasks, read-only for code
- **Contributor**: Read access to plans, write access to assigned tasks

## 4. Features

### 4.1 Core Features

- **Claude Code Skills** (Priority: High)
  - fstrent-task-management Skill for task CRUD operations
  - fstrent-planning Skill for PRD and feature management
  - fstrent-qa Skill for bug tracking
  - Auto-activation based on user requests mentioning tasks/plans

- **Shared Data Layer** (Priority: High)
  - 100% compatibility with Cursor's `.fstrent_spec_tasks/` structure
  - Same YAML frontmatter format
  - Same markdown templates
  - Bidirectional read/write without conflicts

- **Claude Code Commands** (Priority: Medium)
  - `/project:create-task` for quick task creation
  - `/project:update-task-status` for status updates
  - `/project:view-plan` for plan overview
  - `/project:view-context` for project context

- **Task Expansion Agent** (Priority: Medium)
  - Subagent for complex task breakdown
  - Uses same complexity scoring as Cursor rules
  - Creates sub-tasks in shared format

- **Documentation & Examples** (Priority: High)
  - Setup guide for Claude Code users
  - Migration guide for Cursor users
  - Example workflows for both IDEs
  - Troubleshooting guide

### 4.2 Feature References
- Each feature has corresponding documentation in `features/` folder
- Features reference shared `.fstrent_spec_tasks/` data files
- Skills reference Anthropic's official Skills specification

## 5. User experience

### 5.1 Entry points & first-time user flow
**For Claude Code Users:**
1. Install fstrent_spec_tasks Skills from repository
2. Claude automatically detects task-related requests
3. Skills activate and guide user through task creation
4. User works naturally with Claude, Skills handle file operations

**For Cursor Users:**
1. Continue using existing `.cursor/rules/` system
2. Optionally install Claude Code Skills for team compatibility
3. No changes to existing workflow required

### 5.2 Core experience
**Creating a Task (Claude Code):**
1. User: "Create a task to implement user authentication"
2. fstrent-task-management Skill activates automatically
3. Claude prompts for priority, dependencies, acceptance criteria
4. Skill creates task file in `.fstrent_spec_tasks/tasks/`
5. Skill updates `TASKS.md` with new entry
6. User receives confirmation with task ID

**Viewing Project Plan (Both IDEs):**
1. User requests plan overview
2. System reads `.fstrent_spec_tasks/PLAN.md`
3. Displays formatted project context
4. Shows active tasks and progress

### 5.3 Advanced features & edge cases
- Handling concurrent edits from multiple IDEs
- Resolving task ID conflicts
- Migrating existing Cursor projects to dual-IDE setup
- Syncing MCP tool configurations

### 5.4 UI/UX highlights
- Natural language interaction (no special syntax required)
- Automatic Skill activation (no manual commands for basic operations)
- Consistent file structure visible in both IDEs
- Clear status indicators using Windows-safe emojis

## 6. Narrative
A development team uses both Cursor and Claude Code based on personal preference. When a developer creates a task in Cursor using the rules system, it writes to `.fstrent_spec_tasks/TASKS.md`. Their teammate opens the same project in Claude Code, and the fstrent-task-management Skill automatically recognizes the task structure, allowing them to update task status seamlessly. The project manager reviews progress by simply opening `TASKS.md` in any text editor. Everyone works with the same data, regardless of their tool choice, eliminating workflow friction and enabling true cross-IDE collaboration.

## 7. Success metrics

### 7.1 User-centric metrics
- Time to create first task: < 2 minutes
- Task creation success rate: > 95%
- Cross-IDE compatibility rate: 100% (no data loss)
- User satisfaction with dual-IDE workflow: > 4/5

### 7.2 Business metrics
- Adoption rate among Claude Code users
- Retention of existing Cursor users
- Reduction in IDE-switching friction
- Community contributions to Skills

### 7.3 Technical metrics
- File format compatibility: 100%
- Skill activation accuracy: > 90%
- Zero data corruption incidents
- MCP tool compatibility: 100%

## 8. Technical considerations

### 8.1 Affected subsystems
- **Primary subsystems** (directly modified/extended):
  - Claude Code Skills System: New Skills for task management
  - File I/O Layer: Shared read/write to `.fstrent_spec_tasks/`
  - Documentation System: Dual-IDE guides and examples

- **Secondary subsystems** (indirectly affected):
  - MCP Tool Integration: Shared `.mcp.json` configuration
  - Version Control: Git handling of shared files
  - IDE Configuration: Separate but compatible configs

### 8.2 Integration points
- Anthropic Skills API for Claude Code
- Cursor Rules system (existing)
- MCP servers (fstrent_mcp_tasks, etc.)
- File system for shared data storage
- Git for version control

### 8.3 Data storage & privacy
- All data stored locally in project directory
- No cloud sync required
- Standard file permissions apply
- Git handles versioning and collaboration
- No PII or sensitive data in templates

### 8.4 Scalability & performance
- File-based system scales to hundreds of tasks
- Skills load progressively (metadata → body → resources)
- No database required
- Minimal memory footprint
- Fast file I/O operations

### 8.5 Potential challenges
- Concurrent edit conflicts (mitigated by Git)
- Skill activation accuracy (requires good descriptions)
- User education on dual-IDE setup
- Maintaining compatibility as IDEs evolve

## 9. Milestones & sequencing

### 9.1 Project estimate
- **Medium**: 2-3 weeks for full implementation and testing

### 9.2 Team size & composition
- Small Team: 1-2 people (1 Developer, 1 Documentation Writer)

### 9.3 Suggested phases

- **Phase 1: Core Skills Development** (1 week)
  - Key deliverables:
    - fstrent-task-management Skill
    - fstrent-planning Skill
    - fstrent-qa Skill
    - Basic testing with sample projects

- **Phase 2: Commands & Agents** (3-4 days)
  - Key deliverables:
    - Custom commands for common operations
    - Task expansion subagent
    - Integration testing

- **Phase 3: Documentation & Examples** (3-4 days)
  - Key deliverables:
    - Setup guides for both IDEs
    - Example projects
    - Troubleshooting documentation
    - Video tutorials (optional)

## 10. User stories

### 10.1 Cross-IDE Task Creation
- **ID**: US-001
- **Description**: As a developer using Claude Code, I want to create tasks that my Cursor-using teammates can see and update, so that we can collaborate seamlessly.
- **Acceptance Criteria**:
  - Task created in Claude Code appears in `.fstrent_spec_tasks/TASKS.md`
  - Task uses same YAML format as Cursor tasks
  - Cursor users can read and update the task
  - No data loss or corruption

### 10.2 Natural Language Task Management
- **ID**: US-002
- **Description**: As a Claude Code user, I want to manage tasks using natural language without learning special commands, so that I can focus on development instead of tool syntax.
- **Acceptance Criteria**:
  - Skills activate automatically for task-related requests
  - No special syntax required for basic operations
  - Clear feedback on task operations
  - Helpful prompts for required information

### 10.3 Existing Project Migration
- **ID**: US-003
- **Description**: As a Cursor user with existing fstrent_spec_tasks projects, I want to use Claude Code without migrating or converting my data, so that I can try the new IDE risk-free.
- **Acceptance Criteria**:
  - Claude Code Skills read existing `.fstrent_spec_tasks/` files
  - No conversion or migration required
  - All existing tasks and plans accessible
  - Can switch back to Cursor anytime

### 10.4 Project Plan Visualization
- **ID**: US-004
- **Description**: As a project manager, I want to view project plans and task status in either IDE, so that I can track progress regardless of which tool developers use.
- **Acceptance Criteria**:
  - PLAN.md renders correctly in both IDEs
  - Task status visible and accurate
  - Progress metrics calculated consistently
  - Export options available

### 10.5 MCP Tool Compatibility
- **ID**: US-005
- **Description**: As a developer, I want MCP tools to work the same way in both Cursor and Claude Code, so that I don't have to learn different tool configurations.
- **Acceptance Criteria**:
  - Same `.mcp.json` works in both IDEs
  - MCP tools accessible from Skills and Rules
  - Consistent tool behavior
  - Shared tool documentation

