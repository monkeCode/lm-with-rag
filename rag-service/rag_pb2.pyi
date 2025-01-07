from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VectorizeRequest(_message.Message):
    __slots__ = ("documents",)
    DOCUMENTS_FIELD_NUMBER: _ClassVar[int]
    documents: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, documents: _Optional[_Iterable[str]] = ...) -> None: ...

class VectorizeResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: int
    def __init__(self, result: _Optional[int] = ...) -> None: ...

class GetAnswerRequest(_message.Message):
    __slots__ = ("document",)
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    document: str
    def __init__(self, document: _Optional[str] = ...) -> None: ...

class SimilarDocument(_message.Message):
    __slots__ = ("document", "similarity")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    SIMILARITY_FIELD_NUMBER: _ClassVar[int]
    document: str
    similarity: float
    def __init__(self, document: _Optional[str] = ..., similarity: _Optional[float] = ...) -> None: ...

class GetAnswerResponse(_message.Message):
    __slots__ = ("answers",)
    ANSWERS_FIELD_NUMBER: _ClassVar[int]
    answers: _containers.RepeatedCompositeFieldContainer[SimilarDocument]
    def __init__(self, answers: _Optional[_Iterable[_Union[SimilarDocument, _Mapping]]] = ...) -> None: ...
