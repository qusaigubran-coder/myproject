from threading import Lock

_processed_event_ids: set[str] = set()
_lock = Lock()


def register_event(event_id: str) -> bool:
    with _lock:
        if event_id in _processed_event_ids:
            return False

        _processed_event_ids.add(event_id)
        return True


def reset_event_store() -> None:
    with _lock:
        _processed_event_ids.clear()
