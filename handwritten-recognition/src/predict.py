import logging
from pathlib import Path
from typing import Any, Literal, cast

import numpy as np
from numpy.typing import NDArray
from tensorflow.keras.models import load_model  # type: ignore[import-not-found]

from config import COMBINED_MODEL_PATH, DIGIT_MODEL_PATH, LETTER_MODEL_PATH
from src.utils.helpers import format_result  # type: ignore[reportUnknownVariableType]

logger = logging.getLogger(__name__)

ModelMode = Literal["combined", "digits", "letters"]


class Predictor:
    def __init__(self) -> None:
        self._models: dict[ModelMode, Any] = {}

    def _load(self, mode: ModelMode) -> Any:
        if mode in self._models:
            return self._models[mode]

        path_map: dict[ModelMode, Path] = {
            "combined": COMBINED_MODEL_PATH,
            "digits": DIGIT_MODEL_PATH,
            "letters": LETTER_MODEL_PATH,
        }
        path = path_map[mode]
        if not path.exists():
            raise FileNotFoundError(f"Model not found for {mode}: {path}. Run scripts/train_*.py first.")

        model = cast(Any, load_model)(str(path))
        self._models[mode] = model
        return model

    def loaded_models(self) -> dict[ModelMode, bool]:
        return {k: (k in self._models) for k in ("combined", "digits", "letters")}

    def predict_array(
        self,
        arr: NDArray[np.float32],
        mode: ModelMode = "combined",
    ) -> dict[str, object]:
        model = self._load(mode)
        probs = model.predict(arr, verbose=0)[0]
        result = cast(Any, format_result)(probs, mode)
        return cast(dict[str, object], result)
