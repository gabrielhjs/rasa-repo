import json
import logging
from typing import Union, Text, Dict

import jsonschema

from .message import MpWppInteractive, MpWppText
from .schema import CONTENT_SCHEMA


logger = logging.getLogger(__name__)


def load_messages() -> Dict[Text, Union[MpWppInteractive, MpWppText]]:
    messages_file = open("./messages.json", encoding="Utf-8")

    messages: Dict[Text, Union[MpWppInteractive, MpWppText]] = json.load(messages_file)

    try:
        for key, value in messages.items():
            jsonschema.validate(value, CONTENT_SCHEMA)

    except jsonschema.exceptions.ValidationError as e:
        logger.error("Failed to load messages")
        print(e.message)
        exit(1)

    logger.info("Successfully loaded messages")

    return messages
