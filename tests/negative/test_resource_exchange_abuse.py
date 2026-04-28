from __future__ import annotations

import pytest

from tigrbl_auth.standards.oauth2.resource_indicators import select_resource_indicator


@pytest.mark.negative
def test_resource_indicator_abuse_cases_are_rejected() -> None:
    with pytest.raises(ValueError):
        select_resource_indicator(["https://rs.example.com/a", "https://rs.example.com/b"])
    with pytest.raises(ValueError):
        select_resource_indicator("https://rs.example.com/a", audience="https://rs.example.com/b")
