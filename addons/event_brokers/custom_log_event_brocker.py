import logging
from asyncio import AbstractEventLoop
from typing import Dict, Text, Any, Optional, Type

from rasa.core.brokers.broker import EventBroker, EB
from rasa.utils.endpoints import EndpointConfig


logger = logging.getLogger("LogEventBroker")


class LogEventBroker(EventBroker):
  @classmethod
  async def from_endpoint_config(
    cls: Type["LogEventBroker"],
    broker_config: EndpointConfig,
    event_loop: Optional[AbstractEventLoop] = None
  ) -> Optional[EB]:
    return cls(
      broker_config.kwargs.get("credential")
    )

  def __init__(self, credential: Text) -> None:
    self.credential = credential

  def publish(self, event: Dict[Text, Any]) -> None:
    if event["event"] == "user":
      text = event.get("text", "***")
      logger.warning(f"user: {text}")

    elif event["event"] == "bot":
      text = event.get("text", "***")
      logger.warning(f"bot: {text}")
      logger.warning(self.credential)
