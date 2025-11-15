# Team Wiki Examples

Practical examples for team collaboration using MediaWiki.

## Example 1: Project Dashboard

```python
from scripts.page_manager import PageManager
from scripts.category_manager import CategoryManager
from datetime import datetime

page_manager = PageManager()
cat_manager = CategoryManager()

def create_project_dashboard(project_name):
    """Create a comprehensive project dashboard."""

    dashboard_content = f"""
= {project_name} Dashboard =

{{{{Project Infobox
|name={project_name}
|status=Active
|start_date={datetime.now().strftime('%Y-%m-%d')}
|team_size=5
|priority=High
}}}}

== Quick Links ==

* [[{project_name}/Overview|Project Overview]]
* [[{project_name}/Timeline|Timeline]]
* [[{project_name}/Team|Team Members]]
* [[{project_name}/Documentation|Documentation]]

== Current Sprint ==

{{{{Sprint Status
|sprint=Sprint 15
|start={datetime.now().strftime('%Y-%m-%d')}
|end={(datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')}
|completed=12
|total=20
}}}}

=== In Progress ===

* [[Task:AUTH-123|User Authentication]]
* [[Task:API-456|REST API Development]]
* [[Task:UI-789|Dashboard UI]]

=== Blockers ===

* Waiting for API key from external service
* Database migration pending approval

== Recent Updates ==

{{{{Recent Changes|category=Project:{project_name}|limit=10}}}}

== Metrics ==

=== This Week ===

* Commits: 47
* Pull Requests: 8
* Issues Closed: 12
* Code Coverage: 87%

=== Velocity Chart ===

[[File:{project_name}_Velocity_Chart.png|600px]]

== Team Availability ==

{{{{{project_name} Team Calendar}}}}

== Documentation ==

* [[{project_name}/Architecture|Architecture Overview]]
* [[{project_name}/API|API Documentation]]
* [[{project_name}/Setup|Development Setup]]
* [[{project_name}/Deployment|Deployment Guide]]

== Resources ==

* [https://github.com/company/{project_name} GitHub Repository]
* [https://jira.company.com/project/{project_name} JIRA Board]
* [https://slack.company.com/channels/{project_name} Slack Channel]

[[Category:Projects]]
[[Category:Active Projects]]
[[Category:{project_name}]]
"""

    return page_manager.create_or_update_page(
        title=f'Project:{project_name}',
        content=dashboard_content,
        summary=f"Created dashboard for {project_name}"
    )

# Usage
from datetime import timedelta
create_project_dashboard('Phoenix')
print("✓ Project dashboard created")
```

## Example 2: Team Meeting Notes

