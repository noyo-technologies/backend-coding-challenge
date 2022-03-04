# Extension Two: Insert and Merge Location Segments

There is an external application that Noyo syncs data with. They get segment data from the past that we need to inject. As such, we need a new endpoint that will take in a single segment for an employee and merge it into our existing list of segments. 

1. The incoming segment will always have an end_date
2. Incoming segment wins in an overlap scenario, meaning you must update the start and end dates of any existing segment as necessary.

