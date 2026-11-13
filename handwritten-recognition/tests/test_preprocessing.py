import numpy as np, pytest
from PIL import Image
from src.preprocessing import preprocess_canvas_list, preprocess_pil_image
def test_canvas_280():
    img = np.full((280*280,), 255, dtype=float); img[100*280+100] = 0
    out = preprocess_canvas_list(img.tolist()); assert out.shape == (1,28,28,1); assert out.max() <= 1.0
def test_canvas_28():
    out = preprocess_canvas_list([255.0]*(28*28)); assert out.shape == (1,28,28,1)
def test_bad_size():
    with pytest.raises(ValueError): preprocess_canvas_list([0]*100)
def test_pil():
    out = preprocess_pil_image(Image.new("L", (100,100), color=255)); assert out.shape == (1,28,28,1)
