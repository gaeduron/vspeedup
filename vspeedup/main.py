import numpy as np
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip, concatenate_videoclips
import moviepy.audio.fx.all as afx

from vspeedup.editor import editor

def get_volume_chunks(wave, chunk_size, chunk_number):
    number_of_points = chunk_size * chunk_number
    chunked_wave = np.array_split(wave[:number_of_points], chunk_number)
    matrix = np.asarray(chunked_wave)
    matrix = np.stack(matrix)
    volume_chunks = np.absolute(matrix).mean(1)
    return volume_chunks

def audio_analysis(volume_chunks, chunk_number,  volume_threshold, wave):
    voice = volume_chunks >= volume_threshold
    silence = volume_chunks < volume_threshold

    plt.figure(figsize=(20,3))
    plt.plot(wave)
    plt.figure(figsize=(20,3))
    plt.bar(np.arange(chunk_number)[voice], volume_chunks[voice], color="green")
    plt.bar(np.arange(chunk_number)[silence], volume_chunks[silence], color="red")
    plt.show()

def auto_speedup(path, volume_threshold=0.01, speed=4, verbose=True):
    print(f"Starting to process video:\n{path}")
    clip = VideoFileClip(path) # get video
    wave = clip.fx(afx.audio_normalize).audio.to_soundarray().T[0] # get one audio channel

    # Get bitrate data
    bit_per_frame = len(wave) // int(clip.fps * clip.duration)
    audio_bitrate = bit_per_frame * clip.fps

    # Chunk sound into mean volume array
    chunk_size = int(audio_bitrate) # chunks are a second long
    chunk_number = len(wave) // chunk_size
    volume_chunks = get_volume_chunks(wave, chunk_size, chunk_number)

    if verbose:
        audio_analysis(volume_chunks, chunk_number, volume_threshold, wave)


    # Edit video
    clips = editor(clip, volume_chunks, chunk_number, volume_threshold, speed)
    final_clip = concatenate_videoclips(clips)

    # Export video
    export_path = f"{path[:-4]}-EDITED-x{speed}.mp4"
    final_clip.write_videofile(export_path,
        codec='libx264', 
        audio_codec='aac', 
        temp_audiofile='temp-audio.m4a', 
        remove_temp=True)
    
    return export_path

def interface(volume_threshold, speed, verbose):
    from ipyfilechooser import FileChooser
    from IPython.display import Javascript, display
    from ipywidgets import widgets

    # Create and display a FileChooser widget
    fc = FileChooser()
    display(fc)

    options = {
        "path": fc,
        "volume_threshold": volume_threshold,
        "speed": speed,
        "verbose": verbose
    }

    def run_script(ev):
        auto_speedup(
            options["path"].selected,
            options["volume_threshold"],
            options["speed"],
            options["verbose"]
        )

    button = widgets.Button(description="Edit video")
    button.on_click(run_script)
    display(button)