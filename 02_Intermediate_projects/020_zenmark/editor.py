import tkinter as tk
from tkinter import filedialog, messagebox
from tkhtmlview import HTMLLabel
import markdown2
from xhtml2pdf import pisa
import os

class ZenMark:
    def __init__(self, root):
        self.root = root
        self.root.title("ZenMark - Live Markdown Editor")
        self.root.geometry("1100x700")

        # Create Menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        
        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Export PDF", command=self.export_pdf)
        
        view_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_theme)

        # Main Split Screen
        self.paned = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashwidth=4, bg="#cccccc")
        self.paned.pack(fill=tk.BOTH, expand=True)

        # Left: Editor
        self.editor = tk.Text(self.paned, undo=True, font=("Menlo", 14), 
                              padx=10, pady=10, relief=tk.FLAT)
        self.paned.add(self.editor)

        # Right: Preview
        self.preview = HTMLLabel(self.paned, html="<h1>Live Preview</h1>", 
                                 padx=10, pady=10)
        self.paned.add(self.preview)

        # Status Bar
        self.status = tk.Label(root, text="Words: 0", anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Real-time binding
        self.editor.bind("<<Modified>>", self.on_content_changed)

    def on_content_changed(self, event=None):
        if self.editor.edit_modified():
            content = self.editor.get("1.0", tk.END)
            
            # Update Word Count
            words = len(content.split())
            self.status.config(text=f"Words: {words}")
            
            # Update HTML Preview
            html = markdown2.markdown(content)
            self.preview.set_html(html)
            
            self.editor.edit_modified(False)

    def save_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".md")
        if path:
            with open(path, "w") as f:
                f.write(self.editor.get("1.0", tk.END))

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Markdown", "*.md")])
        if path:
            with open(path, "r") as f:
                self.editor.delete("1.0", tk.END)
                self.editor.insert("1.0", f.read())

    def export_pdf(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf")
        if path:
            html = markdown2.markdown(self.editor.get("1.0", tk.END))
            with open(path, "wb") as f:
                pisa.CreatePDF(html, dest=f)
            messagebox.showinfo("ZenMark", "PDF Exported Successfully!")

    def toggle_theme(self):
        curr = self.editor.cget("background")
        if curr == "white" or curr == "SystemWindow":
            self.editor.config(bg="#1e1e1e", fg="#d4d4d4", insertbackground="white")
        else:
            self.editor.config(bg="white", fg="black", insertbackground="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZenMark(root)
    root.mainloop()