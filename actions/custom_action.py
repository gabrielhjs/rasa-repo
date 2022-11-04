import re
from abc import ABC
from typing import Text

from rasa_sdk import Action  # type: ignore


class CustomAction(Action, ABC):
    def name(self) -> Text:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", self.__class__.__name__).lower()
