"""AI-generated unit tests for edge cases and boundary values."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    """Helper to create test interaction logs."""
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_matches_when_multiple_have_same_item_id() -> None:
    """Test that filtering returns ALL interactions with matching item_id, not just the first."""
    interactions = [
        _make_log(1, 1, 1),
        _make_log(2, 2, 1),  # Same item_id=1, different learner
        _make_log(3, 3, 1),  # Same item_id=1, different learner
        _make_log(4, 1, 2),  # Different item_id
    ]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 3
    assert all(i.item_id == 1 for i in result)
    assert set(i.id for i in result) == {1, 2, 3}


def test_filter_with_negative_item_id_returns_empty() -> None:
    """Test boundary value: negative item_id should not match any interactions."""
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, -1)
    assert result == []


def test_filter_with_zero_item_id_returns_empty() -> None:
    """Test boundary value: item_id=0 should not match interactions with positive IDs."""
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 0)
    assert result == []
