from typing import TypedDict, Text, Literal, List


class MpWppText(Text):
    pass


class MpWppMedia(TypedDict):
    url: Text
    caption: Text


class MpWppInteractiveHeader(TypedDict):
    type: Literal[
        "text",
        "video",
        "image",
        "document",
    ]


class MpWppInteractiveHeaderText(MpWppInteractiveHeader):
    text: Text


class MpWppInteractiveHeaderVideo(MpWppInteractiveHeader):
    video: MpWppMedia


class MpWppInteractiveHeaderImage(MpWppInteractiveHeader):
    image: MpWppMedia


class MpWppInteractiveHeaderDocument(MpWppInteractiveHeader):
    document: MpWppMedia


class MpWppInteractiveBody(TypedDict):
    text: Text


class MpWppInteractiveSectionRow(TypedDict):
    id: Text
    title: Text
    description: Text


class MpWppInteractiveSection(TypedDict):
    title: Text
    rows: List[MpWppInteractiveSectionRow]


class MpWppInteractiveActionSections(TypedDict):
    sections: List[MpWppInteractiveSection]


class MpWppInteractiveActionButton(TypedDict):
    button: Text


class MpWppInteractiveButton(TypedDict):
    id: Text
    type: Text
    title: Text


class MpWppInteractiveActionButtons(TypedDict):
    buttons: List[MpWppInteractiveButton]


class MpWppInteractiveFooter(TypedDict):
    text: Text


class MpWppInteractiveReply(TypedDict, total=False):
    id: Text
    text: Text
    description: Text


class MpWppInteractive(TypedDict, total=False):
    type: Literal[
        "list",
        "button",
        "product",
        "product_list",
        "button_reply",
    ]
    header: Literal[
        "MpWppInteractiveHeaderText",
        "MpWppInteractiveHeaderVideo",
        "MpWppInteractiveHeaderImage",
        "MpWppInteractiveHeaderDocument",
    ]
    body: MpWppInteractiveBody
    action: Literal[
        "MpWppInteractiveActionSections",
        "MpWppInteractiveActionButton",
        "MpWppInteractiveActionButtons",
    ]
    footer: MpWppInteractiveFooter
    reply: MpWppInteractiveReply


class MpWppMessage(TypedDict):
    type: Literal[
        "text",
        "interactive",
    ]
    content: Literal[
        "MpWppText",
        "MpWppMedia",
        "MpWppInteractive",
    ]
    preview_url: bool
    recipient_type: Literal["individual"]
    to: Text
