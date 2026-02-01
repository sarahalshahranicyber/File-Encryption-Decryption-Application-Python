import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet

# === Encryption Functions ===

# Generate a key and save it to a file
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Load the saved key from file
def load_key():
    return open("secret.key", "rb").read()

# Encrypt the file (overwrite the original)
def encrypt_file(filepath, key):
    f = Fernet(key)
    with open(filepath, "rb") as file:
        data = file.read()
    encrypted = f.encrypt(data)
    with open(filepath, "wb") as file:
        file.write(encrypted)

# Decrypt the file (overwrite the original)
def decrypt_file(filepath, key):
    f = Fernet(key)
    with open(filepath, "rb") as file:
        data = file.read()
    decrypted = f.decrypt(data)
    with open(filepath, "wb") as file:
        file.write(decrypted)

# === GUI Functions ===

def select_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, filepath)

def encrypt_action():
    filepath = file_entry.get()
    if not filepath:
        messagebox.showwarning("Warning", "Please select a file.")
        return

    proceed = messagebox.askyesno("Are you sure?",
                                  "This will overwrite the original file with encrypted data. Continue?")
    if not proceed:
        return

    try:
        key = load_key()
    except FileNotFoundError:
        generate_key()
        key = load_key()

    try:
        encrypt_file(filepath, key)
        messagebox.showinfo("Success", "File encrypted successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decrypt_action():
    filepath = file_entry.get()
    if not filepath:
        messagebox.showwarning("Warning", "Please select a file.")
        return

    proceed = messagebox.askyesno("Are you sure?",
                                  "This will overwrite the file with decrypted data. Continue?")
    if not proceed:
        return

    try:
        key = load_key()
        decrypt_file(filepath, key)
        messagebox.showinfo("Success", "File decrypted successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# === GUI Setup ===

root = tk.Tk()
root.title("File Encryptor & Decryptor")
root.geometry("450x220")

tk.Label(root, text="Select File:").pack(pady=10)
file_entry = tk.Entry(root, width=50)
file_entry.pack()

tk.Button(root, text="Browse", command=select_file).pack(pady=5)
tk.Button(root, text="Encrypt (Overwrite)", command=encrypt_action).pack(pady=5)
tk.Button(root, text="Decrypt (Overwrite)", command=decrypt_action).pack(pady=5)

tk.Label(root, text="Note: This will overwrite the original file.", fg="red").pack(pady=10)

root.mainloop()