```python
from scripts.page_manager import PageManager
from datetime import datetime

class MeetingNotesManager:
    """Manage team meeting notes."""

    def __init__(self):
        self.page_manager = PageManager()

    def create_meeting_notes(
        self,
        meeting_type='Team',
        attendees=None,
        agenda=None,
        notes=None,
        action_items=None
    ):
        """Create meeting notes page."""

        date = datetime.now().strftime('%Y-%m-%d')
        page_title = f'Meetings:{meeting_type}/{date}'

        # Build attendees section
        attendees_section = ""
        if attendees:
            attendees_section = "== Attendees ==\n\n"
            for attendee in attendees:
                attendees_section += f"* {attendee}\n"
            attendees_section += "\n"

        # Build agenda section
        agenda_section = ""
        if agenda:
            agenda_section = "== Agenda ==\n\n"
            for i, item in enumerate(agenda, 1):
                agenda_section += f"{i}. {item}\n"
            agenda_section += "\n"

        # Build notes section
        notes_section = ""
        if notes:
            notes_section = "== Notes ==\n\n"
            for topic, content in notes.items():
                notes_section += f"=== {topic} ===\n\n{content}\n\n"

        # Build action items section
        action_section = ""
        if action_items:
            action_section = "== Action Items ==\n\n"
            for item in action_items:
                action_section += f"* {{{{Action|owner={item['owner']}|due={item['due']}}}}} {item['task']}\n"
            action_section += "\n"

        # Build full content
        content = f"""
= {meeting_type} Meeting - {date} =

{{{{Meeting Info
|type={meeting_type}
|date={date}
|duration={len(attendees or [])} attendees
}}}}

{attendees_section}
{agenda_section}
{notes_section}
{action_section}
== Next Meeting ==

Scheduled for: {{{{Next Meeting Date}}}}

[[Category:Meetings]]
[[Category:{meeting_type} Meetings]]
"""

        return self.page_manager.create_or_update_page(
            title=page_title,
            content=content,
            summary=f"Created {meeting_type} meeting notes for {date}"
        )

    def create_meeting_index(self, meeting_type='Team'):
        """Create an index of all meetings."""

        from scripts.search_manager import SearchManager
        search_manager = SearchManager()

        # Find all meetings of this type
        meetings = search_manager.search_prefix(
            prefix=f'Meetings:{meeting_type}/',
            limit=100
        )

        # Sort by date (newest first)
        meetings.sort(reverse=True)

        # Build index
        content_parts = [
            f"= {meeting_type} Meeting Notes =",
            "",
            "Index of all meeting notes.",
            "",
            "== Recent Meetings ==",
            ""
        ]

        for meeting in meetings[:10]:  # Show last 10
            content_parts.append(f"* [[{meeting}]]")

        content_parts.extend([
            "",
            "== All Meetings ==",
            ""
        ])

        # Group by year
        by_year = {}
        for meeting in meetings:
            # Extract year from meeting title
            year = meeting.split('/')[-1][:4]  # Get YYYY from YYYY-MM-DD

            if year not in by_year:
                by_year[year] = []

            by_year[year].append(meeting)

        for year in sorted(by_year.keys(), reverse=True):
            content_parts.extend([
                f"=== {year} ===",
                ""
            ])

            for meeting in by_year[year]:
                content_parts.append(f"* [[{meeting}]]")

            content_parts.append("")

        content_parts.extend([
            f"[[Category:Meetings]]",
            f"[[Category:{meeting_type} Meetings]]",
            "[[Category:Index]]"
        ])

        content = '\n'.join(content_parts)

        return self.page_manager.create_or_update_page(
            title=f'Meetings:{meeting_type}/Index',
            content=content,
            summary="Updated meeting index"
        )

# Usage
manager = MeetingNotesManager()

result = manager.create_meeting_notes(
    meeting_type='Team',
    attendees=['Alice', 'Bob', 'Charlie'],
    agenda=[
        'Sprint review',
        'Upcoming releases',
        'Team building event'
    ],
    notes={
        'Sprint Review': '''
Sprint 15 completed with 95% of planned work done.
One story carried over to next sprint.
''',
        'Upcoming Releases': '''
Version 2.0 scheduled for next month.
Beta testing starts next week.
'''
    },
    action_items=[
        {'owner': 'Alice', 'due': '2025-11-15', 'task': 'Schedule beta testing'},
        {'owner': 'Bob', 'due': '2025-11-10', 'task': 'Update release notes'}
    ]
)

if result['success']:
    print("✓ Meeting notes created")

# Create meeting index
manager.create_meeting_index('Team')
```

## Example 3: Team Member Profiles

