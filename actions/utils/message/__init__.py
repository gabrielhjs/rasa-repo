import json

from jsonschema import validate  # type: ignore

from .schema import SCHEMA, Message

message_file = open("./messages.json")

message: Message = json.load(message_file)

validate(message, schema=SCHEMA)
