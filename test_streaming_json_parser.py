from streaming_json_parser import StreamingJsonParser


def test_init():
    parser = StreamingJsonParser()
    assert parser.get() == {}


def test_streaming_json_parser():
    parser = StreamingJsonParser()
    parser.consume('{"foo": "bar"}')
    assert parser.get() == {"foo": "bar"}


def test_chunked_streaming_json_parser():
    parser = StreamingJsonParser()
    parser.consume('{"foo":')
    parser.consume('"bar')
    assert parser.get() == {"foo": "bar"}


def test_partial_streaming_json_parser():
    parser = StreamingJsonParser()
    parser.consume('{"foo": "bar')
    assert parser.get() == {"foo": "bar"}


def test_multiple_consume():
    parser = StreamingJsonParser()
    parser.consume('{"foo"')
    assert parser.get() == {}

    parser.consume(': "')
    assert parser.get() == {"foo": ""}

    parser.consume("hello")
    assert parser.get() == {"foo": "hello"}

    parser.consume(' world", "name": "andrew"')
    assert parser.get() == {"foo": "hello world", "name": "andrew"}


def test_completed_nested_object():
    parser = StreamingJsonParser()
    parser.consume('{"full_name": {"firstname":"andrew", "lastname": "doh"}}')
    assert parser.get() == {"full_name": {"firstname": "andrew", "lastname": "doh"}}


def test_partial_nested_object():
    parser = StreamingJsonParser()
    parser.consume('{"full_name": {"firstname":"and')
    assert parser.get() == {"full_name": {"firstname": "and"}}

    parser.consume('rew", "lastname": "doh"}')
    assert parser.get() == {"full_name": {"firstname": "andrew", "lastname": "doh"}}


def test_empty_object():
    parser = StreamingJsonParser()
    parser.consume("{}")
    assert parser.get() == {}


def test_empty_nested_object():
    parser = StreamingJsonParser()
    parser.consume('{"empty": {}}')
    assert parser.get() == {"empty": {}}


def test_deeply_nested():
    parser = StreamingJsonParser()
    parser.consume('{"a": {"b": {"c": "deep"}}}')
    assert parser.get() == {"a": {"b": {"c": "deep"}}}


def test_partial_deep_nesting():
    parser = StreamingJsonParser()
    parser.consume('{"a": {"b": {"c": "de')
    assert parser.get() == {"a": {"b": {"c": "de"}}}


def test_sibling_after_nested():
    parser = StreamingJsonParser()
    parser.consume('{"nested": {"a": "1"}, "sibling": "2"}')
    assert parser.get() == {"nested": {"a": "1"}, "sibling": "2"}
