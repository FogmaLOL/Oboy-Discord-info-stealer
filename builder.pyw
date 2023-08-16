import tkinter as tk
import os
from tkinter import messagebox
from tkinter import filedialog
import subprocess


def browse_script_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python, Executable, and Pythonw files", "*.py *.pyw *.exe")])
    script_path_entry.delete(0, tk.END)
    script_path_entry.insert(0, file_path)


def toggle_fullscreen():
    if root.attributes("-fullscreen"):
        root.attributes("-fullscreen", False)
        fullscreen_button.config(text="Full Screen", bg="#6A00FF")
    else:
        root.attributes("-fullscreen", True)
        fullscreen_button.config(text="Exit Full Screen", bg="#FF6A00")


def create_new_script():
    script_path = script_path_entry.get()

    with open(script_path, "r") as script_file:
        script_content = script_file.read()

    new_script_content = script_content.replace("Ur webhook", webhook_entry.get())

    save_filename = save_entry.get() + script_type.get()

    if script_type.get() == ".exe":
        script_directory = os.path.dirname(script_path)
        save_path = os.path.join(script_directory, save_filename + ".py")
        with open(save_path, "w") as new_script_file:
            new_script_file.write(new_script_content)

        subprocess.call(["pyinstaller", "--onefile", save_path])
        os.remove(save_path)

    else:
        script_directory = os.path.dirname(script_path)
        save_path = os.path.join(script_directory, save_filename)
        with open(save_path, "w") as new_script_file:
            new_script_file.write(new_script_content)

    messagebox.showinfo("File Created", f"New file '{save_filename}' has been created.")


# Create the main window
root = tk.Tk()
root.title("Webhook Replacer V2")
root.configure(bg="#101010")
root.geometry("900x600")

# Sidebar
sidebar = tk.Frame(root, bg="#6A00FF")
sidebar.pack(fill="y", side="left", pady=20, padx=10)

builder_label = tk.Label(sidebar, text="Builder", bg="#6A00FF", fg="#FFFFFF", font=("Arial", 20, "bold"))
builder_label.pack(pady=(20, 10))

credits_label = tk.Label(sidebar, text="Credits", bg="#6A00FF", fg="#FFFFFF", font=("Arial", 16))
credits_label.pack(pady=(0, 10))

github_link = tk.Label(sidebar, text="GitHub", bg="#6A00FF", fg="#FF6A00", font=("Arial", 14, "underline"))
github_link.pack()
github_link.bind("<Button-1>", lambda e: os.system("start https://github.com/FogmaLOL"))

# Main Content
main_content = tk.Frame(root, bg="#101010")
main_content.pack(fill="both", expand=True, padx=20)

# Title Label
title_label = tk.Label(main_content, text="Webhook Replacer V2", bg="#101010", fg="#6A00FF", font=("Arial", 24, "bold"))
title_label.pack(pady=20)

# Script File Label and Entry
script_path_label = tk.Label(main_content, text="Select Script or Executable File:", bg="#101010", fg="#FFFFFF",
                             font=("Arial", 14))
script_path_label.pack()

script_path_entry = tk.Entry(main_content, width=50, font=("Arial", 12))
script_path_entry.pack()

browse_button = tk.Button(main_content, text="Browse", command=browse_script_file, font=("Arial", 12))
browse_button.pack()

# Webhook URL Label and Entry
webhook_label = tk.Label(main_content, text="Enter New Webhook URL:", bg="#101010", fg="#FFFFFF", font=("Arial", 14))
webhook_label.pack()

webhook_entry = tk.Entry(main_content, width=50, font=("Arial", 12))
webhook_entry.pack()

# Choose Script Type Buttons
script_type = tk.StringVar(value=".py")


def set_script_type(extension):
    script_type.set(extension)


button_frame = tk.Frame(main_content, bg="#101010")
button_frame.pack()

py_button = tk.Radiobutton(button_frame, text=".py", variable=script_type, value=".py",
                           command=lambda: set_script_type(".py"), bg="#6A00FF", fg="#FFFFFF", font=("Arial", 12))
py_button.pack(side="left", padx=10)

pyw_button = tk.Radiobutton(button_frame, text=".pyw", variable=script_type, value=".pyw",
                            command=lambda: set_script_type(".pyw"), bg="#6A00FF", fg="#FFFFFF", font=("Arial", 12))
pyw_button.pack(side="left", padx=10)

exe_button = tk.Radiobutton(button_frame, text=".exe", variable=script_type, value=".exe",
                            command=lambda: set_script_type(".exe"), bg="#6A00FF", fg="#FFFFFF", font=("Arial", 12))
exe_button.pack(side="left", padx=10)

# Name of New Script Label and Entry
save_label = tk.Label(main_content, text="Enter Name of New Script:", bg="#101010", fg="#FFFFFF", font=("Arial", 14))
save_label.pack()

save_entry = tk.Entry(main_content, width=50, font=("Arial", 12))
save_entry.pack()

# Create New Script Button
create_button = tk.Button(main_content, text="Create New Script", command=create_new_script, bg="#6A00FF", fg="#FFFFFF",
                          font=("Arial", 14))
create_button.pack(pady=20)

# Full Screen Button
fullscreen_button = tk.Button(main_content, text="Full Screen", command=toggle_fullscreen, bg="#6A00FF", fg="#FFFFFF",
                              font=("Arial", 14))
fullscreen_button.pack()

root.mainloop()
