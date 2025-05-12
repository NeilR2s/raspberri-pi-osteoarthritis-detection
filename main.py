import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import os
import subprocess
import shutil
import threading
# import spidev
import numpy as np
import cv2
from PIL import Image, ImageTk
import inference


# Directory to store notes
NOTES_DIR = "notes"
STORAGE_DIR = "storage_folders"

class BasePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        top_bar = tk.Frame(self, bg="white")
        top_bar.pack(fill="x", anchor="n")

        

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="white")
        self.bind("<Escape>", lambda e: self.destroy())

        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (MainMenu, StoragePage, NotesPage, AboutPage, InferencePage):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.place(relwidth=1, relheight=1)

        self.after(100, lambda: self.attributes("-fullscreen", True))  # Delayed fullscreen
        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        self.frames[page_name].tkraise()

    def open_storage(self):
        self.show_frame("StoragePage")

    def open_notes(self):
        self.show_frame("NotesPage")

    def open_about(self):
        self.show_frame("AboutPage")

    def open_gallery(self):
        print("Opening Gallery...")

# class DisplayPage(BasePage):
#     def __init__(self, parent, controller):
#         super().__init__(parent, controller)
#         self.controller = controller
#         self.running = True
#         self.last_frame = None

#         title = tk.Label(self, text="Display Page", font=("Helvetica", 24, "bold"), bg="white")
#         title.pack(pady=10)

#         self.video_label = tk.Label(self, bg="black")
#         self.video_label.pack(pady=10)

#         button_frame = tk.Frame(self, bg="white")
#         button_frame.pack(pady=10)

#         capture_btn = tk.Button(button_frame, text="Capture", font=("Helvetica", 14), width=12, command=self.capture_image)
#         capture_btn.grid(row=0, column=0, padx=10)

#         back_btn = tk.Button(self, text="Back", font=("Helvetica", 12), command=self.go_back)
#         back_btn.pack(pady=10)

#         self.cap_thread = threading.Thread(target=self.update_video)
#         self.cap_thread.daemon = True
#         self.cap_thread.start()

#     def update_video(self):
#         spi = spidev.SpiDev()
#         spi.open(0, 0)
#         spi.max_speed_hz = 20000000

#         def read_frame():
#             frame = np.zeros((60, 80), dtype=np.uint16)
#             valid_rows = 0
#             retries = 0
#             while valid_rows < 60:
#                 packet = spi.readbytes(164)
#                 if len(packet) != 164:
#                     continue
#                 if packet[0] & 0x0F == 0x0F:
#                     retries += 1
#                     if retries > 100:
#                         return None
#                     continue
#                 row_number = packet[1]
#                 if row_number < 60:
#                     row_data = np.frombuffer(bytearray(packet[4:]), dtype='>u2')
#                     frame[row_number] = row_data
#                     valid_rows += 1
#             return frame
            
#         def normalize_frame(frame):
#             min_val = np.min(frame)
#             max_val = np.max(frame)
#             if max_val - min_val == 0:
#                 return np.zeros_like(frame, dtype=np.uint8)
#             norm = ((frame - min_val) * 255.0 / (max_val - min_val)).astype(np.uint8)
#             return norm

#         while self.running:
#             raw = read_frame()
#             if raw is None:
#                 continue
#             norm = normalize_frame(raw)
#             colored = cv2.applyColorMap(norm, cv2.COLORMAP_INFERNO)
#             resized = cv2.resize(colored, (480, 360), interpolation=cv2.INTER_NEAREST)

#             self.last_frame = colored.copy()

#             image = Image.fromarray(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
#             imgtk = ImageTk.PhotoImage(image=image)
#             self.video_label.imgtk = imgtk
#             self.video_label.config(image=imgtk)

#             self.video_label.after(30)

#         spi.close()

#     def capture_image(self):
#         if self.last_frame is None:
#             messagebox.showerror("Error", "No image to capture.")
#             return

#         popup = tk.Toplevel(self)
#         popup.title("Captured Image")
#         popup.geometry("500x500")
#         popup.configure(bg="white")

#         resized = cv2.resize(self.last_frame, (480, 360), interpolation=cv2.INTER_NEAREST)
#         image = Image.fromarray(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
#         imgtk = ImageTk.PhotoImage(image=image)

