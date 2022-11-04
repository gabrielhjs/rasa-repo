import inspect
from typing import Any, Awaitable, Callable, Text

from rasa.core.channels import InputChannel, UserMessage
from sanic import Blueprint, HTTPResponse, Request, response


class HealthCheckInput(InputChannel):
    @classmethod
    def name(cls) -> Text:
        return "status"

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[Any]]
    ) -> Blueprint:
        """Groups the collection of endpoints used by rest channel."""
        module_type = inspect.getmodule(self)
        if module_type is not None:
            module_name = module_type.__name__
        else:
            module_name = None

        custom_webhook = Blueprint(
            "custom_webhooks",
            module_name,
        )

        @custom_webhook.route("/", methods=["GET"])
        async def health(_request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        return custom_webhook
