from typing import Dict, Text, TypedDict, Union

SCHEMA = {
    "type": "object",
}


class TextMessage(TypedDict):
    text: Text


Message = Dict[Text, Union[TextMessage]]
