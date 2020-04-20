from RecordLib.utilities.serializers import to_serializable


def test_case_serialize(example_case):
    serialized = to_serializable(example_case)
    assert "docket_number" in serialized.keys()
    assert "otn" in serialized.keys()


def test_serialize_none():
    serialized = to_serializable(None)
    assert serialized == ""


def test_serialize_docket(example_docket):
    ser = to_serializable(example_docket)
    assert "_case" in ser.keys()


def test_serialize_summary(example_summary):
    ser = to_serializable(example_summary)
    assert "_cases" in ser.keys()
