import argparse
from config import COMBINED_MODEL_PATH, EPOCHS, BATCH_SIZE
from src.train import load_combined, train_and_save
if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--epochs", type=int, default=EPOCHS); p.add_argument("--batch-size", type=int, default=BATCH_SIZE); a = p.parse_args()
    (x_tr, y_tr), (x_te, y_te) = load_combined()
    train_and_save(x_tr, y_tr, x_te, y_te, 36, COMBINED_MODEL_PATH, epochs=a.epochs, batch_size=a.batch_size)
