CONTENT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2019-09/schema",
    "type": "object",
    "oneOf": [{"required": ["interactive"]}, {"required": ["text"]}],
    "properties": {
        "text": {"type": "string"},
        "interactive": {
            "type": "object",
            "addtionalProperties": False,
            "required": ["type", "body", "action"],
            "properties": {
                "type": {"enum": ["list", "button"]},
                "body": {
                    "type": "object",
                    "addtionalProperties": False,
                    "properties": {"text": {"type": "string", "maxLenght": 1024}},
                },
                "action": {
                    "type": "object",
                    "addtionalProperties": False,
                    "oneOf": [
                        {"required": ["sections"]},
                        {"required": ["button"]},
                        {"required": ["buttons"]},
                    ],
                    "properties": {
                        "sections": {
                            "type": "array",
                            "minItems": 1,
                            "maxItems": 10,
                            "items": {
                                "type": "object",
                                "addtionalProperties": False,
                                "required": ["title"],
                                "properties": {
                                    "title": {"type": "string", "maxLenght": 24},
                                    "rows": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "addtionalProperties": False,
                                            "required": ["id", "title"],
                                            "properties": {
                                                "id": {
                                                    "type": "string",
                                                    "maxLenght": 200,
                                                },
                                                "title": {
                                                    "type": "string",
                                                    "maxLenght": 24,
                                                },
                                                "description": {
                                                    "type": "string",
                                                    "maxLenght": 72,
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                        "button": {"type": "string", "maxLenght": 20},
                        "buttons": {
                            "type": "array",
                            "minItems": 1,
                            "maxItems": 3,
                            "items": {
                                "type": "object",
                                "addtionalProperties": False,
                                "required": ["id", "type", "title"],
                                "properties": {
                                    "id": {"type": "string", "maxLenght": 256},
                                    "type": {"type": "string", "maxLenght": 20},
                                    "title": {"type": "string", "maxLenght": 20},
                                },
                            },
                        },
                    },
                },
                "footer": {
                    "type": "object",
                    "addtionalProperties": False,
                    "properties": {"text": {"type": "string", "maxLenght": 60}},
                },
            },
        },
    },
}
