from moviepy.editor import vfx
import moviepy.audio.fx.all as afx

def chunk_is_first_silent(removable_chunk, volume_chunks, n, volume_threshold):
    return removable_chunk == None\
        and volume_chunks[n] < volume_threshold\
        and volume_chunks[n-1] < volume_threshold\
        and volume_chunks[n+1] < volume_threshold

def chunk_is_last_silent(removable_chunk, volume_chunks, n, volume_threshold):
    return removable_chunk and volume_chunks[n] >= volume_threshold

def editor(clip, volume_chunks, chunk_number, volume_threshold, speed):
    chunks = []
    clips = []
    removable_chunk = None
    normal_chunk = 0

    # Cutting and editing of the chunks
    for n in range(1,chunk_number-1):
        if chunk_is_first_silent(removable_chunk, volume_chunks, n, volume_threshold):
            removable_chunk = n

        elif chunk_is_last_silent(removable_chunk, volume_chunks, n, volume_threshold):
            if removable_chunk != 1: # if the video start by silence we don't want to add a normal chunk before the silent chunk
                clips.append(clip.subclip(normal_chunk,removable_chunk-1 + 0.9))
                chunks.append({"voice": True, "second": [normal_chunk, removable_chunk-1 + 0.9]})
            clips.append(clip.subclip(removable_chunk, n-2 + 0.9).fx(vfx.speedx, 4).fx(afx.volumex, 0))
            chunks.append({"voice": False, "second": [removable_chunk, n-2 + 0.9 ]})
            removable_chunk = None
            normal_chunk = n-1

    # Add a closing normal chunk if the video end without silence
    if chunks[-1]["second"][1] < chunk_number:
        chunks.append({"voice": True, "second": [chunks[-1]["second"][1]+1, chunk_number]})
        clips.append(clip.subclip(chunks[-1]["second"][0], chunks[-1]["second"][1]))

    return clips
    