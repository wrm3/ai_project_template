"""
Tests for the OpenManus integration module.
"""

import unittest
from unittest.mock import MagicMock, patch

from ..openmanus import integration


class TestOpenManusIntegration(unittest.TestCase):
    """Test cases for the OpenManusIntegration class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Reset the singleton instance before each test
        integration._instance = None
    
    def test_singleton_pattern(self):
        """Test that the integration manager follows the singleton pattern."""
        instance1 = integration.get_integration()
        instance2 = integration.get_integration()
        self.assertIs(instance1, instance2)
    
    def test_list_tools(self):
        """Test that list_tools returns a list of tool names."""
        with patch.object(integration.OpenManusIntegration, 'list_tools', return_value=['tool1', 'tool2']):
            tools = integration.list_tools()
            self.assertEqual(tools, ['tool1', 'tool2'])
    
    @patch('hanx_tools.openmanus.integration.OpenManusIntegration.register_with_mcp_server')
    def test_register_with_mcp_server(self, mock_register):
        """Test that register_with_mcp_server calls the integration manager."""
        mock_server = MagicMock()
        integration.register_with_mcp_server(mock_server)
        mock_register.assert_called_once_with(mock_server)
    
    @patch('hanx_tools.openmanus.integration.OpenManusIntegration.register_with_cursorrules')
    def test_register_with_cursorrules(self, mock_register):
        """Test that register_with_cursorrules calls the integration manager."""
        mock_globals = {}
        integration.register_with_cursorrules(mock_globals)
        mock_register.assert_called_once_with(mock_globals)


if __name__ == '__main__':
    unittest.main() 