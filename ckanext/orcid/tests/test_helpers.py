from __future__ import annotations

from ckanext.orcid.utils import check_pattern, is_valid_orcid

import pytest


@pytest.mark.parametrize(
    "orcid",
    [
        "0000-0002-1825-0097",
        "0000-0001-5109-3700",
        "0000-0002-1694-233X",
    ],
)
def test_check_pattern_valid(orcid):
    assert check_pattern(orcid) is True


@pytest.mark.parametrize(
    "orcid",
    [
        "0000-0002-1825-009",  # too short last segment
        "000-0002-1825-0097",  # too short first segment
        "0000-0002-1825-00970",  # too long
        "XXXX-0002-1825-0097",  # non-digits in first segment
        "0000-0002-1825-009A",  # invalid char (not X) at end
        "",
        "not-an-orcid",
    ],
)
def test_check_pattern_invalid(orcid):
    assert check_pattern(orcid) is False


def test_is_valid_orcid_fails_on_bad_format():
    # Should return False immediately without hitting the API
    assert is_valid_orcid("not-valid") is False
