import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from pytube import YouTube
import threading
import webbrowser
import os
from time import sleep


def validate_url(url):
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return False
    return True


def preview_video():
    url = entry_url.get()
    
    if not validate_url(url):
        return
    
    try:
        yt = YouTube(url)
        webbrowser.open(yt.watch_url)
        
    except Exception:
        messagebox.showerror("Error", "Failed to preview video")


def download_video():
    url = entry_url.get()
    
    if not validate_url(url):
        return
    
    download_path = download_path_entry.get()
    if not os.path.isdir(download_path):
        messagebox.showerror("Error", "Please select a valid download path")
        return
    
    download_option = download_option_var.get()
    
    try:
        yt = YouTube(url)
        yt.register_on_progress_callback(progress_callback)
        
        if download_option == "MP4":
            stream = yt.streams.filter(progressive = True, file_extension = 'mp4').first()
        elif download_option == "MP3":
            stream = yt.streams.filter(only_audio = True).first()
        else:
            messagebox.showerror("Error", "Please Select MP4 or MP3!")
            return
        
        if stream:
            status_label.config(text = "Downloading...")
            threading.Thread(target = stream.download, kwargs = {"output_path": download_path}).start()
        else:
            messagebox.showerror("Error", "No suitable stream found!")
            
    except Exception:
        messagebox.showerror("Error", "Failed to download video")


def progress_callback(stream, chunk, bytes_remaining):
    
    root.geometry("400x310")
    progress_bar.pack(pady = 3)
    
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    progress_var.set(percentage)
    
    status_label.config(text = f"Downloaded: {int(percentage)}%")
    
    if int(percentage) == 100:
        sleep(4)
        status_label.config(text = "Download Complete", fg = "Green")
        

def select_download_path():
    
    path = filedialog.askdirectory()
    download_path_entry.delete(0, tk.END)
    download_path_entry.insert(0, path)


root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("400x280")
root.resizable(0, 0)

url_label = tk.Label(root, text = "Enter YouTube URL:", font = ("Arial", 12))
url_label.pack(pady=10)
entry_url = tk.Entry(root, width = 60, relief = "sunken", bd = 2)
entry_url.pack(pady=2)


preview_button = tk.Button(root, text = "Preview", font = ("Arial", 10), command = preview_video)
preview_button.pack(pady=5)


download_option_var = tk.StringVar(value="Video")
video_radio = tk.Radiobutton(root, text = "MP4", font = ("Arial", 10), variable = download_option_var, value = "MP4")
audio_radio = tk.Radiobutton(root, text = "MP3", font = ("Arial", 10), variable = download_option_var, value = "MP3")
video_radio.place(x = 140, y = 110)
audio_radio.place(x = 210, y = 110)


download_path_label = tk.Label(root, text = "Select Download Path:", font = ("Arial", 10))
download_path_label.pack(pady = 45)
download_path_entry = tk.Entry(root, width = 55, relief = "sunken", bd = 2, )

download_path_entry.place(x = 10, y = 180)
browse_button = tk.Button(root, text = "Browse", font = ("Arial", 9), command = select_download_path)
browse_button.place(x = 345, y = 178)


download_button = tk.Button(root, text = "Download", font = ("Arial", 10), command = download_video)
download_button.pack(pady = 2)


status_label = tk.Label(root, text = "", font = ("Arial", 10))
status_label.pack(pady = 3)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable = progress_var, maximum = 100, orient = "horizontal", length = 370)
progress_bar.pack_forget()

root.mainloop()