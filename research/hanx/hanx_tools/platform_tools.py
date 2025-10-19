"""
Platform tools module that imports and re-exports the individual platform API clients.
This module serves as a compatibility layer for existing code that imports from platform_tools.
"""

from tools.jira_api import jira, JiraAPI
from tools.confluence_api import confluence, ConfluenceAPI
from tools.bitbucket_api import bitbucket, BitbucketAPI
from tools.trello_api import trello, TrelloAPI

# Re-export the classes and instances for backward compatibility
__all__ = [
    'JiraAPI', 'jira',
    'ConfluenceAPI', 'confluence',
    'BitbucketAPI', 'bitbucket',
    'TrelloAPI', 'trello'
] 