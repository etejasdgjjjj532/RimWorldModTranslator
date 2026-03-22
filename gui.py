import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from translator import RimWorldModTranslator
import os

class RimWorldTranslatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RimWorld Mod Translator GUI")
        self.root.geometry("600x400")
        
        # Styles
        style = ttk.Style()
        style.configure("TButton", padding=5)
        
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Mod Path
        ttk.Label(main_frame, text="Mod Folder Path:").pack(anchor=tk.W)
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.path_var = tk.StringVar()
        ttk.Entry(path_frame, textvariable=self.path_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(path_frame, text="Browse", command=self.browse_folder).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Options
        self.xlsx_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Export to Excel (.xlsx)", variable=self.xlsx_var).pack(anchor=tk.W)
        
        self.merge_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(main_frame, text="Merge with existing translations", variable=self.merge_var).pack(anchor=tk.W)
        
        # Run Button
        self.run_btn = ttk.Button(main_frame, text="Run Extraction", command=self.start_extraction)
        self.run_btn.pack(pady=20)
        
        # Log Output
        ttk.Label(main_frame, text="Status Log:").pack(anchor=tk.W)
        self.log_text = tk.Text(main_frame, height=10, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_var.set(folder)

    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "
")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def start_extraction(self):
        mod_path = self.path_var.get()
        if not mod_path or not os.path.exists(mod_path):
            messagebox.showerror("Error", "Please select a valid Mod folder.")
            return
        
        self.run_btn.config(state=tk.DISABLED)
        self.log("Starting extraction...")
        
        # Run in thread to keep GUI responsive
        thread = threading.Thread(target=self.run_process, args=(mod_path,))
        thread.start()

    def run_process(self, mod_path):
        try:
            translator = RimWorldModTranslator(
                mod_path=mod_path,
                output_path="./output",
                merge_existing=self.merge_var.get()
            )
            
            if self.xlsx_var.get():
                self.log("Exporting to Excel...")
                translator.export_to_xlsx()
                self.log("Excel export complete.")
            else:
                self.log("Generating XML templates...")
                translator.generate_xml_templates()
                self.log("XML generation complete.")
                
            self.log("Processing finished successfully.")
            messagebox.showinfo("Success", "Extraction complete! Check the 'output' folder.")
        except Exception as e:
            self.log(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.root.after(0, lambda: self.run_btn.config(state=tk.NORMAL))

if __name__ == "__main__":
    root = tk.Tk()
    app = RimWorldTranslatorGUI(root)
    root.mainloop()
