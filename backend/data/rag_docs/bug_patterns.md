# Bug Patterns

## Off-by-One Errors
Check loop boundaries carefully. Bugs often happen when using `<`, `<=`, `range(n)`, or indexing `arr[i + 1]`.

Category: Bug
Severity: Medium
Languages: All

## Null or None References
Always validate that an object is not `None` or `null` before accessing its fields or methods.

Bad:
value = user.profile.name

Good:
if user and user.profile:
    value = user.profile.name

Category: Bug
Severity: High
Languages: Python, JavaScript, Java

## Mutable Default Arguments
Do not use mutable objects like lists or dictionaries as Python default arguments.

Bad:
def add_item(item, items=[]):
    items.append(item)
    return items

Good:
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

Category: Bug
Severity: High
Languages: Python