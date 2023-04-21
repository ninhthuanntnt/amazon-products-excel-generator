import concurrent.futures
import os
import threading
import tkinter as tk
import traceback
from tkinter import filedialog, messagebox, ttk

import coloredlogs
from safe_counter import SafeCounter
from tshirt import generate_t_shirt_excel
from wall import generate_wall_excel

coloredlogs.install(level='INFO')
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


def browse_side_excel_file():
    folderpath = filedialog.askopenfilename()
    side_excel_file_label.config(text="Selected side excel file:", fg=FG_COLOR, bg=BG_COLOR)
    side_excel_file_name_label.config(text=folderpath, fg=FG_COLOR, bg=HL_COLOR, wraplength=400)


def get_excel_type(folder_path):
    for filename in os.listdir(folder_path):
        if filename.startswith("tshirt"):
            return "tshirt"
        elif filename.startswith("wall"):
            return "wall"
        else:
            continue

    return None


def get_excel_for_multiple_folders(foder_path):
    for folder_name in os.listdir(foder_path):
        child_folder_path = os.path.join(folder_path, folder_name)
        if (os.path.isdir(child_folder_path)):
            return get_excel_type(child_folder_path)

    return None


def check_value_is_0_then_show_info(count: SafeCounter):
    if (count.value() == 0):
        messagebox.showinfo("Successfully",
                            f"Success generate excel files")

def generate_side_excel(error, finish, child_sku):
    pass

def threadpool_run(input_path, output_path):
    with concurrent.futures.ThreadPoolExecutor() as executor:

        total_count = 0;
        realtime_counter = SafeCounter()

        for folder_name in os.listdir(input_path):
            folder_path = os.path.join(input_path, folder_name)
            if os.path.isdir(folder_path):
                excel_type = get_excel_type(folder_path)
                error = lambda e: (messagebox.showerror("App error", traceback.format_exc()),
                                   submit_button.config(text="submit", state="normal"),
                                   executor.shutdown(wait=False))
                finish = lambda time_exec, saved_path, return_data: (realtime_counter.decrement(),
                                                                     check_value_is_0_then_show_info(realtime_counter),
                                                                     submit_button.config(text="submit", state="normal"),
                                                                     print(return_data))
                if (excel_type == "tshirt"):
                    executor.submit(generate_t_shirt_excel, folder_path, output_path, error, finish)
                    realtime_counter.increment()
                    total_count += 1
                elif (excel_type == "wall"):
                    executor.submit(generate_wall_excel, folder_path, output_path, error, finish)
                    realtime_counter.increment()
                    total_count += 1
                else:
                    messagebox.showerror("Error template file",
                                         "Not support this type. Only support 'tshirt.xlsx' and 'wall.xlsx'\nNon-error files've already saved")

                    submit_button.config(text="submit", state="normal")
                    break

                print(realtime_counter.value())


def handle_upload_multiple_folders(input_path, output_path):
    finish_all = lambda time_exec, saved_path: (
        messagebox.showinfo("Successfully",
                            f"Success generate excel file: \n{saved_path} \nexecution time: {time_exec}"),
        submit_button.config(text="submit", state="normal")
    )

    threading.Thread(target=threadpool_run, args=(input_path, output_path)).start()


def do_upload_one_folder(target, args):
    error = lambda e: (
        messagebox.showerror("App error", traceback.format_exc()),
        submit_button.config(text="submit", state="normal")
    )
    finish = lambda time_exec, saved_path, return_data: (
        messagebox.showinfo("Successfully",
                            f"Success generate excel file: \n{saved_path} \nexecution time: {time_exec}"),
        submit_button.config(text="submit", state="normal")
    )
    threading.Thread(target=target, args=args + (error, finish)).start()


def handle_upload_one_folder(input_path, output_path):
    excel_type = get_excel_type(input_path)
    if (excel_type == "tshirt"):
        do_upload_one_folder(generate_t_shirt_excel, (input_path, output_path))
    elif (excel_type == "wall"):
        do_upload_one_folder(generate_wall_excel, (input_path, output_path))
    else:
        messagebox.showerror("Error template file",
                             "Not support this type. Only support 'tshirt.xlsx' and 'wall.xlsx'")
        submit_button.config(text="submit", state="normal")


def submit_files():
    # Replace this function with your own code to submit the selected input file and output folder
    submit_button.config(text="Generating...", state="disable")

    input_path = input_folder_name_label.cget("text")
    output_path = output_folder_name_label.cget("text")

    if (checkbox_var.get()):
        handle_upload_multiple_folders(input_path, output_path)
    else:
        handle_upload_one_folder(input_path, output_path)


# Create the main window and set its size
root = tk.Tk()
root.geometry("500x850")
root.resizable(False, False)
root.configure(bg=BG_COLOR)
root.title("File Selection App")
# Create a section for checkbox
custom_style = ttk.Style()
custom_style.configure("CustomCheckbox.TCheckbutton", background=BG_COLOR, foreground=FG_COLOR, bordercolor="#000000",
                       borderwidth=5, relief="raised", font=FONT)

checkbox_var = tk.BooleanVar(value=True)
checkbox = ttk.Checkbutton(root, text="Multiple files", variable=checkbox_var, style="CustomCheckbox.TCheckbutton")
checkbox.pack(pady=10)

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

# Create a section for selecting the side excel file
side_excel_file_label = tk.Label(root, text="No side excel file selected", font=FONT, fg=FG_COLOR, bg=BG_COLOR)
side_excel_file_label.pack(pady=20)

side_excel_file_name_label = tk.Label(root, text="", font=FONT, fg=FG_COLOR, bg=HL_COLOR, padx=10,
                                      pady=10, width=40, height=3)
side_excel_file_name_label.pack()

side_excel_browse_button = tk.Button(root, text="Browse side excel file", font=FONT, fg=FG_COLOR, bg=BTN_COLOR,
                                     activebackground=BTN_HL_COLOR, bd=0, highlightthickness=0,
                                     command=browse_side_excel_file)
side_excel_browse_button.pack(pady=20)

# Create a button to submit the selected files
submit_button = tk.Button(root, text="Submit", font=FONT, fg=FG_COLOR, bg=BTN_COLOR,
                          activebackground=BTN_HL_COLOR, bd=0, highlightthickness=0, command=submit_files)
submit_button.pack(pady=30)


# Apply a hover effect to the buttons
def on_enter(e):
    e.widget['background'] = BTN_HL_COLOR


def on_leave(e):
    e.widget['background'] = BTN_COLOR


input_browse_button.bind("<Enter>", on_enter)
input_browse_button.bind("<Leave>", on_leave)
output_browse_button.bind("<Enter>", on_enter)
output_browse_button.bind("<Leave>", on_leave)
side_excel_browse_button.bind("<Enter>", on_enter)
side_excel_browse_button.bind("<Leave>", on_leave)
submit_button.bind("<Enter>", on_enter)
submit_button.bind("<Leave>", on_leave)

# Start the GUI main loop
root.mainloop()
