# Creating a Claude Code Plugin to Bundle MCPs & Skills

## 🎯 What You Can Do

Create a **plugin** that bundles:
- ✅ Skills (your custom capabilities)
- ✅ MCP Servers (database connections, APIs)
- ✅ Agents (specialized subagents)
- ✅ Commands (custom slash commands)
- ✅ Hooks (event handlers)

Store it in a **Git repository** and install with **one command**!

---

## 📦 Plugin Structure

```
my-development-toolkit/           # Your Git repository
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest (REQUIRED)
├── skills/                       # Your custom skills
│   ├── mysql-patterns/
│   │   └── SKILL.md
│   ├── oracle-patterns/
│   │   └── SKILL.md
│   └── api-testing/
│       └── SKILL.md
├── agents/                       # Your custom agents
│   ├── database-expert.md
│   └── api-tester.md
├── commands/                     # Your custom commands
│   ├── db-query.md
│   └── api-test.md
├── .mcp.json                     # MCP server definitions
└── README.md                     # Documentation
```

---

## 📄 Complete Example: Database Toolkit Plugin

### **1. Plugin Manifest** (`.claude-plugin/plugin.json`)

```json
{
  "name": "my-db-toolkit",
  "version": "1.0.0",
  "description": "Database development toolkit with MySQL/Oracle skills and MCP connections",
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com"
  },
  "keywords": ["database", "mysql", "oracle", "sql"],
  "license": "MIT"
}
```

### **2. MCP Server Configuration** (`.mcp.json`)

```json
{
  "$schema": "https://github.com/modelcontextprotocol/servers/blob/main/schema.json",
  "mcpServers": {
    "mysql": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-mysql"],
      "env": {
        "MYSQL_CONNECTION_STRING": "${MYSQL_URL}"
      }
    },
    "oracle": {
      "command": "npx",
      "args": ["-y", "@your-org/mcp-oracle"],
      "env": {
        "ORACLE_CONNECTION_STRING": "${ORACLE_URL}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${POSTGRES_URL}"
      }
    }
  }
}
```

**Note:** Users will need to set environment variables for credentials!

### **3. Database Skills** (`skills/mysql-patterns/SKILL.md`)

```markdown
---
name: MySQL Query Patterns
description: Apply company MySQL query conventions and performance best practices. Use when writing or optimizing MySQL queries.
---

# MySQL Query Patterns

## Our Schema Conventions
- Tables use snake_case naming
- Primary keys are always `id` (bigint, auto-increment)
- Foreign keys follow pattern `{table}_id`
- Timestamps: `created_at`, `updated_at` (always UTC)
- Soft deletes: `deleted_at` (nullable timestamp)

## Performance Best Practices
1. **Always use indexes** on foreign keys and frequently queried columns
2. **Limit result sets** to 1000 rows by default
3. **Use EXPLAIN** to verify query plans before production
4. **Avoid SELECT \*** - specify columns explicitly
5. **Use prepared statements** for all queries with user input

## Common Query Patterns

### Active Records Only
```sql
-- Always filter out soft-deleted records
SELECT * FROM users 
WHERE deleted_at IS NULL 
  AND active = 1;
```

### Pagination
```sql
-- Use LIMIT with OFFSET for pagination
SELECT id, name, email 
FROM users 
WHERE deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 50 OFFSET 0;
```

### Joins with Performance
```sql
-- Join pattern with proper indexing
SELECT 
  o.id,
  o.order_date,
  u.name as customer_name
FROM orders o
INNER JOIN users u ON o.user_id = u.id
WHERE o.deleted_at IS NULL
  AND u.deleted_at IS NULL
  AND o.created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
ORDER BY o.created_at DESC;
```

## Query Review Checklist
- [ ] Uses prepared statements or parameterized queries
- [ ] Filters out soft-deleted records
- [ ] Has appropriate indexes
- [ ] Limits result set size
- [ ] Handles NULL values properly
- [ ] Uses explicit column names (no SELECT *)
```

### **4. Database Agent** (`agents/database-expert.md`)

```markdown
---
name: database-expert
description: Expert database developer for MySQL and Oracle. Use when working with database schemas, queries, or optimizations.
tools: Read, Edit, Write, Grep, Bash
---

# Database Expert Agent

## Expertise
- MySQL and Oracle database design
- Query optimization and performance tuning
- Schema migrations and versioning
- Index strategy and analysis
- Stored procedures and functions
- Transaction management

## Responsibilities
1. **Schema Design**
   - Design normalized table structures
   - Create appropriate indexes
   - Define foreign key relationships
   - Plan for scalability

2. **Query Optimization**
   - Analyze query execution plans
   - Suggest index improvements
   - Refactor slow queries
   - Implement caching strategies

3. **Best Practices**
   - Follow company database conventions
   - Use prepared statements
   - Implement proper error handling
   - Document complex queries

## When to Use
- Designing new database schemas
- Optimizing slow queries
- Debugging database issues
- Writing complex SQL queries
- Planning data migrations
```

