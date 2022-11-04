import json
from typing import Any, Dict, List, Text, Union

from fhir_types import (
    FHIR_Questionnaire,
    FHIR_QuestionnaireResponse,
    FHIR_Questionnaire_Item,
)
from rasa_sdk import Action, Tracker  # type: ignore
from rasa_sdk.events import ActiveLoop, SlotSet  # type: ignore
from rasa_sdk.executor import CollectingDispatcher  # type: ignore
from rasa_sdk.types import DomainDict  # type: ignore

from .utils.mb_wpp import GLOBAL_MESSAGES
from .custom_action import CustomAction
from .utils.mb_wpp.elements import render_elements


questionnaire: FHIR_Questionnaire = {
    "resourceType": "Questionnaire",
    "id": "1",
    "title": "Formulário de acompanhamento",
    "status": "active",
    "code": [{"system": "laura", "code": "1"}],
    "item": [
        {
            "text": "Como se sente hoje?",
            "type": "choice",
            "linkId": "1",
            "code": [{"system": "laura", "code": "1.1"}],
            "answerOption": [
                {
                    "valueCoding": {
                        "system": "laura",
                        "code": "1.1.1",
                        "display": "melhorei",
                    }
                },
                {
                    "valueCoding": {
                        "system": "laura",
                        "code": "1.1.2",
                        "display": "piorei",
                    }
                },
            ],
            "repeats": False,
            "required": False,
            "readOnly": False,
        },
        {
            "text": "Deseja falar com um profissional?",
            "linkId": "2",
            "type": "choice",
            "code": [{"system": "laura", "code": "1.2"}],
            "answerOption": [
                {
                    "valueCoding": {
                        "system": "laura",
                        "code": "1.2.1",
                        "display": "sim",
                    }
                },
                {
                    "valueCoding": {
                        "system": "laura",
                        "code": "1.2.2",
                        "display": "não",
                    }
                },
            ],
            "repeats": False,
            "required": True,
            "enableWhen": [
                {
                    "question": "1",
                    "operator": "=",
                    "answerCoding": {
                        "system": "laura",
                        "code": "1.1.2",
                        "display": "piorei",
                    },
                }
            ],
            "enableBehavior": "all",
        },
    ],
}
questionnaire_response: FHIR_QuestionnaireResponse = {
    "resourceType": "QuestionnaireResponse",
    "item": [],
}


async def get_questionnaire(_sender_id: str, _questionnaire: str) -> FHIR_Questionnaire:
    global questionnaire
    return questionnaire


async def get_questionnaire_response(
    _sender_id: str, _questionnaire: str
) -> FHIR_QuestionnaireResponse:
    global questionnaire_response
    return questionnaire_response


async def save_questionnaire_response(qr: FHIR_QuestionnaireResponse) -> None:
    global questionnaire_response
    questionnaire_response = qr


class ActionFhirQuestionnaire(CustomAction, Action):
    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        fhir_questionnaire: Union[Text, None] = tracker.slots.get("fhir_questionnaire")
        questionnaire_item: int

        if fhir_questionnaire is None:
            fhir_questionnaire: FHIR_Questionnaire = await get_questionnaire(
                tracker.sender_id, "asd"
            )
            fhir_questionnaire_response: FHIR_QuestionnaireResponse = (
                await get_questionnaire_response(tracker.sender_id, "asd")
            )
            questionnaire_item = 0

        else:
            fhir_questionnaire: FHIR_Questionnaire = json.loads(fhir_questionnaire)
            fhir_questionnaire_response: FHIR_QuestionnaireResponse = json.loads(
                tracker.slots.get("fhir_questionnaire_response")
            )
            questionnaire_item = int(tracker.slots.get("fhir_questionnaire_item"))

        if questionnaire_item > 0:
            answer = int(tracker.latest_message["text"])
            question: FHIR_Questionnaire_Item = fhir_questionnaire["item"][
                questionnaire_item - 1
            ]

            fhir_questionnaire_response["item"].append(
                {
                    "linkId": fhir_questionnaire["id"],
                    "text": question["text"],
                    "answer": [question["answerOption"][answer]],
                }
            )

        if questionnaire_item < len(fhir_questionnaire["item"]):
            item = fhir_questionnaire["item"][questionnaire_item]

            dispatcher.utter_message(json_message=render_elements(item["answerOption"]))

            opt = {"1": "sair do questionario"}

            if not item["required"]:
                opt.update({"2": "próxima"})

            dispatcher.utter_message(json_message=opt)

            return [
                ActiveLoop("action_fhir_questionnaire"),
                SlotSet("fhir_questionnaire", json.dumps(fhir_questionnaire)),
                SlotSet(
                    "fhir_questionnaire_response",
                    json.dumps(fhir_questionnaire_response),
                ),
                SlotSet("fhir_questionnaire_item", str(questionnaire_item + 1)),
            ]

        await save_questionnaire_response(fhir_questionnaire_response)

        dispatcher.utter_message(text=GLOBAL_MESSAGES["text_example"]["text"])

        return [
            ActiveLoop(None),
            SlotSet("fhir_questionnaire_item"),
            SlotSet("fhir_questionnaire"),
            SlotSet("fhir_questionnaire_response"),
        ]