```python
from scripts.page_manager import PageManager
from scripts.file_uploader import FileUploader

page_manager = PageManager()
uploader = FileUploader()

def create_team_profile(
    name,
    role,
    email,
    skills,
    current_projects,
    bio='',
    photo_path=None
):
    """Create team member profile page."""

    # Upload photo if provided
    photo_wiki_name = None
    if photo_path:
        result = uploader.upload_file(
            filepath=photo_path,
            wiki_filename=f'{name.replace(" ", "_")}_Photo.jpg',
            description=f'Profile photo for {name}',
            categories=['Team Photos']
        )
        if result['success']:
            photo_wiki_name = result['filename']

    # Build profile content
    content_parts = [
        f"= {name} =",
        ""
    ]

    # Add photo if available
    if photo_wiki_name:
        content_parts.extend([
            f"[[File:{photo_wiki_name}|thumb|right|200px|{name}]]",
            ""
        ])

    content_parts.extend([
        f"'''Role:''' {role}",
        f"'''Email:''' {email}",
        "",
        "== Biography ==",
        "",
        bio or f"{name} is a {role} at our company.",
        "",
        "== Skills ==",
        ""
    ])

    for skill in skills:
        content_parts.append(f"* {skill}")

    content_parts.extend([
        "",
        "== Current Projects ==",
        ""
    ])

    for project in current_projects:
        content_parts.append(f"* [[{project}]]")

    content_parts.extend([
        "",
        "== Contact ==",
        "",
        f"* Email: {email}",
        "* Slack: @" + name.lower().replace(" ", ""),
        "",
        "[[Category:Team Members]]",
        f"[[Category:{role}]]"
    ])

    content = '\n'.join(content_parts)

    return page_manager.create_or_update_page(
        title=f'Team:{name}',
        content=content,
        summary=f"Created profile for {name}"
    )

def create_team_directory():
    """Create team directory page."""

    from scripts.category_manager import CategoryManager
    cat_manager = CategoryManager()

    # Get all team members
    team_members = cat_manager.client.get_pages_in_category('Team Members')

    # Group by role
    by_role = {}
    for member in team_members:
        # Get role from categories
        categories = cat_manager.client.get_categories(member['title'])
        roles = [c.replace('Category:', '') for c in categories
                if c != 'Category:Team Members']

        role = roles[0] if roles else 'Team Member'

        if role not in by_role:
            by_role[role] = []

        by_role[role].append(member['title'])

    # Build directory
    content_parts = [
        "= Team Directory =",
        "",
        "Complete directory of all team members.",
        "",
        "{{Team Search Box}}",
        ""
    ]

    for role in sorted(by_role.keys()):
        content_parts.extend([
            f"== {role}s ==",
            ""
        ])

        for member in sorted(by_role[role]):
            member_name = member.replace('Team:', '')
            content_parts.append(f"* [[{member}|{member_name}]]")

        content_parts.append("")

    content_parts.extend([
        "[[Category:Team]]",
        "[[Category:Directory]]"
    ])

    content = '\n'.join(content_parts)

    return page_manager.create_or_update_page(
        title='Team:Directory',
        content=content,
        summary="Updated team directory"
    )

# Usage
create_team_profile(
    name='Alice Johnson',
    role='Software Engineer',
    email='alice@company.com',
    skills=['Python', 'React', 'Docker', 'AWS'],
    current_projects=['Project:Phoenix', 'Project:Atlas'],
    bio='Alice has 8 years of experience in full-stack development...',
    photo_path='team_photos/alice.jpg'
)

create_team_directory()
print("✓ Team profiles created")
```

## Example 4: Onboarding Checklist

```python
from scripts.page_manager import PageManager

def create_onboarding_page(new_hire_name, role, start_date, buddy):
    """Create onboarding checklist for new team member."""

    page_title = f'Onboarding:{new_hire_name.replace(" ", "_")}'

    content = f"""
= Onboarding: {new_hire_name} =

{{{{Onboarding Info
|name={new_hire_name}
|role={role}
|start_date={start_date}
|buddy={buddy}
|status=In Progress
}}}}

== Welcome! ==

Welcome to the team, {new_hire_name}! This page tracks your onboarding progress.

Your onboarding buddy is [[Team:{buddy}|{buddy}]].

== Week 1: Getting Started ==

=== Day 1 ===

* [ ] Complete HR paperwork
* [ ] Get company laptop and accounts
* [ ] Set up development environment
* [ ] Meet with manager
* [ ] Team introduction

=== Day 2-3 ===

* [ ] Complete security training
* [ ] Set up all development tools
* [ ] Clone and build main repository
* [ ] Review [[Team:Coding Standards|coding standards]]
* [ ] Review [[Team:Development Workflow|development workflow]]

=== Day 4-5 ===

* [ ] Complete first small task
* [ ] Submit first pull request
* [ ] Attend team standup
* [ ] Shadow {buddy} on current work
* [ ] Schedule 1:1s with team members

== Week 2: Deep Dive ==

* [ ] Read all [[Category:Architecture|architecture documentation]]
* [ ] Complete training modules
* [ ] Take on larger task
* [ ] Present at team meeting
* [ ] Review [[Team:Best Practices|best practices]]

== Week 3-4: Ramping Up ==

* [ ] Work on feature independently
* [ ] Participate in code reviews
* [ ] Help with on-call rotation (shadowing)
* [ ] Contribute to documentation
* [ ] 30-day check-in with manager

== Resources ==

* [[Team:New Hire Guide|Complete New Hire Guide]]
* [[Development:Setup|Development Setup]]
* [[Team:Directory|Team Directory]]
* [[FAQ:Index|FAQ]]

== Feedback ==

Please share your onboarding feedback here:

<feedback form>

[[Category:Onboarding]]
[[Category:Team]]
"""

    page_manager = PageManager()
    return page_manager.create_or_update_page(
        title=page_title,
        content=content,
        summary=f"Created onboarding page for {new_hire_name}"
    )

# Usage
create_onboarding_page(
    new_hire_name='David Chen',
    role='Backend Engineer',
    start_date='2025-12-01',
    buddy='Alice Johnson'
)
print("✓ Onboarding page created")
```

