Please analyze and fix the GitHub issue: $ARGUMENTS

## Workflow

1. **Understand the Issue**
   - Read the issue description thoroughly
   - Identify the expected vs actual behavior
   - Note any reproduction steps provided

2. **Locate Relevant Code**
   - Search for files/functions mentioned in the issue
   - Use grep/codebase search to find related code
   - Review recent changes that might have caused the issue

3. **Implement the Fix**
   - Make minimal, focused changes
   - Follow project coding standards
   - Add comments explaining non-obvious fixes
   - Consider edge cases

4. **Test the Fix**
   - Verify the fix resolves the reported issue
   - Run existing tests to prevent regressions
   - Add new tests if coverage is lacking

5. **Document the Solution**
   - Create a clear commit message
   - Reference the issue number
   - Explain what was changed and why

## Commit Message Format
```
Fix: [Brief description] (Issue #$ARGUMENTS)

- Detailed explanation of the problem
- What was changed
- Why this approach was chosen

Resolves #$ARGUMENTS
```

