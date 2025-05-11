# 6_error_handling.md

## Description

Handles errors and edge cases.

## Pseudocode

```python
def handle_errors(query_result):
    """
    Handles errors and edge cases.
    """
    if query_result is None:
        # Handle the case where no data is found
        return "No data found for the given query."

        # TEST: Check if the no data message is returned correctly

    elif query_result == "API Error":
        # Handle the case where the API fails
        return "API Error: Please try again later."

        # TEST: Check if the API error message is returned correctly

    else:
        # If there are no errors, return the query result
        return query_result

        # TEST: Check if the query result is returned correctly
```

## TDD Anchors

- `// TEST: Check if the no data message is returned correctly`
- `// TEST: Check if the API error message is returned correctly`
- `// TEST: Check if the query result is returned correctly`
