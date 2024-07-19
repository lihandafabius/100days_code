from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import filedialog as fd
import os

img_path = None
logo_path = None
photo = None
original_photo = None
new_logo = None
watermark_text = None
logo = None


def open_photo():
    global img_path, photo, original_photo, label_photo, tk_photo
    img_path = fd.askopenfilename(
        title="Select a file of any type",
        filetypes=[("All files", "*.*")])
    if img_path:
        photo = Image.open(img_path)
        original_photo = photo.copy()  # Keep a copy of the original photo
        tk_photo = ImageTk.PhotoImage(photo.resize((200, 200)))
        label_photo.configure(image=tk_photo)
        label_photo.image = tk_photo
        success_text.set("Photo loaded successfully.")


def open_logo():
    global logo_path, new_logo, logo, label_logo, tk_logo
    logo_path = fd.askopenfilename(
        title="Select a file of any type",
        filetypes=[("All files", "*.*")])
    if logo_path:
        logo = Image.open(logo_path)
        tk_logo = ImageTk.PhotoImage(logo.resize((200, 200)))
        label_logo.configure(image=tk_logo)
        label_logo.image = tk_logo
        success_text.set("Logo loaded successfully.")


def save():
    global new_logo, watermark_text, photo, original_photo, logo
    if original_photo is None:
        success_text.set("Please load a photo before saving.")
        return

    width = int(logo_width_input.get())
    height = int(logo_height_input.get())
    x_offset = int(logo_x_offset_input.get())
    y_offset = int(logo_y_offset_input.get())

    watermark_text = watermark_text_input.get()

    watermark_image = original_photo.copy()  # Work on a copy of the original photo
    draw = ImageDraw.Draw(watermark_image)

    if watermark_text:
        font = ImageFont.truetype("arial.ttf", 40)
        textwidth, textheight = draw.textbbox((0, 0), watermark_text, font=font)[2:]
        x = watermark_image.size[0] - x_offset - textwidth
        y = watermark_image.size[1] - y_offset - textheight
        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))

    if logo:
        new_logo = logo.resize((width, height))
        box = (watermark_image.size[0] - x_offset - new_logo.size[0],
               watermark_image.size[1] - y_offset - new_logo.size[1],
               watermark_image.size[0] - x_offset,
               watermark_image.size[1] - y_offset)
        watermark_image.paste(new_logo, box, new_logo if new_logo.mode == 'RGBA' else None)

    if watermark_image.mode == 'RGBA':
        watermark_image = watermark_image.convert('RGB')  # Convert to RGB mode

    finished_img_path = os.path.splitext(img_path)[0] + "_WM.jpg"
    watermark_image.save(finished_img_path)
    watermark_image.show()
    success_text.set(f"Success! File saved to {finished_img_path}.")

    photo = watermark_image.copy()  # Update photo with the watermark


def remove_watermark():
    global photo, original_photo, img_path
    if original_photo is None:
        success_text.set("Please load a photo before removing watermark.")
        return

    photo = original_photo.copy()  # Restore the original photo
    tk_photo = ImageTk.PhotoImage(photo.resize((200, 200)))
    label_photo.configure(image=tk_photo)
    label_photo.image = tk_photo

    clean_img_path = os.path.splitext(img_path)[0] + "_Clean.jpg"
    photo.save(clean_img_path)
    success_text.set(f"Watermark removed. File saved to {clean_img_path}.")


def close_app():
    root.destroy()

# ---------------------------- UI SETUP ------------------------------- #

root = Tk()
root.config(padx=20, pady=20, bg="white")
root.title("Watermark Marker")

style = ttk.Style()
style.configure("RoundedButton.TButton", relief="flat", background="#4CAF50", foreground="white", font=("Arial", 12), padding=10)
style.map("RoundedButton.TButton",
          background=[('active', '#45a049')],
          relief=[('pressed', 'sunken')])

frame = Frame(root, bg="white")
frame.grid(row=0, column=0, padx=10, pady=10)

button_open_photo = ttk.Button(frame, text='Add Images', command=open_photo, width=20, style="RoundedButton.TButton")
button_open_photo.grid(row=0, column=0, padx=10, pady=10)

button_open_logo = ttk.Button(frame, text='Add Logo', command=open_logo, width=20, style="RoundedButton.TButton")
button_open_logo.grid(row=0, column=1, padx=10, pady=10)

button_remove_watermark = ttk.Button(frame, text='Remove Watermark', command=remove_watermark, width=20, style="RoundedButton.TButton")
button_remove_watermark.grid(row=0, column=2, padx=10, pady=10)

logo_width_label = Label(frame, text="Logo Width:", bg="white")
logo_width_label.grid(row=1, column=0)
logo_width_input = Entry(frame, width=10)
logo_width_input.insert(0, "50")
logo_width_input.grid(row=1, column=1, sticky="w")

logo_height_label = Label(frame, text="Logo Height:", bg="white")
logo_height_label.grid(row=2, column=0)
logo_height_input = Entry(frame, width=10)
logo_height_input.insert(0, "50")
logo_height_input.grid(row=2, column=1, sticky="w")

logo_x_offset_label = Label(frame, text="Logo X Offset:", bg="white")
logo_x_offset_label.grid(row=3, column=0)
logo_x_offset_input = Entry(frame, width=10)
logo_x_offset_input.insert(0, "20")
logo_x_offset_input.grid(row=3, column=1, sticky="w")

logo_y_offset_label = Label(frame, text="Logo Y Offset:", bg="white")
logo_y_offset_label.grid(row=4, column=0)
logo_y_offset_input = Entry(frame, width=10)
logo_y_offset_input.insert(0, "20")
logo_y_offset_input.grid(row=4, column=1, sticky="w")

watermark_text_label = Label(frame, text="Watermark Text:", bg="white")
watermark_text_label.grid(row=5, column=0)
watermark_text_input = Entry(frame, width=20)
watermark_text_input.grid(row=5, column=1, columnspan=2, sticky="w")

button_render = ttk.Button(frame, text='Render', command=save, width=20, style="RoundedButton.TButton")
button_render.grid(row=6, column=0, columnspan=3, pady=20)

button_quit = ttk.Button(frame, text="Close App", command=close_app, width=20, style="RoundedButton.TButton")
button_quit.grid(row=7, column=0, columnspan=3, pady=10)

success_text = StringVar()
success_text.set("")
success_label = Label(root, textvariable=success_text, background='white')
success_label.grid(row=1, column=0, columnspan=3)

label_photo = Label(root)
label_photo.grid(row=2, column=0, pady=10)

label_logo = Label(root)
label_logo.grid(row=2, column=1, pady=10)

root.mainloop()
