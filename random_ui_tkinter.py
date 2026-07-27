#!/usr/bin/env python3
"""
Random Number Generator GUI using Tkinter.
A clean, modern desktop application for generating random integers.

Run: python random_ui_tkinter.py
"""
import os
import tkinter as tk
from tkinter import ttk, messagebox
import random
import datetime

APP_TITLE = "Random Number Generator"

class RNGApp(tk.Tk):
    """Main Application Window for the Random Number Generator."""
    
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.resizable(False, False)
        
        # Configure a clean background and padding for the main window
        self.configure(padx=20, pady=20, bg="#f3f4f6")
        self.history = []

        self._setup_styles()
        self._build_ui()

    def _setup_styles(self):
        """Configure ttk styles to achieve a modern, clean look."""
        style = ttk.Style(self)
        try:
            # Attempt to use a cleaner theme if available (Windows native)
            style.theme_use("vista")
        except tk.TclError:
            try:
                style.theme_use("clam")
            except tk.TclError:
                pass
                
        # Main background for frames
        style.configure("TFrame", background="#f3f4f6")
        style.configure("TLabel", background="#f3f4f6", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#111827")
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10), foreground="#6b7280")
        
        # Result Card styles
        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure("Result.TLabel", background="#ffffff", font=("Segoe UI", 28, "bold"), foreground="#2563eb")
        
        # Primary Action Button
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"))
        
    def _build_ui(self):
        """Construct the user interface components."""
        
        # --- Header Section ---
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Logo
        try:
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
            self.logo_img = tk.PhotoImage(file=logo_path)
            logo_label = ttk.Label(header_frame, image=self.logo_img)
            logo_label.pack(side="left", padx=(0, 15))
        except Exception:
            pass # fallback if logo not found
            
        text_frame = ttk.Frame(header_frame)
        text_frame.pack(side="left", fill="x")
        
        ttk.Label(text_frame, text="Randomize.", style="Header.TLabel").pack(anchor="w")
        ttk.Label(text_frame, text="Enter a range to generate a random integer.", style="Subtitle.TLabel").pack(anchor="w")

        # --- Input Section ---
        input_frame = ttk.Frame(self)
        input_frame.pack(fill="x", pady=(0, 15))
        
        # Min Input
        min_frame = ttk.Frame(input_frame)
        min_frame.pack(side="left", padx=(0, 15))
        ttk.Label(min_frame, text="Minimum").pack(anchor="w")
        self.min_var = tk.StringVar()
        self.entry_min = ttk.Entry(min_frame, textvariable=self.min_var, width=15, font=("Segoe UI", 11))
        self.entry_min.pack()
        self.entry_min.bind("<Return>", lambda e: self.generate())
        
        # Max Input
        max_frame = ttk.Frame(input_frame)
        max_frame.pack(side="left")
        ttk.Label(max_frame, text="Maximum").pack(anchor="w")
        self.max_var = tk.StringVar()
        self.entry_max = ttk.Entry(max_frame, textvariable=self.max_var, width=15, font=("Segoe UI", 11))
        self.entry_max.pack()
        self.entry_max.bind("<Return>", lambda e: self.generate())
        
        # --- Actions Section ---
        action_frame = ttk.Frame(self)
        action_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Button(action_frame, text="Swap", command=self.swap_values, width=8).pack(side="left", padx=(0, 5))
        ttk.Button(action_frame, text="Random Range", command=self.randomize_range, width=15).pack(side="left")
        
        self.generate_btn = ttk.Button(action_frame, text="Generate", command=self.generate, style="Primary.TButton")
        self.generate_btn.pack(side="right")

        # --- Result Section ---
        self.result_frame = tk.Frame(self, bg="#ffffff", bd=1, relief="solid", highlightbackground="#e5e7eb", highlightcolor="#e5e7eb")
        self.result_frame.pack(fill="x", pady=(0, 20), ipady=15)
        
        # Wrapper for internal padding inside result_frame
        inner_res = tk.Frame(self.result_frame, bg="#ffffff")
        inner_res.pack(fill="both", expand=True, padx=20)
        
        self.result_label = ttk.Label(inner_res, text="—", style="Result.TLabel")
        self.result_label.pack(side="left")
        
        ttk.Button(inner_res, text="Copy", command=self.copy_result).pack(side="right", anchor="center")

        # --- History Section ---
        hist_header = ttk.Frame(self)
        hist_header.pack(fill="x", pady=(0, 5))
        ttk.Label(hist_header, text="Recent Generations", font=("Segoe UI", 10, "bold")).pack(side="left")
        ttk.Button(hist_header, text="Clear", command=self.clear_history).pack(side="right")

        self.history_box = tk.Listbox(
            self, 
            height=6, 
            width=50, 
            font=("Segoe UI", 9), 
            bg="#ffffff", 
            fg="#374151", 
            relief="solid",
            bd=1,
            highlightthickness=0,
            selectbackground="#2563eb"
        )
        self.history_box.pack(fill="x")

        # Watermark
        ttk.Label(self, text="Created by Somashankar", font=("Segoe UI", 8), foreground="#9ca3af", background="#f3f4f6").pack(side="bottom", anchor="se", pady=(5, 0))

        # Set focus to min entry initially
        self.entry_min.focus()

    def validate_inputs(self):
        """Validate the minimum and maximum input fields."""
        min_s = self.min_var.get().strip()
        max_s = self.max_var.get().strip()
        
        if not min_s or not max_s:
            messagebox.showerror("Invalid Input", "Please enter both minimum and maximum values.")
            return None
            
        try:
            minimum = int(min_s)
            maximum = int(max_s)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integer numbers.")
            return None
            
        if minimum > maximum:
            messagebox.showerror("Invalid Range", "Minimum cannot be greater than maximum.")
            return None
            
        return minimum, maximum

    def generate(self):
        """Generate a random number based on validated inputs."""
        validated = self.validate_inputs()
        if not validated:
            return
            
        minimum, maximum = validated
        value = random.randint(minimum, maximum)
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Update result display
        self.result_label.config(text=str(value))
        
        # Prepend to history
        hist_str = f"{value}  [Range: {minimum}–{maximum}]  •  {timestamp}"
        self.history.insert(0, hist_str)
        self.update_history_box()

    def copy_result(self):
        """Copy the generated result to clipboard."""
        txt = self.result_label.cget("text")
        if txt and txt != "—":
            self.clipboard_clear()
            self.clipboard_append(txt)
            messagebox.showinfo("Success", f"Copied '{txt}' to clipboard.")
        else:
            messagebox.showwarning("No Value", "Generate a value first.")

    def update_history_box(self):
        """Refresh the history Listbox from the internal history list."""
        self.history_box.delete(0, tk.END)
        # Display only up to the last 20 items
        for item in self.history[:20]:
            self.history_box.insert(tk.END, item)

    def clear_history(self):
        """Clear the generation history."""
        self.history.clear()
        self.update_history_box()

    def swap_values(self):
        """Swap the contents of the minimum and maximum inputs."""
        a = self.min_var.get()
        b = self.max_var.get()
        self.min_var.set(b)
        self.max_var.set(a)

    def randomize_range(self):
        """Fill minimum and maximum inputs with random sensible integers."""
        a = random.randint(-100, 1000)
        b = random.randint(-100, 1000)
        self.min_var.set(str(min(a, b)))
        self.max_var.set(str(max(a, b)))

if __name__ == "__main__":
    app = RNGApp()
    app.mainloop()