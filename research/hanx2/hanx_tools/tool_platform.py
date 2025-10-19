"""
Platform tools module that imports and re-exports the individual platform API clients.
This module serves as a compatibility layer for existing code that imports from platform_tools.
"""

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import from atlassian with fallbacks
try:
    from atlassian import jira, JiraAPI
    from atlassian import confluence, ConfluenceAPI
    from atlassian import bitbucket, BitbucketAPI
    from atlassian import trello, TrelloAPI
except ImportError:
    logger.warning("Could not import from atlassian package. Using dummy implementations.")
    
    # Dummy implementations
    class JiraAPI:
        def __init__(self, url=None, username=None, password=None, token=None):
            self.url = url
            self.username = username
            self.token = token
            logger.info("Initialized dummy JiraAPI")
            
        def issue_create(self, fields):
            logger.info(f"Dummy issue_create called with fields: {fields}")
            return {"id": "DUMMY-123", "key": "DUMMY-123"}
            
        def issue_update(self, issue_key, fields):
            logger.info(f"Dummy issue_update called for {issue_key} with fields: {fields}")
            return True
            
        def issue_get(self, issue_key):
            logger.info(f"Dummy issue_get called for {issue_key}")
            return {"id": issue_key, "key": issue_key, "fields": {}}
    
    class ConfluenceAPI:
        def __init__(self, url=None, username=None, password=None, token=None):
            self.url = url
            self.username = username
            self.token = token
            logger.info("Initialized dummy ConfluenceAPI")
            
        def create_page(self, space, title, body, parent_id=None):
            logger.info(f"Dummy create_page called for {title} in {space}")
            return {"id": "12345", "title": title}
            
        def update_page(self, page_id, title, body):
            logger.info(f"Dummy update_page called for {page_id}")
            return {"id": page_id, "title": title}
            
        def get_page_by_title(self, space, title):
            logger.info(f"Dummy get_page_by_title called for {title} in {space}")
            return {"id": "12345", "title": title}
    
    class BitbucketAPI:
        def __init__(self, url=None, username=None, password=None, token=None):
            self.url = url
            self.username = username
            self.token = token
            logger.info("Initialized dummy BitbucketAPI")
            
        def create_repository(self, project_key, repository, **kwargs):
            logger.info(f"Dummy create_repository called for {repository} in {project_key}")
            return {"slug": repository, "name": repository}
            
        def get_branches(self, project_key, repository, **kwargs):
            logger.info(f"Dummy get_branches called for {repository} in {project_key}")
            return {"values": [{"displayId": "main", "id": "refs/heads/main"}]}
    
    class TrelloAPI:
        def __init__(self, api_key=None, token=None):
            self.api_key = api_key
            self.token = token
            logger.info("Initialized dummy TrelloAPI")
            
        def get_boards(self):
            logger.info("Dummy get_boards called")
            return []
    
    # Dummy module objects
    jira = JiraAPI()
    confluence = ConfluenceAPI()
    bitbucket = BitbucketAPI()
    trello = TrelloAPI()

# Re-export the classes and instances for backward compatibility
__all__ = [
    'JiraAPI', 'jira',
    'ConfluenceAPI', 'confluence',
    'BitbucketAPI', 'bitbucket',
    'TrelloAPI', 'trello'
] 