import os
from typing import Dict
from atlassian import Bitbucket
from dotenv import load_dotenv

load_dotenv()

class BitbucketAPI:
    def __init__(self, url: str, username: str, api_token: str):
        """Initialize Bitbucket connection."""
        self.bitbucket = Bitbucket(
            url=url,
            username=username,
            password=api_token
        )

    def create_repo(self, project_key: str, repo_name: str, 
                   is_private: bool = True) -> Dict:
        """Create a new repository."""
        return self.bitbucket.create_repo(
            project_key,
            repo_name,
            is_private=is_private
        )

    def get_repo(self, project_key: str, repo_slug: str) -> Dict:
        """Get repository details."""
        return self.bitbucket.get_repo(project_key, repo_slug)

    def create_pull_request(self, project_key: str, repo_slug: str,
                          title: str, source_branch: str, 
                          target_branch: str = 'main') -> Dict:
        """Create a pull request."""
        return self.bitbucket.create_pull_request(
            project_key,
            repo_slug,
            title,
            source_branch,
            target_branch
        )

# Initialize the Bitbucket API client if credentials are available
bitbucket = None
if all(os.getenv(env) for env in ['BITBUCKET_URL', 'BITBUCKET_USERNAME', 'BITBUCKET_API_TOKEN']):
    bitbucket = BitbucketAPI(
        url=os.getenv('BITBUCKET_URL'),
        username=os.getenv('BITBUCKET_USERNAME'),
        api_token=os.getenv('BITBUCKET_API_TOKEN')
    ) 