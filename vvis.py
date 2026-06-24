import sys
import numpy as np
import pygame
from pydub import AudioSegment
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tkinter import Tk, filedialog

# ===== Helper: Load audio =====
def load_audio(path):
    audio = AudioSegment.from_file(path)  # works for mp3/wav
    audio = audio.set_channels(1).set_frame_rate(44100)  # mono, 44.1kHz
    samples = np.array(audio.get_array_of_samples())
    return samples, audio.frame_rate, audio.duration_seconds

# ===== Visualizer Function =====
def run_visualizer(file_path):
    print(f"Loading: {file_path}")
    samples, rate, duration = load_audio(file_path)

    # Start pygame mixer
    pygame.mixer.init(frequency=rate)
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Plot setup
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(1024)
    line, = ax.plot(x, np.random.rand(1024), lw=2)
    ax.set_ylim(-32768, 32767)
    ax.set_xlim(0, 1024)
    ax.set_title("Real-Time Music Visualizer")
    ax.set_xlabel("Samples")
    ax.set_ylabel("Amplitude")

    # Update function for animation
    chunk_size = 1024
    total_samples = len(samples)
    current_frame = [0]  # use list for mutability inside function

    def update(frame):
        if not pygame.mixer.music.get_busy():
            plt.close(fig)  # close window when music ends
            return line,

        start = current_frame[0]
        end = start + chunk_size
        if end >= total_samples:
            end = total_samples
        chunk = samples[start:end]

        if len(chunk) < chunk_size:
            chunk = np.pad(chunk, (0, chunk_size - len(chunk)))

        line.set_ydata(chunk)
        current_frame[0] += chunk_size
        return line,

    ani = FuncAnimation(fig, update, interval=30, blit=False)

    plt.show(block=True)  # keep window open until user closes

# ===== Entry Point =====
if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Open file dialog if no file passed
        root = Tk()
        root.withdraw()  # hide main tkinter window
        file_path = filedialog.askopenfilename(
            title="Select an MP3 or WAV file",
            filetypes=[("Audio Files", "*.mp3 *.wav")]
        )
        if not file_path:
            print("No file selected. Exiting.")
            sys.exit(0)

    run_visualizer(file_path)
