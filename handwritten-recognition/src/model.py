from importlib import import_module
from typing import Any

_keras_models = import_module("tensorflow.keras.models")
_keras_layers = import_module("tensorflow.keras.layers")

Sequential: Any = _keras_models.Sequential
Conv2D: Any = _keras_layers.Conv2D
MaxPooling2D: Any = _keras_layers.MaxPooling2D
Flatten: Any = _keras_layers.Flatten
Dense: Any = _keras_layers.Dense
Dropout: Any = _keras_layers.Dropout
BatchNormalization: Any = _keras_layers.BatchNormalization


def build_model(
    num_classes: int,
    input_shape: tuple[int, int, int] = (28, 28, 1),
) -> Any:
    model = Sequential([
        Conv2D(32, (3,3), activation="relu", padding="same", input_shape=input_shape),
        BatchNormalization(), MaxPooling2D((2,2)),
        Conv2D(64, (3,3), activation="relu", padding="same"),
        BatchNormalization(), MaxPooling2D((2,2)),
        Conv2D(128, (3,3), activation="relu", padding="same"),
        BatchNormalization(), Flatten(),
        Dense(128, activation="relu"), Dropout(0.3),
        Dense(num_classes, activation="softmax"),
    ])
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model
