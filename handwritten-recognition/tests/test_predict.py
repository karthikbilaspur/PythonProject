from typing import Any, Callable, cast

import numpy as np, pytest
from src.utils.helpers import format_result as _format_result, labels_for_mode

format_result = cast(Callable[[np.ndarray, str], dict[str, Any]], _format_result)
def test_format():
    r = format_result(np.array([0.0]*7 + [0.9] + [0.0]*28), "combined")
    assert r["prediction"] == "7"; assert r["confidence"] == 0.9; assert len(r["top3"]) == 3
def test_labels():
    assert labels_for_mode("digits")[0] == "0"; assert labels_for_mode("letters")[0] == "A"; assert len(labels_for_mode("combined")) == 36
    with pytest.raises(ValueError): labels_for_mode("nope")
