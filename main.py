import tkinter as tk
import ttkbootstrap as ttk
import qrcode
from PIL import ImageTk, Image, ImageDraw
from tkinter import filedialog
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import *
from qrcode.image.styles.colormasks import RadialGradiantColorMask



# Main Class
class QRCodeGenerator:
    def __init__(self, master):
        self.master = master

        self.image = Image.open("PiepsmitTasse.png").resize((130, 100))
        self.photo = ImageTk.PhotoImage(self.image)

        # QR output and Save Variable
        self.qr_image = None
        self.pil_image = None

        # Button placement
        self.MenueButton = tk.Button(root, text="Menue")
        self.MenueButton.place(x=0, y=0)
        self.MenueButton.bind("<Button-1>", self.show_menu)
        self.MenueButton.bind("<Button-2>", self.exit_programm)

        
        # URL Entry Label
        self.url_label = tk.Label(master, text="URL:")
        self.url_label.pack(pady=20)

        self.pieps_image = tk.Label(master, image=self.photo, text="By Freelance Archery", compound="left")
        self.pieps_image.pack(side="bottom")

        # URL Entry Bar
        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack()

        # QRCode Generat Button
        self.generate_button = tk.Button(master, text="QRCode Generieren", command=self.generate_qr)
        self.generate_button.pack(pady=10)


        self.qr_label = tk.Label(master)
        self.qr_label.pack()

        # Dropdown Menu
        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="Speichern unter", command=self.save_file)
        self.menu.add_command(label="Beenden", command=self.exit_programm)

    # Drop down menu activation
    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    # CRCode Generator
    def generate_qr(self):
        url = self.url_entry.get()
        qr = qrcode.QRCode(version=3, box_size=15, border=4, error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
        self.pil_image = img

        # Set Background for Center Image
        draw = ImageDraw.Draw(self.pil_image)
        center_x, center_y = self.pil_image.size[0] // 2, self.pil_image.size[1] // 2
        half_side = 40  # Calculate center ellipse or other form
        draw.ellipse([(center_x - half_side, center_y - half_side), 
                        (center_x + half_side, center_y + half_side)], fill="white")

        # Center and insert Logo Image
        embedded_img = Image.open("PiepsmitTasse.png").resize((130, 100))
        img_width, img_height = embedded_img.size
        img_position = (center_x - img_width//2, center_y - img_height//2)
        self.pil_image.paste(embedded_img, img_position, embedded_img)

        self.qr_image = ImageTk.PhotoImage(self.pil_image)
        self.qr_label.config(image=self.qr_image)
        root.geometry(f'{self.qr_image.height() + 150}x{self.qr_image.width() + 150}')

    # Save to File PIL Function
    def save_file(self):
        if self.pil_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
            if file_path:
                self.pil_image.save(file_path)


    # Stop Programm
    def exit_programm(self):
        root.destroy()

# Main Root
root = ttk.Window(themename='solar')
root.geometry("400x500")
root.title("Piep`s QRCode Generator")
my_qr_generator = QRCodeGenerator(root)
root.mainloop()
