import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import torch
from transformers import DALLForConditionalGeneration, DALLETokenizer
from diffusers import StableDiffusionPipeline

class ImageGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Generator")
        self.model = None
        self.tokenizer = None
        self.image = None

        # Create UI elements
        self.prompt_label = tk.Label(self.root, text="Prompt:")
        self.prompt_entry = tk.Entry(self.root, width=50)
        self.generate_button = tk.Button(self.root, text="Generate", command=self.generate_image)
        self.save_button = tk.Button(self.root, text="Save", command=self.save_image)
        self.edit_button = tk.Button(self.root, text="Edit", command=self.edit_image)

        # Layout UI elements
        self.prompt_label.pack()
        self.prompt_entry.pack()
        self.generate_button.pack()
        self.save_button.pack()
        self.edit_button.pack()

    def generate_image(self):
        prompt = self.prompt_entry.get()
        if self.model == "DALL-E Mini":
            self.image = self.generate_dalle_image(prompt)
        elif self.model == "Stable Diffusion":
            self.image = self.generate_stable_diffusion_image(prompt)
        self.display_image()

    def generate_dalle_image(self, prompt):
        # Load DALL-E Mini model and tokenizer
        model = DALLForConditionalGeneration.from_pretrained('dalle-mini/dalle-mini')
        tokenizer = DALLETokenizer.from_pretrained('dalle-mini/dalle-mini')

        # Tokenize prompt
        inputs = tokenizer(prompt, return_tensors='pt')

        # Generate image
        outputs = model.generate(**inputs, num_beams=4, no_repeat_ngram_size=2, early_stopping=True)

        # Decode generated image
        image = model.decode(outputs[0], force_batch=True)

        return image

    def generate_stable_diffusion_image(self, prompt):
        # Load Stable Diffusion model
        model_id = "CompVis/stable-diffusion-v1-4"
        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)

        # Generate image
        image = pipe(prompt).images[0]

        return image

    def display_image(self):
        # Display generated image
        image_tk = ImageTk.PhotoImage(self.image)
        image_label = tk.Label(self.root, image=image_tk)
        image_label.image = image_tk
        image_label.pack()

    def save_image(self):
        # Save generated image
        filename = filedialog.asksaveasfilename(defaultextension=".png")
        self.image.save(filename)

    def edit_image(self):
        # Edit generated image
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Image")

        # Create edit options
        brightness_label = tk.Label(edit_window, text="Brightness:")
        brightness_slider = tk.Scale(edit_window, from tkinter import DoubleVar
        brightness_slider.pack()
        brightness_slider.set(1.0)

        contrast_label = tk.Label(edit_window, text="Contrast:")
        contrast_slider = tk.Scale(edit_window, from tkinter import DoubleVar
        contrast_slider.pack()
        contrast_slider.set(1.0)

        def apply_edit():
            edited_image = self.image.copy()
            edited_image = ImageEnhance.Brightness(edited_image).enhance(brightness_slider.get())
            edited_image = ImageEnhance.Contrast(edited_image).enhance(contrast_slider.get())
            self.image = edited_image
            self.display_image()

        apply_button = tk.Button(edit_window, text="Apply", command=apply_edit)
        apply_button.pack()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ImageGenerator()
    app.model = "DALL-E Mini"
    app.run()