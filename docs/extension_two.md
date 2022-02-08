# Extension Two: Merge Address Segment Lists

There is an application that we need to sync segment data with. We need a new endpoint that will take in a list of segments for an employee and merge them into our existing list of segments. Overlapping segments with the same address should be merged into one segment. In the case overlappping segments incoming segments win. Incoming segments ALL have end date. See below for some hints.

```python
# Starter
class MergeSegmentSchema(SegmentSchema):
    end_date = fields.Date(required=True)


class MergeSchema(Schema):
    segments = fields.List(
        fields.Nested(MergeSegmentSchema),
        required=True,
    )


@app.route("/api/persons/<uuid:person_id>/merge", methods=["PUT"])
@use_args(MergeSchema())
def merge_segments(payload: dict, person_id: UUID):
    pass
```