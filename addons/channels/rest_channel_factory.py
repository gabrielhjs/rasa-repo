import inspect
import logging
from typing import Callable, Awaitable, Any, Text, Union, Optional, Dict
from abc import ABC

from rasa.core.channels import InputChannel, UserMessage, CollectingOutputChannel
from sanic import Blueprint, Request, HTTPResponse, response
from sanic.response import ResponseStream


logger = logging.getLogger(__name__)


class MyRestChannelFactory(InputChannel, ABC):
  channel_name: Text

  @classmethod
  def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> InputChannel:
    if not credentials:
      cls.raise_missing_credentials_exception()

    return cls(
      credentials.get("credential"),
    )

  def __init__(self, credential: Text):
    self.credential = credential

  @classmethod
  def name(cls) -> Text:
    return cls.channel_name

  @staticmethod
  async def _extract_sender(req: Request) -> Optional[Text]:
    return req.json.get("sender", None)

    # noinspection PyMethodMayBeStatic

  @staticmethod
  def _extract_message(req: Request) -> Optional[Text]:
    return req.json.get("message", None)

  def _extract_input_channel(self, req: Request) -> Text:
    return req.json.get("input_channel") or self.name()

  def blueprint(self, on_new_message: Callable[[UserMessage], Awaitable[Any]]) -> Blueprint:
    """Groups the collection of endpoints used by rest channel."""
    module_type = inspect.getmodule(self)
    if module_type is not None:
      module_name = module_type.__name__
    else:
      module_name = None

    custom_webhook = Blueprint(
      self.name(),
      module_name,
    )

    @custom_webhook.route("", methods=["POST"])
    async def receive(request: Request) -> Union[ResponseStream, HTTPResponse]:
      sender_id = await self._extract_sender(request)
      text = self._extract_message(request)
      input_channel = self._extract_input_channel(request)
      metadata = self.get_metadata(request)

      collector = CollectingOutputChannel()
      try:
        await on_new_message(
          UserMessage(
            text,
            collector,
            sender_id,
            input_channel=input_channel,
            metadata=metadata,
          )
        )
      except Exception as e:
        logger.exception(
          f"An exception occured while handling "
          f"user message '{text}'."
          f"Exception '{e}'."
        )

      return response.json(collector.messages)

    return custom_webhook

  def get_metadata(self, request: Request) -> Optional[Dict[Text, Any]]:
    return request.json.get("metadata", None)

  def get_output_channel(self) -> Optional["CollectingOutputChannel"]:
    return CollectingOutputChannel()
