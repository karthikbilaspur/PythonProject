from src.model import build_model
def test_build_10(): assert build_model(10).output_shape == (None, 10)
def test_build_26(): assert build_model(26).output_shape == (None, 26)
def test_build_36():
    m = build_model(36); assert m.output_shape == (None, 36); assert m.input_shape == (None, 28, 28, 1)
