# Extension Two: Insert and Merge address segments

There is an external application that noyo syncs data with. They get segment data from the past that we need to inject. As such, we need a new endpoint that will take in a single segment for an employee and merge it into our existing list of segments. 

1. Incoming segments all have end dates. 
2. Incoming segment wins in an overlap scenario, meaning you must update the start and end dates of any existing segment as necessary.

