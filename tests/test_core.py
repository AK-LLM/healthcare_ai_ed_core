from core.context import context

def test_context_set_get():
    context.set("foo", "bar")
    assert context.get("foo") == "bar"
    context.clear()
    assert context.get("foo") is None
