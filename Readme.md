# Streaming JSON Parser
This repository contains a **Streaming JSON Parser** developed in Python, capable of processing data received incrementally. At the moment, it can only parse strings and nested objects.<br>
The typical scenario is to simulate partial responses as would be encountered in the streaming output of a large language model (LLM).

A simple example:
```python
parser = StreamingJsonParser()
parser.consume('{"foo":')
parser.consume('"bar')
assert parser.get() == {"foo": "bar"}
```

# Testing the parser
- create a *venv*: `python3 -m venv .venv`
- activate *venv*: `source .venv/bin/activate`
- install dependencies: `pip install -r requirements.txt`
- run tests: `pytest`
