# Extension One: Get Address by Date

You may have noticed that the `GET /api/persons/:id/segment` endpoint only returns the 1st segment. This is probably not ideal behavior. We may want to go back in time (or forward) to see what the segment was or will be. The ability to query the segment by date should be implemented as follows:

`GET /api/persons/:id/segment?date=YYYY-MM-DD`

The endpoint should return the segment that contains the `date` provided in the query string.

