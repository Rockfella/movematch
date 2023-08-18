import bpy


def frame_from_smpte(smpte_timecode: str, fps=None, fps_base=None) -> int:

    if fps == None or fps_base == None:
        # Use current scene fps if fps and fps_base are not provided
        fps = bpy.context.scene.render.fps
        fps_base = bpy.context.scene.render.fps_base
        fps_real = fps / fps_base

    # Split the timecode into its components
    timecode_parts = smpte_timecode.split(':')
    hours = int(timecode_parts[0])
    minutes = int(timecode_parts[1])
    seconds = int(timecode_parts[2])
    frames = int(timecode_parts[3])

    

    hours_seconds_frames = ((hours * 60) * 60) * fps_real
    minutes_seconds_frames = (minutes * 60) * fps_real
    seconds_frames = seconds * fps_real
    frames_frames = frames

    # Calculate the total number of frames
    total_frames = (hours_seconds_frames +
                    minutes_seconds_frames + seconds_frames + frames)

    # print(hours_seconds_frames, minutes_seconds_frames,
    #      seconds_frames, frames_frames)
    return total_frames
