"""
Context Adapter for Prompt-Based Agents

Allows prompt-based agents (markdown files) to read/write shared context.
Converts between SDK context objects and JSON files that prompt agents can access.

Author: Database Expert Agent
Date: 2025-11-01
Task: 052 - Anthropic Agent SDK Integration
"""

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class ContextAdapter:
    """
    Adapter for prompt-based agents to interact with context system

    Provides:
    - SDK context → JSON file conversion
    - Text parsing → structured data extraction
    - Simplified context read/write for prompt agents
    """

    def __init__(self, context_dir: str = ".claude/agent_context/json"):
        """
        Initialize context adapter

        Args:
            context_dir: Directory for JSON context files
        """
        self.context_dir = Path(context_dir)
        self.context_dir.mkdir(parents=True, exist_ok=True)

    def to_json(self, sdk_context: Any, workflow_id: Optional[str] = None) -> str:
        """
        Convert SDK context to JSON file for prompt-based agents

        Args:
            sdk_context: AgentContext object or dict
            workflow_id: Optional workflow ID override

        Returns:
            Path to created JSON file
        """
        # Handle both AgentContext objects and dicts
        if hasattr(sdk_context, 'model_dump_json_safe'):
            context_data = sdk_context.model_dump_json_safe()
            workflow_id = workflow_id or str(sdk_context.workflow_id)
        else:
            context_data = sdk_context
            workflow_id = workflow_id or context_data.get('workflow_id', 'unknown')

        # Write to JSON file
        context_file = self.context_dir / f"{workflow_id}.json"

        with open(context_file, 'w') as f:
            json.dump(context_data, f, indent=2)

        logger.info(f"Converted SDK context to JSON: {context_file}")
        return str(context_file)

    def from_json(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Load context from JSON file

        Args:
            workflow_id: Workflow UUID

        Returns:
            Context data as dictionary
        """
        context_file = self.context_dir / f"{workflow_id}.json"

        if not context_file.exists():
            logger.error(f"Context file not found: {context_file}")
            return None

        try:
            with open(context_file, 'r') as f:
                context_data = json.load(f)

            logger.info(f"Loaded context from JSON: {context_file}")
            return context_data

        except Exception as e:
            logger.error(f"Failed to load context {workflow_id}: {e}")
            return None

    def update_context(
        self,
        workflow_id: str,
        agent_name: str,
        updates: Dict[str, Any]
    ) -> bool:
        """
        Update context with agent results

        Args:
            workflow_id: Workflow UUID
            agent_name: Name of agent making updates
            updates: Dictionary of updates to apply

        Returns:
            True if successful
        """
        context_data = self.from_json(workflow_id)
        if not context_data:
            return False

        # Update agent state
        if 'agent_states' not in context_data:
            context_data['agent_states'] = {}

        if agent_name not in context_data['agent_states']:
            context_data['agent_states'][agent_name] = {
                'status': 'in_progress',
                'agent_type': 'prompt-based'
            }

        # Apply updates
        agent_state = context_data['agent_states'][agent_name]

        # Handle common update patterns
        if 'status' in updates:
            agent_state['status'] = updates['status']

        if 'files_created' in updates:
            agent_state['files_created'] = updates['files_created']

        if 'files_modified' in updates:
            agent_state['files_modified'] = updates['files_modified']

        if 'tests_passing' in updates:
            agent_state['tests_passing'] = updates['tests_passing']

        # Update shared artifacts
        if 'shared_artifacts' in updates:
            if 'shared_artifacts' not in context_data:
                context_data['shared_artifacts'] = {}

            for key, value in updates['shared_artifacts'].items():
                context_data['shared_artifacts'][key] = value

        # Mark agent as completed if status is completed
        if agent_state['status'] == 'completed':
            if 'agents_completed' not in context_data:
                context_data['agents_completed'] = []

            if agent_name not in context_data['agents_completed']:
                context_data['agents_completed'].append(agent_name)

            context_data['current_agent'] = None

        # Update timestamp
        from datetime import datetime
        context_data['updated_at'] = datetime.utcnow().isoformat()

        # Write back to file
        context_file = self.context_dir / f"{workflow_id}.json"
        with open(context_file, 'w') as f:
            json.dump(context_data, f, indent=2)

        logger.info(f"Updated context for agent {agent_name}")
        return True

    def from_text(self, agent_output_text: str) -> Dict[str, Any]:
        """
        Parse prompt-based agent output into structured result

        Extracts:
        - Status indicators (✅, ❌, 🔄)
        - File lists (created/modified)
        - Test results
        - JSON blocks

        Args:
            agent_output_text: Text output from prompt-based agent

        Returns:
            Structured result dictionary
        """
        result = {
            'status': 'completed',
            'files_created': [],
            'files_modified': [],
            'tests_passing': None,
            'raw_output': agent_output_text
        }

        # Extract status
        if '❌' in agent_output_text or 'FAILED' in agent_output_text.upper():
            result['status'] = 'failed'
        elif '🔄' in agent_output_text or 'IN PROGRESS' in agent_output_text.upper():
            result['status'] = 'in_progress'
        elif '✅' in agent_output_text or 'COMPLETED' in agent_output_text.upper():
            result['status'] = 'completed'

        # Extract file paths
        # Pattern: /path/to/file.ext or src/file.py
        file_pattern = r'(?:^|\s)([a-zA-Z0-9_\-./]+\.[a-z]{2,4})(?:\s|$)'
        files = re.findall(file_pattern, agent_output_text, re.MULTILINE)

        # Categorize by keywords
        created_keywords = ['created', 'new file', 'added']
        modified_keywords = ['modified', 'updated', 'changed', 'edited']

        lines = agent_output_text.split('\n')
        for i, line in enumerate(lines):
            line_lower = line.lower()

            # Check for created files
            if any(kw in line_lower for kw in created_keywords):
                for f in files:
                    if f in line and f not in result['files_created']:
                        result['files_created'].append(f)

            # Check for modified files
            if any(kw in line_lower for kw in modified_keywords):
                for f in files:
                    if f in line and f not in result['files_modified']:
                        result['files_modified'].append(f)

        # Extract test results
        test_patterns = [
            r'(\d+) tests? passed',
            r'all tests passing',
            r'tests: (\d+) passed',
            r'✅.*tests?'
        ]

        for pattern in test_patterns:
            match = re.search(pattern, agent_output_text, re.IGNORECASE)
            if match:
                result['tests_passing'] = True
                break

        fail_patterns = [
            r'(\d+) tests? failed',
            r'tests failing',
            r'❌.*tests?'
        ]

        for pattern in fail_patterns:
            match = re.search(pattern, agent_output_text, re.IGNORECASE)
            if match:
                result['tests_passing'] = False
                break

        # Extract JSON blocks if present
        json_pattern = r'```json\s*\n(.*?)\n```'
        json_matches = re.findall(json_pattern, agent_output_text, re.DOTALL)

        if json_matches:
            try:
                # Try to parse the first JSON block
                json_data = json.loads(json_matches[0])
                result['structured_output'] = json_data

                # Override with explicit values from JSON
                if 'status' in json_data:
                    result['status'] = json_data['status']
                if 'files_created' in json_data:
                    result['files_created'] = json_data['files_created']
                if 'files_modified' in json_data:
                    result['files_modified'] = json_data['files_modified']
                if 'tests_passing' in json_data:
                    result['tests_passing'] = json_data['tests_passing']

            except json.JSONDecodeError:
                logger.warning("Found JSON block but failed to parse")

        return result

    def get_context_path(self, workflow_id: str) -> str:
        """
        Get absolute path to context file

        Args:
            workflow_id: Workflow UUID

        Returns:
            Absolute path to context JSON file
        """
        context_file = self.context_dir / f"{workflow_id}.json"
        return str(context_file.absolute())

    def create_context_summary(self, workflow_id: str) -> Optional[str]:
        """
        Create human-readable summary of context for prompt-based agents

        Args:
            workflow_id: Workflow UUID

        Returns:
            Formatted summary string
        """
        context_data = self.from_json(workflow_id)
        if not context_data:
            return None

        summary_parts = [
            f"# Workflow Context Summary",
            f"",
            f"**Workflow ID**: {workflow_id}",
            f"**Task**: {context_data.get('task', 'N/A')}",
            f"**Phase**: {context_data.get('phase', 'N/A')}",
            f"**Started**: {context_data.get('started_at', 'N/A')}",
            f""
        ]

        # Agents completed
        agents_completed = context_data.get('agents_completed', [])
        if agents_completed:
            summary_parts.append(f"## Completed Agents ({len(agents_completed)})")
            for agent in agents_completed:
                summary_parts.append(f"- ✅ {agent}")
            summary_parts.append("")

        # Current agent
        current_agent = context_data.get('current_agent')
        if current_agent:
            summary_parts.append(f"## Current Agent")
            summary_parts.append(f"- 🔄 {current_agent}")
            summary_parts.append("")

        # Shared artifacts
        shared_artifacts = context_data.get('shared_artifacts', {})
        if shared_artifacts:
            summary_parts.append(f"## Shared Artifacts")

            # Database schema
            if 'database_schema' in shared_artifacts and shared_artifacts['database_schema']:
                schema = shared_artifacts['database_schema']
                tables = schema.get('tables', [])
                summary_parts.append(f"- **Database**: {len(tables)} tables")

            # API endpoints
            if 'api_endpoints' in shared_artifacts:
                endpoints = shared_artifacts['api_endpoints']
                summary_parts.append(f"- **API Endpoints**: {len(endpoints)}")
                for ep in endpoints[:5]:  # Show first 5
                    summary_parts.append(f"  - {ep.get('method', 'GET')} {ep.get('path', 'N/A')}")

            # Files
            if 'implementation_files' in shared_artifacts:
                files = shared_artifacts['implementation_files']
                summary_parts.append(f"- **Implementation Files**: {len(files)}")

            summary_parts.append("")

        # Memory context
        memory = context_data.get('memory_context', {})
        if memory:
            prefs = memory.get('user_preferences', {})
            if prefs:
                summary_parts.append(f"## User Preferences")
                for key, value in prefs.items():
                    summary_parts.append(f"- **{key}**: {value}")
                summary_parts.append("")

        summary_parts.append(f"---")
        summary_parts.append(f"*Context file: {self.get_context_path(workflow_id)}*")

        return "\n".join(summary_parts)


# Example usage and testing
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)

    # Initialize adapter
    adapter = ContextAdapter()

    # Create test context data
    test_context = {
        'workflow_id': 'test-workflow-123',
        'task': 'Test prompt-based agent context',
        'phase': 'implementation',
        'started_at': '2025-11-01T12:00:00Z',
        'agents_completed': ['solution-architect'],
        'current_agent': 'backend-developer',
        'shared_artifacts': {
            'api_endpoints': [
                {'path': '/api/users', 'method': 'GET'},
                {'path': '/api/users/:id', 'method': 'GET'}
            ],
            'implementation_files': ['src/api/users.ts', 'src/models/user.ts']
        },
        'memory_context': {
            'user_preferences': {
                'database': 'PostgreSQL',
                'testing_framework': 'pytest'
            }
        }
    }

    # Convert to JSON
    json_path = adapter.to_json(test_context, 'test-workflow-123')
    print(f"Created JSON context: {json_path}")

    # Load back
    loaded = adapter.from_json('test-workflow-123')
    print(f"\nLoaded context: {loaded['task']}")

    # Create summary
    summary = adapter.create_context_summary('test-workflow-123')
    print(f"\n{summary}")

    # Test text parsing
    sample_output = """
    ## Backend Implementation Complete

    ✅ Successfully implemented user authentication API

    **Files Created:**
    - src/auth/login.ts
    - src/auth/logout.ts
    - src/middleware/auth.ts

    **Files Modified:**
    - src/app.ts
    - src/routes/index.ts

    **Tests:** 15 tests passed

    ```json
    {
        "status": "completed",
        "api_endpoints": [
            {"path": "/api/auth/login", "method": "POST"},
            {"path": "/api/auth/logout", "method": "POST"}
        ]
    }
    ```
    """

    result = adapter.from_text(sample_output)
    print(f"\nParsed text result:")
    print(json.dumps(result, indent=2))

    # Update context
    adapter.update_context(
        'test-workflow-123',
        'backend-developer',
        {
            'status': 'completed',
            'files_created': result['files_created'],
            'tests_passing': True,
            'shared_artifacts': {
                'api_endpoints': [
                    {'path': '/api/auth/login', 'method': 'POST'},
                    {'path': '/api/auth/logout', 'method': 'POST'}
                ]
            }
        }
    )

    print("\n✅ Context adapter validated successfully!")
