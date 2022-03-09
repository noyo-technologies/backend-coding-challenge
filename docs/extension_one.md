# Extension One: Get Address by Date

A client has requested the ability to find a segment by its date. You may have noticed that the `GET /api/persons/:id/segment` endpoint only returns whatever the first segment the database returns.
Implement the ability to query the segment by date.

`GET /api/persons/:id/segment?date=YYYY-MM-DD`

The endpoint should return the segment that contains the `date` provided in the query string.