#         img_label = tk.Label(popup, image=imgtk, bg="white")
#         img_label.image = imgtk
#         img_label.pack(pady=10)

#         def save():
#             folders = os.listdir("storage_folders")
#             if not folders:
#                 messagebox.showwarning("No Folders", "No folders found. Create one in the Storage page.")
#                 return

#             folder_name = simpledialog.askstring("Save Image", f"Available folders:\n{', '.join(folders)}\n\nEnter folder name to save:")
#             if folder_name and folder_name in folders:
#                 folder_path = os.path.join("storage_folders", folder_name)
#                 filename = f"thermal_{int(cv2.getTickCount())}.png"
#                 save_path = os.path.join(folder_path, filename)
#                 cv2.imwrite(save_path, self.last_frame)
#                 messagebox.showinfo("Saved", f"Image saved to {save_path}")
#                 popup.destroy()
#             else:
#                 messagebox.showwarning("Invalid Folder", "No folder selected or folder doesn't exist.")

#         def recapture():
#             popup.destroy()

#         btn_frame = tk.Frame(popup, bg="white")
#         btn_frame.pack(pady=10)

#         save_btn = tk.Button(btn_frame, text="Save", font=("Helvetica", 12), command=save)
#         save_btn.grid(row=0, column=0, padx=20)

#         recapture_btn = tk.Button(btn_frame, text="Recapture", font=("Helvetica", 12), command=recapture)
#         recapture_btn.grid(row=0, column=1, padx=20)

#     def go_back(self):
#         self.running = False
#         self.controller.show_frame("MainMenu")