### **5. Custom Command** (`commands/db-schema.md`)

```markdown
---
description: Generate database schema documentation for the current project
---

# Database Schema Documentation Command

Please analyze the database schema in this project and create comprehensive documentation including:

1. **Tables Overview**
   - List all tables with descriptions
   - Row count estimates where available

2. **Schema Details** (for each table)
   - Column names and types
   - Primary keys
   - Foreign keys and relationships
   - Indexes
   - Constraints

3. **Entity Relationship Diagram**
   - Use Mermaid syntax to create an ERD
   - Show table relationships

4. **Common Queries**
   - Document frequently used query patterns
   - Include examples with this schema

5. **Migration History**
   - List applied migrations
   - Note any pending migrations

Save the documentation as `docs/database-schema.md`.
```

---

## 🚀 Publishing Your Plugin

### **Option 1: Simple Git Repository** (Recommended)

1. **Create Git Repository**
   ```bash
   mkdir my-db-toolkit
   cd my-db-toolkit
   git init
   
   # Create structure
   mkdir -p .claude-plugin skills agents commands
   
   # Add files (shown above)
   # ... create plugin.json, .mcp.json, skills, etc.
   
   git add .
   git commit -m "Initial plugin setup"
   ```

2. **Push to GitHub/GitLab**
   ```bash
   git remote add origin https://github.com/your-username/my-db-toolkit.git
   git push -u origin main
   ```

3. **Install Directly from Git**
   ```bash
   # In Claude Code:
   /plugin marketplace add your-username/my-db-toolkit
   /plugin install my-db-toolkit@your-username
   ```

### **Option 2: Create a Marketplace** (For Multiple Plugins)

Create a separate marketplace repository:

```
my-plugin-marketplace/           # Marketplace repo
├── .claude-plugin/
│   └── marketplace.json
└── README.md
```

**`marketplace.json`:**
```json
{
  "name": "my-toolkit-marketplace",
  "description": "My personal development tools and patterns",
  "owner": {
    "name": "Your Name",
    "email": "your.email@example.com"
  },
  "plugins": [
    {
      "name": "my-db-toolkit",
      "description": "Database development toolkit with MySQL/Oracle skills",
      "source": {
        "type": "github",
        "repo": "your-username/my-db-toolkit"
      },
      "version": "1.0.0"
    },
    {
      "name": "my-api-toolkit",
      "description": "API testing and development tools",
      "source": {
        "type": "github",
        "repo": "your-username/my-api-toolkit"
      },
      "version": "1.0.0"
    }
  ]
}
```

Then users install:
```bash
/plugin marketplace add your-username/my-plugin-marketplace
/plugin install my-db-toolkit@my-toolkit-marketplace
```

---

## 🏢 Team Auto-Install Setup

### **Repository-Level Configuration**

For teams to automatically get your plugins when they clone the project:

**`.claude/settings.json`** (in your project repo):
```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "type": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  },
  "plugins": {
    "my-db-toolkit@company-tools": "enabled",
    "my-api-toolkit@company-tools": "enabled"
  }
}
```

**How it works:**
1. Team member clones the project
2. Opens in Claude Code
3. Claude Code prompts: "This repository wants to install plugins. Trust it?"
4. User clicks "Trust"
5. **Plugins auto-install!** 🎉

---

## 📋 Plugin Development Workflow

### **1. Local Development**

```bash
# Create local test marketplace
mkdir test-marketplace
cd test-marketplace

# Create marketplace structure
mkdir -p .claude-plugin
cat > .claude-plugin/marketplace.json << 'EOF'
{
  "name": "test-marketplace",
  "owner": {
    "name": "Test"
  },
  "plugins": [
    {
      "name": "my-db-toolkit",
      "source": "../my-db-toolkit",
      "description": "Testing local plugin"
    }
  ]
}
EOF
```

### **2. Test Locally**

```bash
# In Claude Code:
/plugin marketplace add ./test-marketplace
/plugin install my-db-toolkit@test-marketplace

# Restart Claude Code
# Test your plugin
/db-schema
# Or just ask: "Help me optimize this MySQL query"
```

### **3. Iterate**

```bash
# Make changes to your plugin
cd ../my-db-toolkit
# ... edit files ...

# In Claude Code:
/plugin uninstall my-db-toolkit
/plugin install my-db-toolkit@test-marketplace
# Restart and test again
```

### **4. Validate Before Publishing**

```bash
# In Claude Code:
/plugin validate my-db-toolkit
```

---

## 🔐 Security Best Practices

### **For MCP Credentials**
```json
{
  "mcpServers": {
    "mysql": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-mysql"],
      "env": {
        // ❌ NEVER hardcode credentials
        // "MYSQL_CONNECTION_STRING": "mysql://user:pass@host/db"
        
        // ✅ Use environment variables
        "MYSQL_CONNECTION_STRING": "${MYSQL_URL}"
      }
    }
  }
}
```

### **Environment Variables Setup**

Tell users to set up environment variables:

