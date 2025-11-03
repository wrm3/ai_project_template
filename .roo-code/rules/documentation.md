# Documentation Rules (Roo-Code)

For complete documentation standards, see: `.claude/rules/documentation.md`

## Quick Reference

### Code Documentation
```python
def authenticate_user(username: str, password: str) -> User | None:
    """
    Authenticate user with username and password.

    Args:
        username: User's username
        password: Plain text password

    Returns:
        User object if authentication successful, None otherwise

    Raises:
        ValueError: If username or password empty

    Example:
        >>> user = authenticate_user("john", "secret")
        >>> print(user.email)
        john@example.com
    """
```

### README Structure
```markdown
# Project Name

Brief description (1-2 sentences)

## Features
- Feature 1
- Feature 2

## Installation
Step-by-step instructions...

## Usage
Example code...

## Documentation
Link to full docs...
```

### API Documentation
```markdown
## POST /api/auth/login

Authenticate user and return JWT token.

**Request:**
```json
{
  "username": "john",
  "password": "secret"
}
```

**Response (200):**
```json
{
  "token": "eyJhbG...",
  "user": {...}
}
```

**Errors:**
- 401: Invalid credentials
- 429: Too many attempts
```

### Documentation Types
- **Inline Comments:** Explain WHY, not WHAT
- **Function Docs:** Parameters, returns, errors
- **README:** Setup and usage
- **API Docs:** Endpoints and examples
- **Architecture:** System design

For complete documentation rules, see `.claude/rules/documentation.md`
