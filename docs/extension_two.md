# Extension Two: Merge Address Segment Lists

There is an external API client that modifies segments that is out of our control. We need a new endpoint that will take in a list of segments for an employee and merge them into our existing list of segments. Overlapping segments with the same address should be merged into one segment.

```python
# Suggestion
class MergeSchema(Schema):
    segments = fields.List(fields.Nested(SegmentSchema),  required=True,)


@app.route("/api/persons/<uuid:person_id>/merge", methods=["PUT"])
@use_args(MergeSchema())
def merge_segments(payload: dict, person_id: UUID):
    pass
```