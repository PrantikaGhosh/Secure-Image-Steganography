import cv2
import os

# Load Encoded Image
encoded_image_path = r"C:\Users\prant\OneDrive\Desktop\Stego\encryptedImage.png"
img = cv2.imread(encoded_image_path)

if img is None:
    print("Error: Could not read the encoded image.")
    exit()

# Load Stored Password
try:
    with open("password.txt", "r") as file:
        stored_password = file.read().strip()
except FileNotFoundError:
    print("Error: Password file not found.")
    exit()

# Input Password for Decryption
pas = input("Enter passcode for decryption: ")

if pas == stored_password:
    # Retrieve Message Length from First Pixel
    msg_len = int(img[0, 0, 0]) + (int(img[0, 0, 1]) * 256)

    print("Extracted Message Length:", msg_len)  # Debugging Step

    # Decoding Process
    message = ""
    m, n, z = 1, 0, 0  # Start from (0,1) to match encoding logic
    for _ in range(msg_len):
        char_code = int(img[n, m, z])
        message += chr(char_code)
        z += 1
        if z == 3:  # Move to next pixel
            z = 0
            m += 1
            if m >= img.shape[1]:  # Move to next row
                m = 0
                n += 1

    print("Decrypted Message:", message)
else:
    print("YOU ARE NOT AUTHORIZED")
