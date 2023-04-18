import os
import threading
import tkinter as tk
import traceback
from tkinter import filedialog, messagebox

from tshirt import generate_t_shirt_excel
from wall import generate_wall_excel

# Set the custom font and color scheme
FONT = ("Arial", 14)
BG_COLOR = "#1c1c1c"
FG_COLOR = "#d9d9d9"
HL_COLOR = "#2f2f2f"
BTN_COLOR = "#0080ff"
BTN_HL_COLOR = "#0066cc"

downloads_folder_path = os.path.join(os.path.expanduser("~"), "Downloads")
def browse_input_file():
    filepath = filedialog.askdirectory()
    input_folder_label.config(text="Selected input file:", fg=FG_COLOR, bg=BG_COLOR)
    input_folder_name_label.config(text=filepath, fg=FG_COLOR, bg=HL_COLOR, wraplength=400)

def browse_output_folder():
    folderpath = filedialog.askdirectory()
    output_folder_label.config(text="Selected output folder:", fg=FG_COLOR, bg=BG_COLOR)
    output_folder_name_label.config(text=folderpath, fg=FG_COLOR, bg=HL_COLOR, wraplength=400)

def get_excel_type(folder_path):
    for filename in os.listdir(folder_path):
        if filename.startswith("tshirt"):
            return "tshirt"
        elif filename.startswith("wall"):
            return "wall"
        else:
            continue

    return None

def do_logic(target, args):
    error = lambda e : (
        messagebox.showerror("App error", traceback.format_exc()),
        submit_button.config(text="submit", state="normal")
    )
    finish = lambda : (
        messagebox.showinfo("Successfully", "Successfully"),
        submit_button.config(text="submit", state="normal")
    )
    threading.Thread(target=target, args=args + (error, finish)).start()

def submit_files():
    # Replace this function with your own code to submit the selected input file and output folder
    submit_button.config(text="Generating...", state="disable")

    input_path = input_folder_name_label.cget("text")
    output_path = output_folder_name_label.cget("text")

    excel_type = get_excel_type(input_path)
    if (excel_type == "tshirt"):
        do_logic(generate_t_shirt_excel, (input_path, output_path))
    elif (excel_type == "wall"):
        do_logic(generate_wall_excel, (input_path, output_path))
    else:
        messagebox.showerror("Error template file",
                             "Not support this type. Only support 'tshirt.xlsx' and 'wall.xlsx'")


# Create the main window and set its size
root = tk.Tk()
root.geometry("500x600")
root.configure(bg=BG_COLOR)
root.title("File Selection App")

# Create a section for selecting the input file
input_folder_label = tk.Label(root, text="No input file selected", font=FONT, fg=FG_COLOR, bg=BG_COLOR)
input_folder_label.pack(pady=20)

input_folder_name_label = tk.Label(root, text="", font=FONT, fg=FG_COLOR, bg=HL_COLOR, padx=10, pady=10, width=40,
                                 height=3)
input_folder_name_label.pack()

input_browse_button = tk.Button(root, text="Browse Input File", font=FONT, fg=FG_COLOR, bg=BTN_COLOR,
                                activebackground=BTN_HL_COLOR, bd=0, highlightthickness=0, command=browse_input_file)
input_browse_button.pack(pady=20)

# Create a section for selecting the output folder
output_folder_label = tk.Label(root, text="No output folder selected", font=FONT, fg=FG_COLOR, bg=BG_COLOR)
output_folder_label.pack(pady=20)

output_folder_name_label = tk.Label(root, text=downloads_folder_path, font=FONT, fg=FG_COLOR, bg=HL_COLOR, padx=10,
                                    pady=10, width=40, height=3)
output_folder_name_label.pack()

output_browse_button = tk.Button(root, text="Browse Output Folder", font=FONT, fg=FG_COLOR, bg=BTN_COLOR,
                                 activebackground=BTN_HL_COLOR, bd=0, highlightthickness=0,
                                 command=browse_output_folder)
output_browse_button.pack(pady=20)

# Create a button to submit the selected files
submit_button = tk.Button(root, text="Submit", font=FONT, fg=FG_COLOR, bg=BTN_COLOR,
                          activebackground=BTN_HL_COLOR, bd=0, highlightthickness=0, command=submit_files)
submit_button.pack(pady=20)


# Apply a hover effect to the buttons
def on_enter(e):
    e.widget['background'] = BTN_HL_COLOR


def on_leave(e):
    e.widget['background'] = BTN_COLOR


input_browse_button.bind("<Enter>", on_enter)
input_browse_button.bind("<Leave>", on_leave)
output_browse_button.bind("<Enter>", on_enter)
output_browse_button.bind("<Leave>", on_leave)
submit_button.bind("<Enter>", on_enter)
submit_button.bind("<Leave>", on_leave)

# Start the GUI main loop
root.mainloop()
