import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import subprocess
import threading
import sys
import os

class ADBDeviceCheckerApp:
    def __init__(self, master):
        self.master = master
        master.title("ADB Device Checker")
        master.geometry("800x600") # Ukuran jendela awal
        master.configure(bg="#2E2E2E") # Dark background

        # Gaya modern dengan ttk
        self.style = ttk.Style()
        self.style.theme_use("clam") # 'clam', 'alt', 'default', 'classic'

        # Konfigurasi gaya untuk tombol
        self.style.configure("TButton",
                             font=("Segoe UI", 12, "bold"),
                             foreground="#FFFFFF", # White text
                             background="#4CAF50", # Green for active button
                             relief="flat",
                             padding=10)
        self.style.map("TButton",
                       background=[('active', '#45A049')]) # Darker green on hover

        # Konfigurasi gaya untuk frame
        self.style.configure("TFrame", background="#2E2E2E")

        # Konfigurasi gaya untuk label
        self.style.configure("TLabel",
                             font=("Segoe UI", 14),
                             foreground="#FFFFFF",
                             background="#2E2E2E")

        # --- Bagian Judul ---
        self.title_frame = ttk.Frame(master, padding="20 20 20 10")
        self.title_frame.pack(fill=tk.X)

        self.title_label = ttk.Label(self.title_frame, text="ADB Device Checker", font=("Segoe UI", 24, "bold"), foreground="#00BFFF") # Deep Sky Blue
        self.title_label.pack(pady=10)

        # --- Bagian Tombol ---
        self.button_frame = ttk.Frame(master, padding="10 10 10 20")
        self.button_frame.pack(fill=tk.X)

        self.check_button = ttk.Button(self.button_frame, text="Check ADB Devices", command=self.run_adb_check)
        self.check_button.pack(side=tk.LEFT, padx=10, expand=True)

        self.clear_button = ttk.Button(self.button_frame, text="Clear Log", command=self.clear_log, style="Clear.TButton")
        self.clear_button.pack(side=tk.RIGHT, padx=10, expand=True)

        # Konfigurasi gaya untuk tombol Clear (warna berbeda)
        self.style.configure("Clear.TButton",
                             background="#FF6347", # Tomato
                             foreground="#FFFFFF")
        self.style.map("Clear.TButton",
                       background=[('active', '#E5533A')])


        # --- Bagian Output Log Terminal ---
        self.log_frame = ttk.Frame(master, padding="10")
        self.log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_output = scrolledtext.ScrolledText(self.log_frame,
                                                    wrap=tk.WORD,
                                                    width=80,
                                                    height=20,
                                                    font=("Consolas", 14), # Font monospace untuk terminal
                                                    bg="#1E1E1E", # Darker background for log
                                                    fg="#00FF00", # Bright green text for log
                                                    insertbackground="#00FF00", # Cursor color
                                                    selectbackground="#3A3A3A", # Selection background
                                                    padx=10, pady=10)
        self.log_output.pack(fill=tk.BOTH, expand=True)
        self.log_output.config(state=tk.DISABLED) # Membuat log tidak bisa diedit

        # Menambahkan scrollbar ke log
        self.log_output.vbar.config(width=15, troughcolor="#2E2E2E", background="#555555") # Scrollbar styling

        self.update_log("Welcome to ADB Device Checker! Click 'Check ADB Devices' to begin.")
        self.update_log("Ensure ADB is installed and configured in your system's PATH.")

    def run_adb_check(self):
        self.update_log("\n--- Checking for ADB devices... ---")
        self.check_button.config(state=tk.DISABLED) # Disable button while checking
        threading.Thread(target=self._check_adb_devices_threaded).start()

    def _check_adb_devices_threaded(self):
        try:
            # Jalankan perintah adb devices
            # 'adb.exe' untuk Windows, 'adb' untuk Linux/macOS
            adb_command = "adb"
            if sys.platform == "win32":
                adb_command = "adb.exe"

            # Check if adb is in PATH
            if not self.is_adb_in_path(adb_command):
                self.update_log(f"Error: '{adb_command}' not found. Please ensure ADB is installed and added to your system's PATH environmental variable.")
                messagebox.showerror("ADB Not Found", f"'{adb_command}' not found. Please ensure ADB is installed and added to your system's PATH environmental variable.")
                self.check_button.config(state=tk.NORMAL)
                return

            process = subprocess.Popen([adb_command, "devices"],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       text=True, # Decode stdout/stderr as text
                                       encoding='utf-8') # Specify encoding

            stdout, stderr = process.communicate()

            if stdout:
                self.update_log(stdout)
            if stderr:
                self.update_log(f"Error: {stderr}")
                messagebox.showerror("ADB Error", f"An error occurred while running ADB:\n{stderr}")

        except FileNotFoundError:
            self.update_log(f"Error: ADB command not found. Make sure ADB is installed and added to your system's PATH.")
            messagebox.showerror("Error", "ADB command not found. Please ensure ADB is installed and added to your system's PATH.")
        except Exception as e:
            self.update_log(f"An unexpected error occurred: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        finally:
            self.check_button.config(state=tk.NORMAL) # Re-enable button

    def is_adb_in_path(self, adb_command):
        """Checks if the adb command is executable and in the system's PATH."""
        if sys.platform == "win32":
            # On Windows, check for .exe directly or rely on PATHEXT
            try:
                subprocess.run([adb_command, "version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False
        else:
            # On Linux/macOS, use 'which' or 'command -v'
            try:
                subprocess.run(["which", adb_command], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False


    def update_log(self, message):
        self.log_output.config(state=tk.NORMAL) # Enable editing
        self.log_output.insert(tk.END, message + "\n")
        self.log_output.see(tk.END) # Scroll to the end
        self.log_output.config(state=tk.DISABLED) # Disable editing

    def clear_log(self):
        self.log_output.config(state=tk.NORMAL)
        self.log_output.delete(1.0, tk.END)
        self.log_output.config(state=tk.DISABLED)
        self.update_log("Log cleared.")

def main():
    root = tk.Tk()
    app = ADBDeviceCheckerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()