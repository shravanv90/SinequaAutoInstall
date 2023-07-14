import os
import subprocess
import zipfile
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from time import sleep

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(padx=10, pady=10)  # Add padding to the entire grid
        self.create_widgets()

    def create_widgets(self):
        self.label_zip = tk.Label(self, text="Zip File Path")
        self.label_zip.pack(pady=10)
        self.entry_zip = tk.Entry(self)
        self.entry_zip.pack(pady=10)
        self.entry_zip.insert(0, "sinequa.11.zip")

        self.label_extract = tk.Label(self, text="Extract Path")
        self.label_extract.pack(pady=10)
        self.entry_extract = tk.Entry(self)
        self.entry_extract.pack(pady=10)
        self.entry_extract.insert(0, "C:\\")

        self.install_button = tk.Button(self)
        self.install_button["text"] = "Install Sinequa"
        self.install_button["command"] = self.install_sinequa
        self.install_button.pack(side="top", pady=20)

        self.progress = ttk.Progressbar(self, orient='horizontal', length=300, mode='determinate')
        self.progress.pack(side="top", pady=10)

        self.log = scrolledtext.ScrolledText(self, state='disabled', width=50, height=20)
        self.log.pack(side="top", pady=10)

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom", pady=10)


    def install_sinequa(self):
        zip_path = self.entry_zip.get()
        extract_path = self.entry_extract.get()
        install_path = os.path.join(extract_path, 'sinequa')

        # Stop the service
        service_path = os.path.join(install_path, 'website', 'bin')
        os.chdir(service_path)
        self.log_insert('Stopping Sinequa service...')
        subprocess.run(["scmd", "StopAll"])
        sleep(5)  # give the service time to stop

        # Extract the files
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            total_files = len(zip_ref.infolist())
            self.log_insert(f'Starting extraction of {total_files} files')
            for index, file in enumerate(zip_ref.infolist(), start=1):
                try:
                    zip_ref.extract(file, extract_path)
                except Exception as e:
                    self.log_insert(f'Error extracting file {file.filename}: {str(e)}')
                    continue
                if index % 100 == 0:  # update progress every 100 files
                    self.progress['value'] = index / total_files * 100
                    self.log_insert(f'Extracted {index}/{total_files} files')
                    self.update()
            self.log_insert('Extraction complete.')

        # Start the service
        self.log_insert('Starting Sinequa service...')
        subprocess.run(["scmd", "StartAll"])
        self.log_insert('Sinequa service started')

    def log_insert(self, message):
        self.log['state'] = 'normal'
        self.log.insert('end', message + '\n')
        self.log['state'] = 'disabled'

root = tk.Tk()
app = Application(master=root)
app.mainloop()