## Example 5: Incident Response Documentation

```python
from scripts.page_manager import PageManager
from datetime import datetime

class IncidentManager:
    """Manage incident documentation."""

    def __init__(self):
        self.page_manager = PageManager()

    def create_incident_report(
        self,
        incident_id,
        severity,
        title,
        impact,
        timeline,
        root_cause,
        resolution,
        action_items
    ):
        """Create incident report page."""

        page_title = f'Incidents:{incident_id}'

        content = f"""
= Incident {incident_id}: {title} =

{{{{Incident Report
|id={incident_id}
|severity={severity}
|date={datetime.now().strftime('%Y-%m-%d')}
|status=Resolved
}}}}

== Summary ==

{impact}

== Severity ==

'''{severity}'''

== Timeline ==

{self._format_timeline(timeline)}

== Root Cause ==

{root_cause}

== Resolution ==

{resolution}

== Action Items ==

{self._format_action_items(action_items)}

== Lessons Learned ==

1. What went well
2. What didn't go well
3. How to prevent similar incidents

== References ==

* [[Incidents:Runbook|Incident Response Runbook]]
* [[Operations:Monitoring|Monitoring Setup]]

[[Category:Incidents]]
[[Category:Severity-{severity}]]
[[Category:Resolved]]
"""

        return self.page_manager.create_or_update_page(
            title=page_title,
            content=content,
            summary=f"Created incident report {incident_id}"
        )

    def _format_timeline(self, timeline):
        """Format timeline events."""
        result = []
        for event in timeline:
            result.append(f"* '''{event['time']}''' - {event['event']}")
        return '\n'.join(result)

    def _format_action_items(self, action_items):
        """Format action items."""
        result = []
        for item in action_items:
            result.append(
                f"* [ ] {item['task']} "
                f"(Owner: {item['owner']}, Due: {item['due']})"
            )
        return '\n'.join(result)

    def create_incident_index(self):
        """Create incident index page."""

        from scripts.category_manager import CategoryManager
        cat_manager = CategoryManager()

        # Get all incidents
        incidents = cat_manager.client.get_pages_in_category('Incidents')

        # Group by severity
        by_severity = {
            'Critical': [],
            'High': [],
            'Medium': [],
            'Low': []
        }

        for incident in incidents:
            categories = cat_manager.client.get_categories(incident['title'])

            for category in categories:
                if 'Severity-' in category:
                    severity = category.replace('Category:Severity-', '')
                    if severity in by_severity:
                        by_severity[severity].append(incident['title'])
                    break

        # Build index
        content_parts = [
            "= Incident Reports =",
            "",
            "Index of all incident reports.",
            "",
            "== Statistics ==",
            "",
            f"* Total incidents: {len(incidents)}",
            f"* Critical: {len(by_severity['Critical'])}",
            f"* High: {len(by_severity['High'])}",
            f"* Medium: {len(by_severity['Medium'])}",
            f"* Low: {len(by_severity['Low'])}",
            ""
        ]

        for severity in ['Critical', 'High', 'Medium', 'Low']:
            if by_severity[severity]:
                content_parts.extend([
                    f"== {severity} Severity ==",
                    ""
                ])

                for incident in sorted(by_severity[severity], reverse=True):
                    content_parts.append(f"* [[{incident}]]")

                content_parts.append("")

        content_parts.extend([
            "[[Category:Incidents]]",
            "[[Category:Index]]"
        ])

        content = '\n'.join(content_parts)

        return self.page_manager.create_or_update_page(
            title='Incidents:Index',
            content=content,
            summary="Updated incident index"
        )

# Usage
manager = IncidentManager()

manager.create_incident_report(
    incident_id='INC-2025-001',
    severity='High',
    title='Database Connection Pool Exhaustion',
    impact='Users experienced 503 errors for 45 minutes',
    timeline=[
        {'time': '14:30', 'event': 'Alerts triggered for high error rate'},
        {'time': '14:35', 'event': 'Incident declared'},
        {'time': '14:45', 'event': 'Root cause identified'},
        {'time': '15:00', 'event': 'Fix deployed'},
        {'time': '15:15', 'event': 'Service fully restored'}
    ],
    root_cause='Connection pool size was too small for increased traffic',
    resolution='Increased pool size from 10 to 50 connections',
    action_items=[
        {'task': 'Add monitoring for connection pool usage', 'owner': 'Alice', 'due': '2025-11-20'},
        {'task': 'Review all service pool configurations', 'owner': 'Bob', 'due': '2025-11-25'}
    ]
)

manager.create_incident_index()
print("✓ Incident documentation created")
```