**In `~/.bashrc` or `~/.zshrc`:**
```bash
export MYSQL_URL="mysql://user:pass@localhost/mydb"
export ORACLE_URL="oracle://user:pass@host:1521/service"
export POSTGRES_URL="postgresql://user:pass@localhost/mydb"
```

Or use `.env` file in project (but `.gitignore` it!):
```bash
# .env
MYSQL_URL=mysql://user:pass@localhost/mydb
ORACLE_URL=oracle://user:pass@host:1521/service
```

---

## 📦 Complete Plugin Repository Structure

```
my-db-toolkit/                    # Git repository root
├── .claude-plugin/
│   └── plugin.json              # Plugin metadata
├── .mcp.json                     # MCP server definitions
├── skills/                       # Skills directory
│   ├── mysql-patterns/
│   │   ├── SKILL.md
│   │   └── example-queries.sql  # Optional supporting files
│   ├── oracle-patterns/
│   │   └── SKILL.md
│   └── performance-tuning/
│       ├── SKILL.md
│       └── scripts/
│           └── analyze-query.sh
├── agents/                       # Agents directory
│   ├── database-expert.md
│   ├── query-optimizer.md
│   └── migration-helper.md
├── commands/                     # Commands directory
│   ├── db-schema.md
│   ├── analyze-query.md
│   └── generate-migration.md
├── hooks/                        # Hooks directory (optional)
│   └── hooks.json
├── .gitignore
├── README.md
└── LICENSE
```

**`.gitignore`:**
```gitignore
# Never commit these
.env
.env.local
*.env

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
```

**`README.md`:**
```markdown
# My Database Toolkit Plugin

Database development toolkit for Claude Code with MySQL/Oracle support.

## Installation

```bash
/plugin marketplace add your-username/my-db-toolkit
/plugin install my-db-toolkit@your-username
```

## Setup

Set environment variables for database connections:

```bash
export MYSQL_URL="mysql://user:pass@localhost/mydb"
export ORACLE_URL="oracle://user:pass@host:1521/service"
```

## What's Included

- **Skills**: MySQL patterns, Oracle patterns, Performance tuning
- **Agents**: Database expert, Query optimizer, Migration helper
- **Commands**: /db-schema, /analyze-query, /generate-migration
- **MCPs**: MySQL, Oracle, PostgreSQL connections

## Usage

Just start working with databases and Claude will use the appropriate skills automatically!

Or explicitly use commands:
- `/db-schema` - Generate database documentation
- `/analyze-query` - Optimize a SQL query
```

---

## 🎓 Example Use Cases

### **Use Case 1: Personal Toolkit**
Package all your preferred MCPs, skills, and patterns into one plugin:
- Your coding style preferences
- Your database conventions
- Your API testing patterns
- Your deployment scripts

### **Use Case 2: Team Standardization**
Create an organization plugin with:
- Company coding standards
- Internal API skills
- Database schema conventions
- Security review patterns

### **Use Case 3: Framework Support**
Build a plugin for a specific framework:
- Laravel development patterns
- Next.js best practices
- Django conventions
- Rails workflows

---

## 🔄 Plugin Updates

### **Versioning**

```json
{
  "name": "my-db-toolkit",
  "version": "1.1.0",  // Update this
  "description": "..."
}
```

### **Changelog**

Keep a `CHANGELOG.md`:
```markdown
# Changelog

## [1.1.0] - 2025-10-20
### Added
- PostgreSQL skill
- Query performance analyzer agent

### Fixed
- MySQL connection string parsing
```

### **User Updates**

```bash
# Users can update by reinstalling
/plugin uninstall my-db-toolkit
/plugin install my-db-toolkit@your-username
```

---

## 🌟 Real-World Examples to Study

- **Anthropic's Official Skills**: https://github.com/anthropics/skills
- **Dan Ávila's Marketplace**: https://github.com/dan-avila/claude-code-plugins
- **Seth Hobson's Subagents**: https://github.com/jeremylongshore/claude-code-plugins-plus

---

## ✅ Quick Start Checklist

- [ ] Create Git repository with plugin structure
- [ ] Add `plugin.json` with metadata
- [ ] Add `.mcp.json` with MCP server definitions (use environment variables!)
- [ ] Create skills in `skills/` directory
- [ ] Create agents in `agents/` directory
- [ ] Create commands in `commands/` directory
- [ ] Add comprehensive README with setup instructions
- [ ] Test locally with test marketplace
- [ ] Push to GitHub/GitLab
- [ ] Install and verify: `/plugin marketplace add user/repo`

---

## 🚨 Important Notes

1. **MCPs need environment variables** - Never commit credentials
2. **Skills activate automatically** - Claude decides when to use them
3. **Commands need manual invocation** - User types `/command-name`
4. **Agents can be automatic or manual** - Depends on description
5. **Plugins install globally** - Available across all projects once installed
6. **Repository-level config** - For team auto-install

---

**You now have everything you need to create, package, and distribute your own Claude Code plugin!** 🎉