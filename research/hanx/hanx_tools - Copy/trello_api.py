import os
from typing import Dict, List, Optional
from trello import TrelloClient
from dotenv import load_dotenv

load_dotenv()

class TrelloAPI:
    def __init__(self, api_key: str, token: str):
        """Initialize Trello connection."""
        self.client = TrelloClient(
            api_key=api_key,
            token=token
        )

    def get_boards(self) -> List[Dict]:
        """Get all boards."""
        return [{'id': board.id, 'name': board.name} 
                for board in self.client.list_boards()]

    def create_board(self, name: str, description: Optional[str] = None) -> Dict:
        """Create a new board."""
        board = self.client.add_board(name, desc=description)
        return {'id': board.id, 'name': board.name}

    def create_card(self, list_id: str, name: str, 
                   description: Optional[str] = None) -> Dict:
        """Create a new card in a list."""
        trello_list = self.client.get_list(list_id)
        card = trello_list.add_card(name=name, desc=description)
        return {'id': card.id, 'name': card.name}

    def get_cards(self, list_id: str) -> List[Dict]:
        """Get all cards in a list."""
        trello_list = self.client.get_list(list_id)
        return [{'id': card.id, 'name': card.name} 
                for card in trello_list.list_cards()]

# Initialize the Trello API client if credentials are available
trello = None
if all(os.getenv(env) for env in ['TRELLO_API_KEY', 'TRELLO_TOKEN']):
    trello = TrelloAPI(
        api_key=os.getenv('TRELLO_API_KEY'),
        token=os.getenv('TRELLO_TOKEN')
    ) 