## Example 6: Decision Log

```python
from scripts.page_manager import PageManager
from datetime import datetime

def log_decision(
    title,
    context,
    options_considered,
    decision,
    decision_makers,
    rationale,
    consequences
):
    """Log an architectural or technical decision."""

    page_title = f'Decisions:{datetime.now().strftime("%Y-%m-%d")}_{title.replace(" ", "_")}'

    # Format options
    options_section = ""
    for i, option in enumerate(options_considered, 1):
        options_section += f"=== Option {i}: {option['name']} ===\n\n"
        options_section += f"Pros:\n"
        for pro in option.get('pros', []):
            options_section += f"* {pro}\n"
        options_section += f"\nCons:\n"
        for con in option.get('cons', []):
            options_section += f"* {con}\n"
        options_section += "\n"

    content = f"""
= Decision: {title} =

{{{{Decision Record
|date={datetime.now().strftime('%Y-%m-%d')}
|status=Approved
|decision_makers={', '.join(decision_makers)}
}}}}

== Context ==

{context}

== Options Considered ==

{options_section}

== Decision ==

{decision}

== Rationale ==

{rationale}

== Consequences ==

=== Positive ===

{self._format_list(consequences.get('positive', []))}

=== Negative ===

{self._format_list(consequences.get('negative', []))}

=== Neutral ===

{self._format_list(consequences.get('neutral', []))}

== Decision Makers ==

{self._format_list([f"[[Team:{dm}|{dm}]]" for dm in decision_makers])}

[[Category:Decisions]]
[[Category:Architecture Decisions]]
"""

    page_manager = PageManager()
    return page_manager.create_or_update_page(
        title=page_title,
        content=content,
        summary=f"Logged decision: {title}"
    )

def _format_list(items):
    """Format list of items."""
    if not items:
        return "None"
    return '\n'.join([f"* {item}" for item in items])

# Usage
log_decision(
    title="Switch to Microservices Architecture",
    context="Our monolithic application is becoming difficult to scale and maintain.",
    options_considered=[
        {
            'name': 'Keep Monolith',
            'pros': ['Simple deployment', 'No migration needed'],
            'cons': ['Scaling issues', 'Slow deployments']
        },
        {
            'name': 'Migrate to Microservices',
            'pros': ['Better scalability', 'Independent deployments'],
            'cons': ['Increased complexity', 'Migration effort']
        }
    ],
    decision="Migrate to microservices architecture over next 6 months",
    decision_makers=['Alice Johnson', 'Bob Smith', 'CTO'],
    rationale="Benefits of scalability and team autonomy outweigh migration costs",
    consequences={
        'positive': [
            'Teams can deploy independently',
            'Better scalability',
            'Technology flexibility'
        ],
        'negative': [
            'Increased operational complexity',
            '6-month migration timeline',
            'Need for service mesh'
        ],
        'neutral': [
            'Need to train team on microservices patterns'
        ]
    }
)

print("✓ Decision logged")
```

## Best Practices for Team Wikis

### 1. Keep Content Up-to-Date

```python
# Add "last reviewed" dates
footer = f"""
---
''Last reviewed: {datetime.now().strftime('%Y-%m-%d')} by [[Team:{reviewer}]]''
"""
```

### 2. Use Templates

```python
# Create consistent page structures
MEETING_TEMPLATE = "..."
PROJECT_TEMPLATE = "..."
INCIDENT_TEMPLATE = "..."
```

### 3. Cross-Link Related Pages

```python
# Add "See Also" sections
see_also = """
== See Also ==

* [[Related Page 1]]
* [[Related Page 2]]
"""
```

### 4. Maintain Good Information Architecture

```python
# Use consistent naming:
# - Team:Name (team members)
# - Project:Name (projects)
# - Meetings:Type/Date (meeting notes)
# - Incidents:ID (incident reports)
```

### 5. Archive Old Content

```python
# Mark outdated content
archive_notice = """
{{Archived|date=2025-11-01|reason=Project completed}}
"""
```
