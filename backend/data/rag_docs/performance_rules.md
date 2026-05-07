# Performance Rules

## N+1 Query Problem
Avoid executing database queries inside loops. Fetch related data in a single query using joins or batching.

Bad:
for user in users:
    db.query(f"SELECT * FROM orders WHERE user_id = {user.id}")

Good:
SELECT * FROM orders WHERE user_id IN (...)

Category: Performance
Severity: High
Languages: Python, JavaScript, Java

## Inefficient Loops (O(n^2))
Avoid nested loops when a hash map or set can reduce complexity to O(n).

Bad:
for i in range(len(arr)):
    for j in range(len(arr)):
        if arr[i] == arr[j]:
            ...

Good:
seen = set()
for x in arr:
    if x in seen:
        ...
    seen.add(x)

Category: Performance
Severity: Medium
Languages: All

## Unnecessary Recomputations
Avoid recalculating values repeatedly inside loops. Cache results or compute once outside the loop.

Category: Performance
Severity: Medium
Languages: All