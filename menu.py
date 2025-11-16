import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from pathlib import Path

CONFIG_DIR = "configs"

class NexusMenu:
    def __init__(self, on_attach, on_update, on_panic):
        self.root = tk.Tk()
        self.root.title("NEXUS EXTERNAL v4.1")
        self.root.geometry("500x700")
        self.root.configure(bg="#1a1a1a")
        self.root.attributes("-topmost", True)
        self.on_attach = on_attach
        self.on_update = on_update
        self.on_panic = on_panic
        self.build_menu()
    
    def build_menu(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#1a1a1a", foreground="#ffffff")
        
        title = tk.Label(self.root, text="🔥 NEXUS v4.1 🔥", font=('Arial', 16, 'bold'), bg="#1a1a1a", fg="#00ff00")
        title.pack(pady=10)
        
        status = tk.Label(self.root, text="❌ Not Attached", bg="#1a1a1a", fg="#ff4444")
        status.pack(pady=5)
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Visuals Tab
        visuals = ttk.Frame(notebook)
        notebook.add(visuals, text="🎨 Visuals")
        ttk.Checkbutton(visuals, text="☐ ESP Box").pack(anchor="w", padx=20, pady=2)
        ttk.Checkbutton(visuals, text="👤 Names").pack(anchor="w", padx=20, pady=2)
        # Add more...
        
        # Combat Tab
        combat = ttk.Frame(notebook)
        notebook.add(combat, text="⚔️ Combat")
        ttk.Checkbutton(combat, text="🎯 Aimbot").pack(anchor="w", padx=20, pady=2)
        # Sliders for FOV/Smooth...
        
        # Movement Tab
        movement = ttk.Frame(notebook)
        notebook.add(movement, text="🚀 Movement")
        ttk.Checkbutton(movement, text="⚡ SpeedWalk").pack(anchor="w", padx=20, pady=2)
        # Sliders...
        
        # Configs Tab
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text="💾 Configs")
        ttk.Button(config_frame, text="💾 Save", command=self.save_config).pack(pady=5)
        ttk.Button(config_frame, text="📂 Load", command=self.load_config).pack(pady=5)
        
        btn_frame = tk.Frame(self.root, bg="#1a1a1a")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="🔗 Attach", command=self.on_attach).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔄 Update", command=self.on_update).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="❌ Panic", command=self.on_panic).pack(side=tk.LEFT, padx=5)
    
    def save_config(self):
        name = filedialog.asksaveasfilename(defaultextension=".json", initialdir=CONFIG_DIR)
        if name:
            # Save logic
            pass
    
    def load_config(self):
        name = filedialog.askopenfilename(initialdir=CONFIG_DIR)
        if name:
            # Load logic
            pass
    
    def run(self):
        self.root.mainloop()