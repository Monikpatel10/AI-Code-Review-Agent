# Security Rules

## SQL Injection
Avoid building SQL queries using string concatenation, f-strings, or template literals. Use parameterized queries or prepared statements.

Bad:
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

Good:
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

Category: Security
Severity: Critical
Languages: Python, JavaScript, Java

## Hardcoded Secrets
Do not hardcode API keys, passwords, database URLs, tokens, or private keys in source code. Use environment variables or a secret manager.

Category: Security
Severity: Critical
Languages: All

## Unsafe Deserialization
Avoid unsafe deserialization using pickle, yaml.load without SafeLoader, or similar APIs on untrusted input.

Category: Security
Severity: High
Languages: Python