# Oracle APEX Development - Skill Rules

## Skill Organization

This file defines how the Oracle APEX Development skill should be invoked and used by Claude Code.

## When to Activate

### Automatic Triggers
Activate this skill when the user mentions any of:
- "APEX application"
- "Oracle APEX"
- "low-code application"
- "Interactive Grid"
- "Interactive Report"
- "APEX form"
- "APEX dashboard"
- "APEX REST"
- "APEX authentication"
- "APEX deployment"
- "APEX chart"
- "APEX visualization"

### Context Clues
Also activate when:
- User requests web application development on Oracle database
- User mentions rapid application development
- User asks about database-driven web apps
- User references APEX-specific components (regions, items, processes)
- User mentions ORDS (Oracle REST Data Services)

## Delegation Rules

### Delegate to oracle-apex-specialist SubAgent When
- Multi-page application architecture needed
- Complex security/authentication schemes
- Performance optimization for enterprise scale
- Custom plugin development
- Migration from legacy systems
- REST API integration design
- Comprehensive application review

### Delegate to database-expert SubAgent When
- Schema design and normalization needed
- Complex SQL query optimization
- PL/SQL package design for business logic
- Database performance tuning
- Index strategy planning

### Delegate to security-auditor SubAgent When
- Security vulnerability assessment needed
- SQL injection testing required
- Authorization scheme review
- Comprehensive security audit

## Skill Components

### Reference Guides (reference/)
1. apex_architecture.md - APEX architecture and components
2. interactive_grids.md - Interactive Grid development
3. forms_reports.md - Forms and Reports best practices
4. charts_visualizations.md - Data visualization
5. plsql_integration.md - PL/SQL integration patterns
6. rest_api_integration.md - REST API integration
7. authentication_security.md - Security best practices
8. performance_tuning.md - Performance optimization

### Templates (templates/)
1. crud_application.sql - Complete CRUD application
2. dashboard_template.sql - Dashboard with charts
3. report_template.sql - Interactive report
4. form_template.sql - Form with validations
5. api_template.sql - REST API module
6. authentication_scheme.sql - Custom authentication

### Examples (examples/)
1. employee_management_app.md - Complete employee management system
2. sales_dashboard.md - Sales analytics dashboard
3. inventory_tracker.md - Inventory management app
4. api_integration_example.md - Third-party API integration

### Scripts (scripts/)
1. apex_export.py - Export APEX applications
2. apex_import.py - Import applications
3. apex_deployment.py - Multi-environment deployment
4. apex_backup.py - Workspace backup

## Usage Patterns

### Pattern 1: Quick Reference
User asks about APEX feature → Reference appropriate guide → Provide code examples

### Pattern 2: Application Development
User requests application → Invoke oracle-apex-specialist SubAgent → Use templates as starting point → Customize for requirements

### Pattern 3: Integration
User needs database work → Collaborate with database-expert → Use hanx-database-tools skill → Build APEX UI on top

### Pattern 4: Troubleshooting
User reports issue → Check reference guides → Verify best practices → Debug and resolve

## Best Practices

### Do
- Always use bind variables (SQL injection prevention)
- Encapsulate business logic in PL/SQL packages
- Apply authorization to sensitive components
- Enable Session State Protection
- Implement proper error handling
- Use pagination for large datasets
- Create indexes on filter columns
- Test with realistic data volumes
- Version control application exports
- Document complex processes

### Don't
- Concatenate user input into SQL (SQL injection risk)
- Put complex logic directly in APEX processes
- Skip authorization checks
- Ignore performance implications
- Use SELECT * in production
- Load 10,000+ rows without pagination
- Deploy without testing
- Forget to handle errors
- Skip security validations
- Ignore APEX Advisor recommendations

## Success Criteria

An APEX development task is successful when:
- Application functions correctly end-to-end
- Security measures implemented (auth, authz, validation)
- Performance is acceptable (< 3 second page loads)
- Code follows APEX best practices
- Tests pass (unit, integration, security)
- Documentation is complete
- Version controlled
- Ready for deployment

## Integration with Project Workflow

### With Task Management
- Create tasks for APEX development work
- Track feature implementation progress
- Document APEX-specific requirements
- Link to relevant reference guides

### With Quality Assurance
- Test APEX applications thoroughly
- Use APEX Advisor for code quality
- Report bugs with page/region/item details
- Test authorization schemes

### With Deployment
- Export applications for version control
- Deploy using established pipeline
- Test in staging before production
- Monitor post-deployment

---

**Summary**: This skill provides comprehensive APEX development support through reference guides, templates, examples, and utility scripts. Delegate to appropriate SubAgents for specialized work, and follow best practices consistently.