class MainMenu(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        title = tk.Label(self, text="THERMAL APP", font=("Helvetica", 24, "bold"), bg="white")
        title.pack(pady=(20, 10))

        button_frame = tk.Frame(self, bg="white")
        button_frame.pack(expand=True)

        btn_style = {"width": 30, "height": 4, "font": ("Helvetica", 20)}

        buttons = [
            ("Storage", controller.open_storage),
            ("Notes", controller.open_notes),
            ("About", controller.open_about),
            ("Display", lambda: controller.show_frame("DisplayPage")),
            ("Run Inference", lambda: controller.show_frame("InferencePage")),
        ]

        for i, (text, cmd) in enumerate(buttons):
            row = i // 2
            col = i % 2
            btn = tk.Button(button_frame, text=text, command=cmd, **btn_style)
            btn.grid(row=row, column=col, padx=20, pady=20)

        gallery_btn = tk.Button(self, text="Gallery", command=controller.open_gallery, **btn_style)
        gallery_btn.pack(pady=20)



    def capture_image(self):
        if self.last_frame is None:
            messagebox.showerror("Error", "No image to capture.")
            return

        popup = tk.Toplevel(self)
        popup.title("Captured Image")
        popup.geometry("500x500")
        popup.configure(bg="white")

        resized = cv2.resize(self.last_frame, (480, 360), interpolation=cv2.INTER_NEAREST)
        image = Image.fromarray(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=image)

        img_label = tk.Label(popup, image=imgtk, bg="white")
        img_label.image = imgtk
        img_label.pack(pady=10)

        def save():
            folders = os.listdir("storage_folders")
            if not folders:
                messagebox.showwarning("No Folders", "No folders found. Create one in the Storage page.")
                return

            folder_name = simpledialog.askstring("Save Image", f"Available folders:\n{', '.join(folders)}\n\nEnter folder name to save:")
            if folder_name and folder_name in folders:
                folder_path = os.path.join("storage_folders", folder_name)
                filename = f"thermal_{int(cv2.getTickCount())}.png"
                save_path = os.path.join(folder_path, filename)
                cv2.imwrite(save_path, self.last_frame)
                messagebox.showinfo("Saved", f"Image saved to {save_path}")
                popup.destroy()
            else:
                messagebox.showwarning("Invalid Folder", "No folder selected or folder doesn't exist.")

        def recapture():
            popup.destroy()

        btn_frame = tk.Frame(popup, bg="white")
        btn_frame.pack(pady=10)

        save_btn = tk.Button(btn_frame, text="Save", font=("Helvetica", 12), command=save)
        save_btn.grid(row=0, column=0, padx=20)

        recapture_btn = tk.Button(btn_frame, text="Recapture", font=("Helvetica", 12), command=recapture)
        recapture_btn.grid(row=0, column=1, padx=20)

    def go_back(self):
        self.running = False
        self.controller.show_frame("MainMenu")

class InferencePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.selected_image_path = None 

        title = tk.Label(self, text="Inference Page", font=("Helvetica", 24, "bold"), bg="white")
        title.pack(pady=10)

        select_image_btn = tk.Button(self, text="Select Image from Gallery", font=("Helvetica", 24), command=self.select_image)
        select_image_btn.pack(pady=10)

        self.image_path_label = tk.Label(self, text="No image selected", font=("Helvetica", 24), bg="white")
        self.image_path_label.pack(pady=5)

        run_inference_btn = tk.Button(self, text="Run CNN Model", font=("Helvetica", 24), command=self.run_inference)
        run_inference_btn.pack(pady=10)

        self.results_label = tk.Label(self, text="Inference results will appear here", font=("Helvetica", 16), bg="white", wraplength=600)
        self.results_label.pack(pady=10)

        back_btn = tk.Button(self, text="Back", font=("Helvetica", 16), command=lambda: controller.show_frame("MainMenu"))
        back_btn.pack(pady=20)

    def select_image(self):
        self.selected_image_path = filedialog.askopenfilename(
            initialdir=STORAGE_DIR,
            title="Select an Image",
            filetypes=(("PNG Images", "*.png"), ("All files", "*.*"))
        )
        if self.selected_image_path:
            self.image_path_label.config(text=f"Selected: {os.path.basename(self.selected_image_path)}")
            self.results_label.config(text="Inference results will appear here") # Clear previous results
        else:
            self.image_path_label.config(text="No image selected")
            self.selected_image_path = None

    def run_inference(self):
        if self.selected_image_path:

            results = inference.predict(self.selected_image_path)
            self.results_label.config(text=f"Inference Results: {results}")

        else:
            messagebox.showwarning("No Image Selected", "Please select an image first.")

            

            
    
class StoragePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        if not os.path.exists("storage_folders"):
            os.makedirs("storage_folders")

        title = tk.Label(self, text="Storage Page", font=("Helvetica", 24, "bold"), bg="white")
        title.pack(pady=10)

        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.scroll_frame = tk.Frame(self.canvas, bg="white")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        btn_container = tk.Frame(self, bg="white")
        btn_container.pack(fill="x", pady=10)

        create_btn = tk.Button(btn_container, text="Create Folder", font=("Helvetica", 12),
                               command=self.create_folder)
        create_btn.pack(side="left", padx=20)

        back_btn = tk.Button(btn_container, text="Back", font=("Helvetica", 12),
                             command=lambda: controller.show_frame("MainMenu"))
        back_btn.pack(side="right", padx=20)

        self.folder_buttons = []
        self.load_folders()

    def load_folders(self):
        self.folder_buttons = sorted([
            folder for folder in os.listdir("storage_folders")
            if os.path.isdir(os.path.join("storage_folders", folder))
        ])
        self.display_folders()
        
    def create_folder(self):
        folder_name = simpledialog.askstring("Create Folder", "Enter folder name:")
        if folder_name:
            folder_path = os.path.join("storage_folders", folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                self.folder_buttons.append(folder_name)
                self.folder_buttons.sort()
                self.display_folders()

    def delete_folder(self, row):
        folder_name = row.winfo_children()[0].cget("text")
        folder_path = os.path.join("storage_folders", folder_name)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        self.folder_buttons.remove(folder_name)
        self.display_folders()
        
    def display_folders(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for folder_name in self.folder_buttons:
            row = tk.Frame(self.scroll_frame, bg="white")
            row.pack(pady=5, fill="x", padx=10)

            folder_btn = tk.Button(row, text=folder_name,
                                   width=25, height=2,
                                   font=("Helvetica", 12),
                                   bg="#f0f0f0", anchor="w",
                                   command=lambda name=folder_name: print(f"Opened folder: {name}"))
            folder_btn.pack(side="left", padx=(0, 10))

            delete_btn = tk.Button(row, text="X", font=("Helvetica", 12),
                                   bg="red", fg="white",
                                   command=lambda r=row: self.delete_folder(r))
            delete_btn.pack(side="left")

class NotesPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        if not os.path.exists(NOTES_DIR):
            os.makedirs(NOTES_DIR)

        title = tk.Label(self, text="Notes Page", font=("Helvetica", 24, "bold"), bg="white")
        title.pack(pady=10)

        self.text_area = tk.Text(self, wrap="word", font=("Helvetica", 14), height=15, width=80)
        self.text_area.pack(pady=20)
        

        button_frame = tk.Frame(self, bg="white")
        button_frame.pack(pady=20)

        save_btn = tk.Button(button_frame, text="Save Note", font=("Helvetica", 12), command=self.save_note)
        save_btn.pack(side="left", padx=20)

        load_btn = tk.Button(button_frame, text="Load Note", font=("Helvetica", 12), command=self.load_note)
        load_btn.pack(side="left", padx=20)

        back_btn = tk.Button(self, text="Back", font=("Helvetica", 12),
                             command=lambda: controller.show_frame("MainMenu"))
        back_btn.pack(pady=20)

    def save_note(self):
        note_name = simpledialog.askstring("Save Note", "Enter note name:")
        if note_name:
            note_path = os.path.join(NOTES_DIR, note_name + ".txt")
            with open(note_path, "w") as f:
                f.write(self.text_area.get("1.0", tk.END).strip())
            messagebox.showinfo("Success", "Note saved successfully!")
            
    def load_note(self):
        note_name = simpledialog.askstring("Load Note", "Enter note name to load:")
        if note_name:
            note_path = os.path.join(NOTES_DIR, note_name + ".txt")
            if os.path.exists(note_path):
                with open(note_path, "r") as f:
                    content = f.read()
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert(tk.END, content)
            else:
                messagebox.showerror("Error", "Note not found!")

class AboutPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        title = tk.Label(self, text="About the Lepton FLIR Kit", font=("Helvetica", 24, "bold"), bg="white")
        title.pack(pady=10)

        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.scroll_frame = tk.Frame(self.canvas, bg="white")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        about_text = (
            "The Lepton FLIR Kit with the Lepton 2.5 thermal camera module is a compact, high-performance solution "
            "for capturing thermal images and video. The kit is designed for a variety of applications including "
            "thermal monitoring, heat mapping, and temperature-sensitive analysis.\n\n"
            "Key Features:\n"
            "1. **Lepton 2.5 Camera Module**: A small and low-power thermal sensor with a resolution of 80x60 pixels.\n"
            "2. **Real-Time Video Streaming**: The module supports real-time thermal video streaming, allowing for live monitoring of temperature variations.\n"
            "3. **Compact and Lightweight**: Ideal for integration into portable devices or systems where space and power are limited.\n"
            "4. **Low Cost**: The Lepton series is known for providing affordable thermal imaging solutions for developers and hobbyists.\n\n"
            "Applications:\n"
            "1. **Building Inspections**: Detecting heat leaks and insulation issues.\n"
            "2. **Preventive Maintenance**: Identifying overheating components in machinery or electronics.\n"
            "3. **Medical and Scientific Research**: Studying temperature-related phenomena such as joint inflammation in medical studies.\n"
            "4. **Security and Surveillance**: Detecting heat signatures in low-light or dark environments.\n\n"
            "The integration of the FLIR Lepton 2.5 with the Raspberry Pi platform enables the creation of custom thermal imaging solutions, "
            "making it an ideal choice for research, development, and prototyping in various fields.\n\n"
            "This app allows users to interact with the thermal camera, view live thermal video, capture and save images, and even take notes "
            "on the captured data.\n\n"
            "For more information, please refer to the official FLIR documentation and Raspberry Pi resources."
        )

        about_label = tk.Label(self.scroll_frame, text=about_text, font=("Helvetica", 12),
                               justify="left", bg="white", wraplength=750)
        about_label.pack(padx=20, pady=20)

        back_btn = tk.Button(self, text="Back", font=("Helvetica", 12),
                             command=lambda: controller.show_frame("MainMenu"))
        back_btn.pack(pady=20)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
            
            
