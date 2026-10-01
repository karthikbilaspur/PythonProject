import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageEnhance, ImageFilter, ImageTk
import torch

# Lazy imports to ensure fast app initialization
try:
    from diffusers import StableDiffusionPipeline
    HAS_DIFFUSERS = True
except ImportError:
    HAS_DIFFUSERS = False

try:
    from transformers import DALLETokenizer, DALLForConditionalGeneration
    HAS_DALLE = True
except ImportError:
    HAS_DALLE = False


class ImageGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Multi-Model Image Generator & Editor")
        self.root.geometry("650x850")

        # Models & Pipelines Cache
        self.sd_pipe = None
        self.dalle_model = None
        self.dalle_tokenizer = None

        # Image state tracking
        self.original_image: Image.Image | None = None
        self.current_image: Image.Image | None = None
        self.tk_image = None

        # --- Top Controls Frame ---
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(top_frame, text="Prompt:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.prompt_entry = tk.Entry(top_frame, width=70)
        self.prompt_entry.pack(fill="x", pady=5)
        self.prompt_entry.insert(0, "a cute cat astronaut, high quality")

        # Model Selector Row
        controls_row = tk.Frame(top_frame)
        controls_row.pack(fill="x", pady=5)

        tk.Label(controls_row, text="Model: ").pack(side="left")
        self.model_var = tk.StringVar(value="Stable Diffusion")
        self.model_selector = ttk.Combobox(
            controls_row,
            textvariable=self.model_var,
            values=["Stable Diffusion", "DALL-E Mini"],
            state="readonly",
            width=20,
        )
        self.model_selector.pack(side="left", padx=5)

        self.generate_button = tk.Button(
            controls_row,
            text="Generate Image",
            command=self.start_generation_thread,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 9, "bold"),
        )
        self.generate_button.pack(side="left", padx=10)

        # Status indicator
        self.status_label = tk.Label(top_frame, text="Ready", fg="gray")
        self.status_label.pack(anchor="w", pady=2)

        # --- Display Area ---
        self.image_label = tk.Label(
            self.root, text="Generated image will appear here", bg="#E0E0E0", height=20
        )
        self.image_label.pack(pady=10, padx=10, fill="both", expand=True)

        # --- Integrated Image Adjustments Frame ---
        self.enhance_frame = tk.LabelFrame(self.root, text="Image Enhancements")
        self.enhance_frame.pack(pady=10, padx=10, fill="x")

        # Brightness Slider
        tk.Label(self.enhance_frame, text="Brightness:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        self.brightness_slider = tk.Scale(
            self.enhance_frame,
            from_=0.2,
            to=2.0,
            resolution=0.1,
            orient="horizontal",
            command=self.apply_enhancements,
        )
        self.brightness_slider.set(1.0)
        self.brightness_slider.grid(row=0, column=1, fill="x", expand=True, padx=5)

        # Contrast Slider
        tk.Label(self.enhance_frame, text="Contrast:").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        self.contrast_slider = tk.Scale(
            self.enhance_frame,
            from_=0.2,
            to=2.0,
            resolution=0.1,
            orient="horizontal",
            command=self.apply_enhancements,
        )
        self.contrast_slider.set(1.0)
        self.contrast_slider.grid(row=1, column=1, fill="x", expand=True, padx=5)

        # --- Bottom Action Buttons ---
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10, padx=10, fill="x")

        self.edit_button = tk.Button(
            btn_frame, text="Open Advanced Editor", command=self.edit_image, state="disabled"
        )
        self.edit_button.pack(side="left", padx=5)

        self.save_button = tk.Button(
            btn_frame,
            text="Save Image",
            command=self.save_image,
            state="disabled",
            bg="#2196F3",
            fg="white",
        )
        self.save_button.pack(side="right", padx=5)

    def start_generation_thread(self):
        """Dispatches generation task to a thread to keep the UI responsive."""
        prompt = self.prompt_entry.get().strip()
        if not prompt:
            messagebox.showwarning("Warning", "Please enter a prompt first.")
            return

        self.generate_button.config(state="disabled")
        self.status_label.config(text="Generating image... Please wait.", fg="blue")

        threading.Thread(target=self.generate_image, args=(prompt,), daemon=True).start()

    def generate_image(self, prompt: str):
        selected_model = self.model_var.get()
        try:
            if selected_model == "DALL-E Mini":
                if not HAS_DALLE:
                    raise ImportError("Transformers package is required for DALL-E Mini.")
                raw_image = self.generate_dalle_image(prompt)
            else:
                if not HAS_DIFFUSERS:
                    raise ImportError("Diffusers package is required for Stable Diffusion.")
                raw_image = self.generate_stable_diffusion_image(prompt)

            # Update GUI from background thread
            self.root.after(0, self.update_generated_image, raw_image)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Generation Error", str(e)))
            self.root.after(0, lambda: self.status_label.config(text="Generation failed.", fg="red"))
        finally:
            self.root.after(0, lambda: self.generate_button.config(state="normal"))

    def generate_dalle_image(self, prompt: str) -> Image.Image:
        if self.dalle_model is None or self.dalle_tokenizer is None:
            self.dalle_model = DALLForConditionalGeneration.from_pretrained('dalle-mini/dalle-mini')
            self.dalle_tokenizer = DALLETokenizer.from_pretrained('dalle-mini/dalle-mini')

        inputs = self.dalle_tokenizer(prompt, return_tensors='pt')
        outputs = self.dalle_model.generate(**inputs, num_beams=4, no_repeat_ngram_size=2, early_stopping=True)
        return self.dalle_model.decode(outputs[0], force_batch=True)

    def generate_stable_diffusion_image(self, prompt: str) -> Image.Image:
        if self.sd_pipe is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            torch_dtype = torch.float16 if device == "cuda" else torch.float32

            model_id = "CompVis/stable-diffusion-v1-4"
            self.sd_pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch_dtype)
            self.sd_pipe = self.sd_pipe.to(device)

        return self.sd_pipe(prompt).images[0]

    def update_generated_image(self, img: Image.Image):
        """Sets internal image references and updates UI display."""
        self.original_image = img
        self.current_image = img.copy()

        # Reset Sliders
        self.brightness_slider.set(1.0)
        self.contrast_slider.set(1.0)

        self.display_image(self.current_image)
        self.status_label.config(text="Image generated successfully!", fg="green")
        self.save_button.config(state="normal")
        self.edit_button.config(state="normal")

    def display_image(self, img: Image.Image = None):
        """Displays image resized safely for window boundaries."""
        target_img = img if img is not None else self.current_image
        if target_img is None:
            return

        display_copy = target_img.copy()
        display_copy.thumbnail((500, 500))

        self.tk_image = ImageTk.PhotoImage(display_copy)
        self.image_label.config(image=self.tk_image, text="")

    def apply_enhancements(self, _=None):
        """Applies brightness and contrast live adjustments on main image."""
        if self.original_image is None:
            return

        edited = self.original_image.copy()
        brightness = self.brightness_slider.get()
        contrast = self.contrast_slider.get()

        if brightness != 1.0:
            edited = ImageEnhance.Brightness(edited).enhance(brightness)
        if contrast != 1.0:
            edited = ImageEnhance.Contrast(edited).enhance(contrast)

        self.current_image = edited
        self.display_image(self.current_image)

    def save_image(self):
        if self.current_image is None:
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("All Files", "*.*")],
        )
        if filename:
            self.current_image.save(filename)
            messagebox.showinfo("Success", f"Image saved successfully to:\n{filename}")

    def edit_image(self):
        """Modal window for manual adjustments."""
        if self.current_image is None:
            return

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Advanced Edit")
        edit_window.geometry("300x200")

        tk.Label(edit_window, text="Brightness:").pack(pady=(10, 0))
        b_slider = tk.Scale(edit_window, from_=0.2, to=2.0, resolution=0.1, orient="horizontal")
        b_slider.set(self.brightness_slider.get())
        b_slider.pack(fill="x", padx=15)

        tk.Label(edit_window, text="Contrast:").pack(pady=(10, 0))
        c_slider = tk.Scale(edit_window, from_=0.2, to=2.0, resolution=0.1, orient="horizontal")
        c_slider.set(self.contrast_slider.get())
        c_slider.pack(fill="x", padx=15)

        def apply_edit():
            self.brightness_slider.set(b_slider.get())
            self.contrast_slider.set(c_slider.get())
            self.apply_enhancements()
            edit_window.destroy()

        apply_button = tk.Button(edit_window, text="Apply Changes", command=apply_edit, bg="#4CAF50", fg="white")
        apply_button.pack(pady=15)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ImageGenerator()
    app.run()
    