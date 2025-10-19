import os
import logging
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Try to import TrelloClient with fallback
try:
    from trello import TrelloClient
except ImportError:
    try:
        # Try to import from py-trello package (older version)
        from trello.client import TrelloClient
    except ImportError:
        logger.warning("Could not import TrelloClient. Using dummy implementation.")
        
        # Dummy implementation of TrelloClient
        class TrelloClient:
            def __init__(self, api_key=None, token=None):
                self.api_key = api_key
                self.token = token
                logger.info("Initialized dummy TrelloClient")
                
            def list_boards(self):
                logger.info("Dummy list_boards called")
                return []
                
            def add_board(self, name, desc=None):
                logger.info(f"Dummy add_board called with name: {name}")
                class DummyBoard:
                    def __init__(self, name, desc):
                        self.id = "dummy_board_id"
                        self.name = name
                        self.desc = desc
                return DummyBoard(name, desc)
                
            def get_list(self, list_id):
                logger.info(f"Dummy get_list called with list_id: {list_id}")
                class DummyList:
                    def __init__(self, list_id):
                        self.id = list_id
                        self.name = "Dummy List"
                        
                    def add_card(self, name, desc=None):
                        logger.info(f"Dummy add_card called with name: {name}")
                        class DummyCard:
                            def __init__(self, name, desc):
                                self.id = "dummy_card_id"
                                self.name = name
                                self.desc = desc
                        return DummyCard(name, desc)
                        
                    def list_cards(self):
                        logger.info("Dummy list_cards called")
                        return []
                        
                return DummyList(list_id)

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

# Initialize the Trello API client only if all required environment variables are present
trello = None
if all(os.getenv(env) for env in ['TRELLO_API_KEY', 'TRELLO_TOKEN']):
    try:
        trello = TrelloAPI(
            api_key=os.getenv('TRELLO_API_KEY'),
            token=os.getenv('TRELLO_TOKEN')
        )
        logger.info("Trello API client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Trello API client: {e}")
else:
    logger.warning("Trello API environment variables not set. Trello functionality will be disabled.") 