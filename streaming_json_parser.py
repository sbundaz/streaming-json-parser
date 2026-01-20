from enum import Enum, auto


class ParserState(Enum):
    EXPECT_OBJECT_START = auto()
    EXPECT_KEY_OR_END = auto()
    IN_KEY = auto()
    EXPECT_COLON = auto()
    EXPECT_VALUE = auto()
    IN_STRING_VALUE = auto()
    EXPECT_COMMA_OR_END = auto()


class StreamingJsonParser:
    def __init__(self):
        self._state = ParserState.EXPECT_OBJECT_START
        self._result = {}
        self._current_key = ""
        self._nested_objects = []
        self._keys = []

    def consume(self, buffer: str):
        for c in buffer:
            self._process_char(c)

    def get(self) -> object:
        return self._result
    
    @property
    def _current_obj(self):
        return self._result if not self._nested_objects else self._nested_objects[-1]
    
    def _close_current_obj(self):
        if self._nested_objects:
            self._nested_objects.pop()
            self._current_key = self._keys.pop()

    def _process_char(self, char: str):
        match self._state:
            case ParserState.EXPECT_OBJECT_START:
                self._process_expect_obj_start(char)
            case ParserState.EXPECT_KEY_OR_END:
                self._process_expect_key_or_end(char)
            case ParserState.IN_KEY:
                self._process_in_key(char)
            case ParserState.EXPECT_COLON:
                self._process_expect_colon(char)
            case ParserState.EXPECT_VALUE:
                self._process_expect_value(char)
            case ParserState.IN_STRING_VALUE:
                self._process_in_string_value(char)
            case ParserState.EXPECT_COMMA_OR_END:
                self._process_expect_comma_or_end(char)
            case _:
                raise ValueError("Invalid state")

    def _process_expect_obj_start(self, char: str):
        if char.isspace():
            return
        elif char == "{":
            self._state = ParserState.EXPECT_KEY_OR_END
        else:
            raise ValueError(f"Expected '{{', got '{char}'")

    def _process_expect_key_or_end(self, char: str):
        if char.isspace():
            return
        elif char == '"':
            self._current_key = ""
            self._state = ParserState.IN_KEY
        elif char == "}":
            self._close_current_obj()
            self._state = ParserState.EXPECT_COMMA_OR_END
        else:
            raise ValueError(f"Expected '\"' or '}}', got '{char}'")

    def _process_in_key(self, char: str):
        if char == '"':
            self._state = ParserState.EXPECT_COLON
        else:
            self._current_key += char

    def _process_expect_colon(self, char: str):
        if char.isspace():
            return
        elif char == ":":
            self._state = ParserState.EXPECT_VALUE
        else:
            raise ValueError(f"Expected ':', got '{char}'")

    def _process_expect_value(self, char: str):
        if char.isspace():
            return
        elif char == '"':
            self._state = ParserState.IN_STRING_VALUE
            self._current_obj[self._current_key] = "" # partial value
        elif char == "{":
            new_nested_object = {}
            self._current_obj[self._current_key] = new_nested_object
            self._nested_objects.append(new_nested_object)
            self._keys.append(self._current_key)
            self._state = ParserState.EXPECT_KEY_OR_END
        else:
            raise ValueError(f"Expected '\"', got '{char}'")

    def _process_in_string_value(self, char: str):
        if char == '"':
            self._state = ParserState.EXPECT_COMMA_OR_END
        else:
            self._current_obj[self._current_key] += char

    def _process_expect_comma_or_end(self, char: str):
        if char.isspace():
            return
        elif char == "}":
            self._close_current_obj()
            self._state = ParserState.EXPECT_COMMA_OR_END
        elif char == ",":
            self._state = ParserState.EXPECT_KEY_OR_END
        else:
            raise ValueError(f"Expected ',' or '}}', got '{char}'")