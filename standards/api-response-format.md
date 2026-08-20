# API Response Format Standard

All API responses follow this envelope:

```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "meta": {
    "page": 1,
    "total": 100
  }
}
```

- Always use `success` boolean
- `data` contains the response payload on success
- `error` contains {code, message} on failure
- `meta` contains pagination metadata when applicable

## HTTP Status Codes
- 200: Success
- 201: Created
- 400: Bad request (validation error)
- 401: Unauthorized
- 404: Not found
- 500: Server error
