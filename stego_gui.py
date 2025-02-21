import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import cv2
import numpy as np
from PIL import Image, ImageTk

def select_message_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        message_entry.delete(0, tk.END)
        message_entry.insert(0, file_path)

def encode_message():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    
    img = cv2.imread(file_path)
    msg_file = message_entry.get()
    password = password_entry.get()
    
    if not msg_file or not password:
        messagebox.showerror("Error", "Message File and Password cannot be empty!")
        return
    
    try:
        with open(msg_file, "r") as file:
            msg = file.read()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {e}")
        return
    
    msg = password + "::" + msg  # Append password for verification
    msg_bytes = msg.encode()
    msg_len = len(msg_bytes)
    
    if msg_len > img.shape[0] * img.shape[1]:
        messagebox.showerror("Error", "Message is too long to hide in this image!")
        return
    
    binary_msg = format(msg_len, '016b') + ''.join(format(byte, '08b') for byte in msg_bytes)  # Store length first
    idx = 0
    for row in img:
        for pixel in row:
            for i in range(3):
                if idx < len(binary_msg):
                    pixel[i] = (pixel[i] & 0xFE) | int(binary_msg[idx])
                    idx += 1
    
    output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
    if output_path:
        cv2.imwrite(output_path, img)
        messagebox.showinfo("Success", "Message encoded successfully!")

def decode_message():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
    if not file_path:
        return
    
    img = cv2.imread(file_path)
    binary_msg = ""
    for row in img:
        for pixel in row:
            for i in range(3):
                binary_msg += str(pixel[i] & 1)
    
    msg_length = int(binary_msg[:16], 2)  # Extract length from first 16 bits
    byte_array = [binary_msg[i:i+8] for i in range(16, 16 + msg_length * 8, 8)]
    decoded_msg = ''.join(chr(int(byte, 2)) for byte in byte_array if int(byte, 2) != 0)
    
    if "::" in decoded_msg:
        saved_password, actual_msg = decoded_msg.split("::", 1)
        entered_password = simpledialog.askstring("Password", "Enter password:", show='*')
        if entered_password == saved_password:
            messagebox.showinfo("Decrypted Message", actual_msg)
        else:
            messagebox.showerror("Error", "Incorrect Password!")
    else:
        messagebox.showerror("Error", "No valid hidden message found!")

# GUI Setup
root = tk.Tk()
root.title("Secure Data Hiding in Image")
root.geometry("700x500")
root.configure(bg="#D3D3D3")

frame = tk.Frame(root, bg="#FFFFFF", padx=20, pady=20, relief=tk.RIDGE, borderwidth=3)
frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

title_label = tk.Label(frame, text="Secure Data Hiding in Image", fg="#333", bg="#FFFFFF", font=("Arial", 18, "bold"))
title_label.grid(row=0, column=0, columnspan=3, pady=10)

message_label = tk.Label(frame, text="Message File:", fg="#333", bg="#FFFFFF", font=("Arial", 12))
message_label.grid(row=1, column=0, pady=5, sticky="w")
message_entry = tk.Entry(frame, width=40, font=("Arial", 12))
message_entry.grid(row=1, column=1, pady=5, padx=10)
message_button = tk.Button(frame, text="...", command=select_message_file, font=("Arial", 10))
message_button.grid(row=1, column=2, padx=5)

password_label = tk.Label(frame, text="Password:", fg="#333", bg="#FFFFFF", font=("Arial", 12))
password_label.grid(row=2, column=0, pady=5, sticky="w")
password_entry = tk.Entry(frame, width=40, font=("Arial", 12), show="*")
password_entry.grid(row=2, column=1, pady=5, padx=10)

encode_button = tk.Button(frame, text="Hide Data", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=encode_message)
encode_button.grid(row=3, column=0, pady=10, padx=5)

decode_button = tk.Button(frame, text="Extract Data", font=("Arial", 12, "bold"), bg="#F44336", fg="white", command=decode_message)
decode_button.grid(row=3, column=1, pady=10, padx=5)

root.mainloop()