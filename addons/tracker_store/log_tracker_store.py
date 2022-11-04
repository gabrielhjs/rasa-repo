from typing import Any, Dict, Iterable, Optional, Text

from rasa.core.brokers.broker import EventBroker
from rasa.core.tracker_store import TrackerStore
from rasa.shared.core.domain import Domain
from rasa.shared.core.trackers import DialogueStateTracker


class LogTrackerStore(TrackerStore):
    memory: Dict[Text, any]

    def __init__(
        self,
        domain: Domain,
        event_broker: Optional[EventBroker] = None,
        **kwargs: Dict[Text, Any],
    ) -> None:
        """Initializes the tracker store."""
        self.store: Dict[Text, Text] = {}
        super().__init__(domain, event_broker, **kwargs)
        self.memory = {}

    async def save(self, tracker: DialogueStateTracker) -> None:
        self.memory.update({tracker.sender_id: tracker})

        await self.stream_events(tracker)

    async def retrieve(self, sender_id: Text) -> Optional[DialogueStateTracker]:
        return self.memory.get(sender_id, None)

    async def keys(self) -> Iterable[Text]:
        return self.memory.keys()
