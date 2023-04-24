from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CompletedCommandsRequest(_message.Message):
    __slots__ = ["rover_index"]
    ROVER_INDEX_FIELD_NUMBER: _ClassVar[int]
    rover_index: str
    def __init__(self, rover_index: _Optional[str] = ...) -> None: ...

class CompletedCommandsResponse(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class MapRequest(_message.Message):
    __slots__ = ["rover_name"]
    ROVER_NAME_FIELD_NUMBER: _ClassVar[int]
    rover_name: str
    def __init__(self, rover_name: _Optional[str] = ...) -> None: ...

class MapResponse(_message.Message):
    __slots__ = ["map"]
    MAP_FIELD_NUMBER: _ClassVar[int]
    map: str
    def __init__(self, map: _Optional[str] = ...) -> None: ...

class MineSerialNumRequest(_message.Message):
    __slots__ = ["mine_coord", "rover_index"]
    MINE_COORD_FIELD_NUMBER: _ClassVar[int]
    ROVER_INDEX_FIELD_NUMBER: _ClassVar[int]
    mine_coord: str
    rover_index: str
    def __init__(self, rover_index: _Optional[str] = ..., mine_coord: _Optional[str] = ...) -> None: ...

class MineSerialNumResponse(_message.Message):
    __slots__ = ["mine_serial_num", "rover_index"]
    MINE_SERIAL_NUM_FIELD_NUMBER: _ClassVar[int]
    ROVER_INDEX_FIELD_NUMBER: _ClassVar[int]
    mine_serial_num: str
    rover_index: str
    def __init__(self, rover_index: _Optional[str] = ..., mine_serial_num: _Optional[str] = ...) -> None: ...

class MovesRequest(_message.Message):
    __slots__ = ["rover_index"]
    ROVER_INDEX_FIELD_NUMBER: _ClassVar[int]
    rover_index: str
    def __init__(self, rover_index: _Optional[str] = ...) -> None: ...

class MovesResponse(_message.Message):
    __slots__ = ["moves"]
    MOVES_FIELD_NUMBER: _ClassVar[int]
    moves: str
    def __init__(self, moves: _Optional[str] = ...) -> None: ...

class ShareMinePinRequest(_message.Message):
    __slots__ = ["mine_pin", "rover_index"]
    MINE_PIN_FIELD_NUMBER: _ClassVar[int]
    ROVER_INDEX_FIELD_NUMBER: _ClassVar[int]
    mine_pin: str
    rover_index: str
    def __init__(self, rover_index: _Optional[str] = ..., mine_pin: _Optional[str] = ...) -> None: ...

class ShareMinePinResponse(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
