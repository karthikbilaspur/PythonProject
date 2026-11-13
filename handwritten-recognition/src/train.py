# pyright: reportMissingImports=false, reportMissingTypeStubs=false
# pyright: reportUnknownVariableType=false, reportUnknownMemberType=false, reportUnknownArgumentType=false

from collections.abc import Iterable
from pathlib import Path
from typing import Any, cast

import numpy as np
from numpy.typing import NDArray
import tensorflow_datasets as tfds  # type: ignore[import-not-found]
from tensorflow.keras.datasets import mnist  # type: ignore[import-not-found]
from tensorflow.keras.preprocessing.image import ImageDataGenerator  # type: ignore[import-not-found]
from tensorflow.keras.callbacks import (  # type: ignore[import-not-found]
    Callback,
    EarlyStopping,
    ModelCheckpoint,
)
from src.model import build_model
from src.preprocessing import preprocess_for_training


Array = NDArray[Any]
Dataset = tuple[Array, Array]
DatasetSplits = tuple[Dataset, Dataset]


def load_mnist() -> DatasetSplits:
    return cast(DatasetSplits, mnist.load_data())


def load_emnist_letters() -> DatasetSplits:
    def _to_numpy(split: str) -> Dataset:
        ds = cast(Any, tfds.load)("emnist/letters", split=split, as_supervised=True)
        imgs, labels = [], []
        examples = cast(
            Iterable[tuple[Array, Any]], cast(Any, tfds.as_numpy)(ds)
        )
        for img, lab in examples:
            imgs.append(np.array(img).squeeze())
            labels.append(int(lab))
        x: Array = np.stack(imgs)
        y: Array = np.array(labels)
        x = np.transpose(x, (0, 2, 1))
        y = y - 1
        return x, y

    return _to_numpy("train"), _to_numpy("test")


def load_combined() -> DatasetSplits:
    (mx_tr, my_tr), (mx_te, my_te) = load_mnist()
    (ex_tr, ey_tr), (ex_te, ey_te) = load_emnist_letters()
    ey_tr = ey_tr + 10; ey_te = ey_te + 10
    x_train = np.concatenate([mx_tr, ex_tr]); y_train = np.concatenate([my_tr, ey_tr])
    x_test = np.concatenate([mx_te, ex_te]); y_test = np.concatenate([my_te, ey_te])
    idx = np.random.permutation(len(x_train)); x_train, y_train = x_train[idx], y_train[idx]
    idx = np.random.permutation(len(x_test)); x_test, y_test = x_test[idx], y_test[idx]
    return (x_train, y_train), (x_test, y_test)


def train_and_save(
    x_train: Array,
    y_train: Array,
    x_test: Array,
    y_test: Array,
    num_classes: int,
    save_path: str | Path,
    epochs: int = 12,
    batch_size: int = 128,
) -> Any:
    x_train_p: Array = preprocess_for_training(x_train)
    x_test_p: Array = preprocess_for_training(x_test)
    model = build_model(num_classes)
    datagen: Any = cast(Any, ImageDataGenerator)(
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.1,
    )
    datagen.fit(x_train_p)
    callbacks: list[Callback] = [
        EarlyStopping(
            monitor="val_accuracy", patience=3, restore_best_weights=True
        ),
        ModelCheckpoint(
            str(save_path),
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1,
        ),
    ]
    batches: Any = datagen.flow(x_train_p, y_train, batch_size=batch_size)
    model.fit(
        batches,
        epochs=epochs,
        validation_data=(x_test_p, y_test),
        callbacks=callbacks,
        verbose=1,
    )
    _, acc = model.evaluate(x_test_p, y_test, verbose=0)
    print(f"Test accuracy: {acc:.4f}")
    model.save(str(save_path))
    return model
