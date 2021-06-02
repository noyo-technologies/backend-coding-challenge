# Extension Two: Get Address by Date

You may have noticed that the `GET /api/persons/:id/address` endpoint only returns the latest address segment. In most cases this is the desired behavior, but in some cases we may want to go back in time (or forward) to see what the address was or will be. The ability to query the address by date should be implemented as follows:

`GET /api/persons/:id/address?date=YYYY-MM-DD`

The endpoint should return the address segment that corresponds to the `date` provided in the query string. In order to assist with implementing this behavior we have provided a [failing test case](/tests/api/test_addresses.py#L140).

