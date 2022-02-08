# Extension Two: Insert and Merge addres segments

There is an application that we need to sync segment data with. We need a new endpoint that will take in a list of segments for an employee and merge them into our existing list of segments. 

1. Incoming segments all have end dates. 
2. Incoming segment do not overlap each other
3. Incoming segment that overlap existing segments win, meaning you must update the start and end dates of each segment as necessary.

