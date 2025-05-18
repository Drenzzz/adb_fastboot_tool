import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import os

class ADBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ADB Menu")
        self.root.geometry("600x400")
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title label
        self.title_label = ttk.Label(self.main_frame, text="ADB Menu", font=("Arial", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Button to check ADB devices
        self.check_button = ttk.Button(self.main_frame, text="Check ADB Devices", command=self.check_adb_devices)
        self.check_button.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Text area to display output
        self.output_text = scrolledtext.ScrolledText(self.main_frame, height=15, width=60, wrap=tk.WORD)
        self.output_text.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Exit button
        self.exit_button = ttk.Button(self.main_frame, text="Exit", command=self.root.quit)
        self.exit_button.grid(row=3, column=0, columnspan=2, pady=10)
    
    def check_adb_devices(self):
        """Run adb devices command and display output"""
        self.output_text.delete(1.0, tk.END)  # Clear previous output
        try:
            result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
            self.output_text.insert(tk.END, result.stdout)
        except subprocess.CalledProcessError as e:
            self.output_text.insert(tk.END, f"Error: {e.stderr}")
        except FileNotFoundError:
            self.output_text.insert(tk.END, "Error: ADB not found. Ensure ADB is installed and added to PATH.")

def main():
    root = tk.Tk()
    app = ADBApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()