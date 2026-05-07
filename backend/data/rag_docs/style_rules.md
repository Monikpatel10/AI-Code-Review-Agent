# Style Rules

## Single Responsibility Principle
Each function or class should do one clear job. Split large functions into smaller units when they mix validation, business logic, database access, and response formatting.

Category: Style
Severity: Medium
Languages: All

## Meaningful Naming
Use clear names that describe purpose. Avoid names like `x`, `data`, `temp`, or `stuff` when the value has a specific meaning.

Category: Style
Severity: Low
Languages: All

## Avoid Duplicate Code
Repeated blocks should be extracted into reusable functions or shared utilities.

Category: Style
Severity: Medium
Languages: All

## Specific Exception Handling
Avoid bare `except:` or broad `catch(Exception)` unless there is a clear reason. Catch specific exceptions and log useful context.

Category: Style
Severity: Medium
Languages: Python, JavaScript, Java