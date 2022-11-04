from enum import Enum
from typing import List, Text

from fhir_types import FHIR_Questionnaire_AnswerOption
from typing_extensions import TypedDict


class InteractiveType(Text, Enum):
    BUTTON = "button"


class InteractiveBody(TypedDict):
    text: str


class ButtonType(Text, Enum):
    REPLY = "reply"


class Button(TypedDict):
    id: str
    type: ButtonType
    title: str


class InteractiveAction(TypedDict):
    buttons: List[Button]


class Interactive(TypedDict):
    type: InteractiveType
    body: InteractiveBody
    action: InteractiveAction


class InteractiveMessage(TypedDict):
    interactive: Interactive


def render_elements(
    options: List[FHIR_Questionnaire_AnswerOption],
) -> InteractiveMessage:
    return InteractiveMessage(
        interactive=Interactive(
            type=InteractiveType.BUTTON,
            body=InteractiveBody(text="test"),
            action=InteractiveAction(
                buttons=[
                    Button(
                        id=option["valueCoding"]["code"],
                        type=ButtonType.REPLY,
                        title=option["valueCoding"]["display"],
                    )
                    for option in options
                ]
            ),
        )
    )
