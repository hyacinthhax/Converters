import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy.editor import VideoFileClip, AudioFileClip

# Supported formats
VIDEO_FORMATS = ["mp4", "avi", "mov", "mkv", "webm"]
AUDIO_FORMATS = ["mp3", "wav", "aac", "flac", "ogg"]


class MediaConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Converter")
        self.root.geometry("480x360")
        self.root.resizable(False, False)

        self.file_paths = []  # single or multiple
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Select Files to Convert", font=("Arial", 11, "bold")).pack(pady=8)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Browse Single File", command=self.load_single_file, width=18).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Browse Multiple Files", command=self.load_batch_files, width=18).grid(row=0, column=1, padx=5)

        self.file_label = tk.Label(self.root, text="No files selected", fg="gray")
        self.file_label.pack(pady=5)

        format_frame = tk.Frame(self.root)
        format_frame.pack(pady=5)

        tk.Label(format_frame, text="From:").grid(row=0, column=0, padx=5)
        self.from_format = ttk.Combobox(format_frame, values=VIDEO_FORMATS + AUDIO_FORMATS, width=10)
        self.from_format.grid(row=0, column=1, padx=5)

        tk.Label(format_frame, text="To:").grid(row=0, column=2, padx=5)
        self.to_format = ttk.Combobox(format_frame, values=VIDEO_FORMATS + AUDIO_FORMATS, width=10)
        self.to_format.grid(row=0, column=3, padx=5)

        tk.Button(self.root, text="Convert", command=self.convert_files, bg="#4CAF50", fg="white", width=20).pack(pady=15)

        self.status_label = tk.Label(self.root, text="", fg="blue")
        self.status_label.pack(pady=5)

    # === File loading ===
    def load_single_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a media file",
            filetypes=[("Media Files", "*.mp4 *.avi *.mov *.mkv *.mp3 *.wav *.flac *.aac *.ogg *.webm")]
        )
        if file_path:
            self.file_paths = [file_path]
            self.file_label.config(text=os.path.basename(file_path), fg="black")

    def load_batch_files(self):
        files = filedialog.askopenfilenames(
            title="Select multiple media files",
            filetypes=[("Media Files", "*.mp4 *.avi *.mov *.mkv *.mp3 *.wav *.flac *.aac *.ogg *.webm")]
        )
        if files:
            self.file_paths = list(files)
            self.file_label.config(text=f"{len(files)} files selected", fg="black")

    # === Conversion ===
    def convert_files(self):
        if not self.file_paths:
            messagebox.showerror("Error", "No file(s) selected.")
            return
        if not self.to_format.get():
            messagebox.showerror("Error", "Please select a target format.")
            return

        input_format = self.from_format.get().strip().lower()
        output_format = self.to_format.get().strip().lower()

        success_count, fail_count = 0, 0
        self.status_label.config(text="Converting...", fg="blue")
        self.root.update()

        for file_path in self.file_paths:
            try:
                base, _ = os.path.splitext(file_path)
                output_path = f"{base}_converted.{output_format}"

                # Convert logic
                if input_format in VIDEO_FORMATS and output_format in AUDIO_FORMATS:
                    clip = VideoFileClip(file_path)
                    clip.audio.write_audiofile(output_path)

                elif input_format in AUDIO_FORMATS and output_format in AUDIO_FORMATS:
                    clip = AudioFileClip(file_path)
                    clip.write_audiofile(output_path)

                elif input_format in VIDEO_FORMATS and output_format in VIDEO_FORMATS:
                    clip = VideoFileClip(file_path)
                    clip.write_videofile(output_path)

                else:
                    fail_count += 1
                    continue

                success_count += 1

            except Exception as e:
                print(f"Error converting {file_path}: {e}")
                fail_count += 1

        result_msg = f"✅ {success_count} file(s) converted"
        if fail_count:
            result_msg += f", ⚠️ {fail_count} failed"
        self.status_label.config(text=result_msg, fg="green" if fail_count == 0 else "orange")
        messagebox.showinfo("Conversion Complete", result_msg)


# === Run app ===
if __name__ == "__main__":
    root = tk.Tk()
    app = MediaConverterApp(root)
    root.mainloop()
