import tkinter as tk
from tkinter import filedialog
from scipy.fft import dct, idct
import soundfile as sf
import numpy as np

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def compress_audio():
    input_file = input_entry.get()
    if input_file:
        try:
            # Open the audio file and read data
            audio_data, sample_rate = sf.read(input_file)
            
            # Convert stereo audio to mono
            if audio_data.ndim == 2:
                audio_data = np.mean(audio_data, axis=1)

            # Apply DCT compression
            block_size = 1024  # Adjust block size as needed
            num_blocks = len(audio_data) // block_size
            compressed_data = np.zeros_like(audio_data)
            
            for i in range(num_blocks):
                block = audio_data[i * block_size : (i + 1) * block_size]
                dct_block = dct(block, norm='ortho')
                compressed_block = idct(dct_block, norm='ortho')
                compressed_data[i * block_size : (i + 1) * block_size] = compressed_block
            
            # Save the compressed audio
            output_file = input_file.replace('.wav', '_compressed.wav')
            sf.write(output_file, compressed_data.astype(np.float32), sample_rate)
            
            status_label.config(text="DCT Compression successful!")
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")
    else:
        status_label.config(text="Please select an audio file first.")

# Create the main window
window = tk.Tk()
window.title("Audio Compression")

# Create widgets
select_button = tk.Button(window, text="Select Audio File", command=select_file)
select_button.pack(pady=10)

input_entry = tk.Entry(window, width=50)
input_entry.pack(pady=5)

compress_button = tk.Button(window, text="Compress Audio", command=compress_audio)
compress_button.pack(pady=10)

status_label = tk.Label(window, text="")
status_label.pack(pady=5)

# Run the GUI
window.mainloop()