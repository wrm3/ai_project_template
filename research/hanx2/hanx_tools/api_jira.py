import os
from typing import Dict, List, Optional
from atlassian import Jira
from dotenv import load_dotenv

load_dotenv()

class JiraAPI:
    def __init__(self, url: str, username: str, api_token: str):
        """Initialize Jira connection."""
        self.jira = Jira(
            url=url,
            username=username,
            password=api_token
        )

    def create_issue(self, project: str, summary: str, description: str, 
                    issue_type: str = 'Task') -> Dict:
        """Create a new Jira issue."""
        return self.jira.issue_create({
            'project': {'key': project},
            'summary': summary,
            'description': description,
            'issuetype': {'name': issue_type}
        })

    def get_issue(self, issue_key: str) -> Dict:
        """Get issue details by key."""
        return self.jira.issue(issue_key)

    def search_issues(self, jql: str) -> List[Dict]:
        """Search issues using JQL."""
        return self.jira.jql(jql)

# Initialize the Jira API client only if all required environment variables are present
jira = None
if all(os.getenv(env) for env in ['JIRA_URL', 'JIRA_USERNAME', 'JIRA_API_TOKEN']):
    jira = JiraAPI(
        url=os.getenv('JIRA_URL'),
        username=os.getenv('JIRA_USERNAME'),
        api_token=os.getenv('JIRA_API_TOKEN')
    ) 