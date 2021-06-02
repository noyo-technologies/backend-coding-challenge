# Extension Three: Merge Contiguous Identical Address Segments

You may have noticed during your development that if you submit two identical address segments with different `start_date`'s that the API will create a new address segment record for each. In order to reduce the number of redundant records in the `address_segments` database, you should update the `PUT /api/persons/:id/address` endpoint to check if the new address segment is identical to the latest segment, and if it is it should skip creating a record and return the already existing segment. 

In order to assist with implementing this behavior we have provided a [failing test case](/tests/api/test_addresses.py#L164).

