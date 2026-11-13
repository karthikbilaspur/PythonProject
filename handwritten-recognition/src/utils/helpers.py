import numpy as np
from config import DIGIT_LABELS, LETTER_LABELS, COMBINED_LABELS
LABEL_MAPS = {"digits": DIGIT_LABELS, "letters": LETTER_LABELS, "combined": COMBINED_LABELS}
def labels_for_mode(mode):
    if mode not in LABEL_MAPS:
        raise ValueError(f"Unknown mode {mode}")
    return LABEL_MAPS[mode]
def top_k(probs, labels, k=3):
    probs = np.asarray(probs).flatten()
    idx = np.argsort(probs)[::-1][:k]
    return [{"label": labels[i], "confidence": float(probs[i])} for i in idx]
def format_result(probs, mode):
    labels = labels_for_mode(mode)
    probs = np.asarray(probs).flatten()
    pred = int(np.argmax(probs))
    return {"prediction": labels[pred], "confidence": float(probs[pred]), "top3": top_k(probs, labels, 3), "mode": mode}
