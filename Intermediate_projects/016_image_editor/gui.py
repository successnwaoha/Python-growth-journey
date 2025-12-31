import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import image_ops  # Importing your existing logic!

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Image Editor")
        self.root.geometry("800x600")

        # This will hold our "active" PIL image object
        self.current_image = None
        # This will hold the image shown on the screen
        self.display_image = None

        # --- UI LAYOUT ---
        
        # 1. Buttons Frame (Left side)
        self.controls_frame = tk.Frame(self.root, width=200, bg="#f0f0f0")
        self.controls_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Button(self.controls_frame, text="Open Image", command=self.load_file).pack(fill="x", pady=5)
        
        # Filter Buttons
        tk.Label(self.controls_frame, text="Filters", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Button(self.controls_frame, text="Grayscale", command=self.apply_grayscale).pack(fill="x", pady=2)
        tk.Button(self.controls_frame, text="Blur", command=self.apply_blur).pack(fill="x", pady=2)
        tk.Button(self.controls_frame, text="Rotate 90°", command=self.apply_rotate).pack(fill="x", pady=2)
        tk.Button(self.controls_frame, text="Reset to Original", command=self.reset_image, fg="red").pack(fill="x", pady=10)
        
        # Save Button
        tk.Button(self.controls_frame, text="Save As...", command=self.save_file, bg="green").pack(side="bottom", fill="x", pady=20)

        # 2. Image Display Area (Right side)
        self.canvas = tk.Label(self.root, text="No image loaded", bg="gray")
        self.canvas.pack(expand=True, fill="both", padx=10, pady=10)

    # --- FUNCTIONS ---

    def load_file(self):
        # FIX THE KEYWORD HERE:
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
        if file_path:
            self.current_image = image_ops.open_image(file_path)
            
            # This is our backup! We use .copy() to make it a separate object.
            self.original_image = self.current_image.copy() 
            
            self.show_preview()

    def show_preview(self):
        """Updates the GUI to show the current image."""
        if self.current_image:
            # We resize the preview so it fits the screen (don't worry, doesn't affect the save)
            preview_img = self.current_image.copy()
            preview_img.thumbnail((600, 500)) 
            
            # Convert PIL image to Tkinter-compatible photo
            self.display_image = ImageTk.PhotoImage(preview_img)
            self.canvas.config(image=self.display_image, text="")

    def apply_grayscale(self):
        if self.current_image:
            self.current_image = image_ops.grayscale_image(self.current_image)
            self.show_preview()

    def apply_blur(self):
        if self.current_image:
            self.current_image = image_ops.blur_image(self.current_image)
            self.show_preview()

    def apply_rotate(self):
        if self.current_image:
            # We call the 'rotate_image' function from your image_ops file
            self.current_image = image_ops.rotate_image(self.current_image, 90)
            self.show_preview()
    
    def save_file(self):
        if self.current_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".jpg")
            if save_path:
                image_ops.save_image(self.current_image, save_path)
                messagebox.showinfo("Success", "Image saved successfully!")
    
    def reset_image(self):
        # We check if 'original_image' exists yet
        if hasattr(self, 'original_image'):
            # Set the current image back to the backup
            self.current_image = self.original_image.copy()
            self.show_preview()

# Start the program
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()