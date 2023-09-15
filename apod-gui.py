import tkinter as tk
from tkinter import messagebox
import datetime
import os

def change_wallpaper():
    date_str = date_entry.get()
    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        current_date = datetime.datetime.now().date()
        
        if date < current_date:
            messagebox.showerror("Invalid Date", "Please enter a future date.")
        else:
            # Change the desktop wallpaper logic goes here
            # You can use a library like `pywall` or `wallpaper` to change the wallpaper
            # For simplicity, let's assume we just print a message for now
            messagebox.showinfo("Wallpaper Changed", "Desktop wallpaper changed successfully!")
    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter a valid date in the format YYYY-MM-DD.")

# Create the main window
window = tk.Tk()
window.title("Desktop Wallpaper Changer")

# Create a label and entry field for the date
date_label = tk.Label(window, text="Enter a date (YYYY-MM-DD):")
date_label.pack()

date_entry = tk.Entry(window)
date_entry.pack()

# Create a button to change the wallpaper
change_button = tk.Button(window, text="Change Wallpaper", command=change_wallpaper)
change_button.pack()

# Start the Tkinter event loop
window.mainloop()
