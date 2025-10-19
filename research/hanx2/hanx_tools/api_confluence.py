import os
from typing import Dict, List, Optional
from atlassian import Confluence
from dotenv import load_dotenv

load_dotenv()

class ConfluenceAPI:
    def __init__(self, url: str, username: str, api_token: str):
        """Initialize Confluence connection."""
        self.confluence = Confluence(
            url=url,
            username=username,
            password=api_token
        )

    def create_page(self, space: str, title: str, body: str, 
                   parent_id: Optional[str] = None) -> Dict:
        """Create a new Confluence page."""
        return self.confluence.create_page(
            space=space,
            title=title,
            body=body,
            parent_id=parent_id
        )

    def get_page(self, page_id: str) -> Dict:
        """Get page content by ID."""
        return self.confluence.get_page_by_id(page_id)

    def search_content(self, query: str, space: Optional[str] = None) -> List[Dict]:
        """Search Confluence content."""
        return self.confluence.cql(f'text ~ "{query}"' + 
                                 (f' AND space = "{space}"' if space else ''))

# Initialize the Confluence API client only if all required environment variables are present
confluence = None
if all(os.getenv(env) for env in ['JIRA_URL', 'JIRA_USERNAME', 'JIRA_API_TOKEN']):
    confluence = ConfluenceAPI(
        url=os.getenv('JIRA_URL'),  # Usually same as Jira URL
        username=os.getenv('JIRA_USERNAME'),
        api_token=os.getenv('JIRA_API_TOKEN')
    ) 