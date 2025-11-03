# Roo-Code Command: quality-report

Generate comprehensive quality metrics report.

## Usage
```
/quality-report
```

## Metrics Included
- **Test Coverage** - Percentage of code tested
- **Bug Statistics** - Open/closed bug counts
- **Code Quality** - Linting/formatting issues
- **Technical Debt** - Areas needing refactoring
- **Documentation** - Coverage percentage
- **Security** - Known vulnerabilities

## Example Output
```markdown
# Quality Report
Date: 2025-11-02

## Test Coverage
- Unit Tests: 87%
- Integration Tests: 72%
- E2E Tests: 45%

## Bugs
- Critical: 0
- High: 2
- Medium: 5
- Low: 8

## Code Quality Score: 8.5/10
- Linting Issues: 3
- Formatting Issues: 0
- Complexity Warnings: 5

## Recommendations
1. Increase E2E test coverage
2. Fix 2 high-priority bugs
3. Refactor AuthController (complexity: high)
```
