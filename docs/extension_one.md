# Extension One: `start_date` Validation

Our database schema does not allow for more than one Address Segment with the same `start_date` for the same Person. If a caller sends an API request to the server with the same `start_date` as an existing Address Segment the server should return the following response with a status code of `422`:

```json
{
    "error": "Address segment already exists with start_date 2021-01-01"
}
```

Your task for this extension is to implement this behavior on the `PUT /api/persons/:id/address` endpoint. In order to assist with implementing this behavior we have provided a [failing test case](/tests/api/test_addresses.py#L121).
