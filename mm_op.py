import bpy
import datetime
from bpy.types import Operator
from .mm_global import frame_from_smpte
import os


class MM_OT_NewScene(bpy.types.Operator):
    bl_idname = "movematch.new_scene"
    bl_label = "Add Scene"
    bl_description = "Placeholder action for the button"

    def execute(self, context):
        # create_ffpmpeg()
        scene = bpy.context.scene
        sequences = bpy.data.scenes[bpy.context.scene.name].sequence_editor.sequences
        scene_counter = 0
        has_added_calibration = False
        calibration_duration = 0 
        for sequence in sequences:
            if sequence.type == 'TEXT':
                if sequence.name == '@calibration':
                    print("@calibration found")
                    has_added_calibration = True
                    calibration_duration = sequence.frame_final_duration
                    print("print(sequence.frame_duration)")
                    print("Duration:", sequence.frame_duration)

        for sequence in sequences:
            if sequence.type == 'TEXT':
                name = sequence.name
                first_name = name.split("_")[0]
                second_name = name.split("_")[0]
                
                if first_name == '@scene':
                    print(scene_counter)
                    
                    scene_counter += 1
        if has_added_calibration:
            strip_x_transform = scene_counter * 300 + calibration_duration
        else: 
            strip_x_transform = scene_counter * 300
        

        if scene_counter == 0:

            empty_channel = find_empty_channel(sequences)
            bpy.data.scenes[bpy.context.scene.name].mm_scene_free_channel = empty_channel
        else:
            empty_channel = bpy.data.scenes[bpy.context.scene.name].mm_scene_free_channel

        text_strip = bpy.data.scenes[bpy.context.scene.name].sequence_editor.sequences.new_effect(
            name=f"@scene_{scene_counter}",
            type='TEXT',
            frame_start=scene.frame_start + strip_x_transform,
            frame_end=scene.frame_start + strip_x_transform + 300,
            channel=empty_channel
        )
        text_strip.text = f"@scene_{scene_counter}"
        # Set the font and size for the text strip
        text_strip.font_size = 50.0
        # Set the position and alignment of the text strip
        text_strip.location = (0.05, 0.18)  # Set the position of the text strip
        text_strip.use_shadow = False
        text_strip.use_box = True
        text_strip.shadow_color = (0, 0, 0, 0)  # Set the shadow color
        # text_strip.wrap_width = 300  # Set the wrap width of the text strip
        text_strip.align_x = 'LEFT'  # Set the horizontal alignment
        text_strip.align_y = 'CENTER'  # Set the vertical alignment
        text_strip.color_tag = pickTagColorForScene(scene_counter)
        text_strip.color = pickVisualTextColorForScene(scene_counter)

        


        print("ADD SCENE")

        return {'FINISHED'}


def pickVisualTextColorForScene(key):

    # ColorTag for num hotkeys
    int_key = int(key)

    if int_key == 0:
        return (0.88, 0.38, 0.36, 1.00)  # red
    elif int_key == 1:
        return (0.94, 0.64, 0.33, 1.00)  # orange
    elif int_key == 2:
        return (0.94, 0.86, 0.33, 1.00)  # yellow
    elif int_key == 3:
        return (0.48, 0.80, 0.48, 1.00)  # green
    elif int_key == 4:
        return (0.36, 0.71, 0.91, 1.00)  # blue
    elif int_key == 5:
        return (0.55, 0.35, 0.85, 1.00)  # purple
    elif int_key == 6:
        return (0.77, 0.45, 0.72, 1.00)  # pink
    elif int_key == 7:
        return (0.47, 0.33, 0.25, 1.00)  # brown
    elif int_key == 8:
        return (0.37, 0.37, 0.37, 1.00)  # gray
    elif int_key == 9:
        return (0.48, 0.80, 0.48, 1.00)   # green

    else:
        return (0.48, 0.80, 0.48, 1.00)  # green

class MM_OT_NewCalibration(bpy.types.Operator):
    bl_idname = "movematch.new_calibration"
    bl_label = "Calibration"
    bl_description = "Placeholder action for the button"

    def execute(self, context):
        #create_ffpmpeg()
        #TODO: Calibration add
        scene = bpy.context.scene
        sequences = bpy.data.scenes[bpy.context.scene.name].sequence_editor.sequences
        for sequence in sequences:
            if sequence.type == 'TEXT':
                if sequence.name == '@calibration':
                    sequences.remove(sequence)
                    break
        empty_channel = find_empty_channel(sequences)
        text_strip = bpy.data.scenes[bpy.context.scene.name].sequence_editor.sequences.new_effect(
            name="@calibration",
            type='TEXT',
            frame_start=scene.frame_start,
            frame_end=scene.frame_start + 100,
            channel=empty_channel
        )
        text_strip.text = ''
        # Set the font and size for the text strip
        text_strip.font_size = 50.0
        # Set the position and alignment of the text strip
        text_strip.location = (0.05, 0.1)  # Set the position of the text strip
        text_strip.use_shadow = False
        text_strip.use_box = True
        text_strip.shadow_color = (0, 0, 0, 0)  # Set the shadow color
        # text_strip.wrap_width = 300  # Set the wrap width of the text strip
        text_strip.align_x = 'LEFT'  # Set the horizontal alignment
        text_strip.align_y = 'CENTER'  # Set the vertical alignment
        text_strip.color_tag = "COLOR_04"
        return {'FINISHED'}


def pickTagColorForScene(key):

    # ColorTag for num hotkeys
    int_key = int(key)

    color_array = ["COLOR_01", "COLOR_02", "COLOR_03", "COLOR_04",
                   "COLOR_05", "COLOR_06", "COLOR_07", "COLOR_08", "COLOR_09"]

    if int_key == 0:
        return color_array[0]
    elif int_key == 1:
        return color_array[1]
    elif int_key == 2:
        return color_array[2]
    elif int_key == 3:
        return color_array[3]
    elif int_key == 4:
        return color_array[4]
    elif int_key == 5:
        return color_array[5]
    elif int_key == 6:
        return color_array[6]
    elif int_key == 7:
        return color_array[7]
    elif int_key == 8:
        return color_array[8]
    elif int_key == 9:
        return color_array[3]

    else:
        return color_array[3]  # green

class MM_OT_FfmpegCreate(bpy.types.Operator):
    bl_idname = "movematch.ffmpeg_create"
    bl_label = "Create FFMPEG"
    bl_description = "Placeholder action for the button"

    def execute(self, context):
        create_ffpmpeg()

        return {'FINISHED'}




class MM_OT_ArrangeChannels(bpy.types.Operator):
    bl_idname = "movematch.arrange_channels"
    bl_label = "Arrange Clips"
    bl_description = "Placeholder action for the button"

    def execute(self, context):
        arrange_strips()
        
        return {'FINISHED'}



class MM_OT_Master_Clock_Button(Operator):
    bl_idname = "movematch.master_button_operator"
    bl_label = "Set Master Clock"
    bl_description = "Sets the master clock to the frame selected in the timeline"

    def execute(self, context):
        # button_function(self, context)

        if check_string_format(context.scene.mm_master_time):
            print("String is in the correct format.")
            print(context.scene.mm_master_time)
            setNewMasterClock(self, context)

        else:
            print("String is not in the correct format.")

        return {'FINISHED'}


def setNewMasterClock(self, context):

    context.scene.mm_master_time_frame = context.scene.frame_current

    scene = bpy.context.scene

    calc_master_frame = bpy.data.scenes[bpy.context.scene.name].mm_master_time_frame
    calc_master_time = bpy.data.scenes[bpy.context.scene.name].mm_master_time

    setWaterMasterTime(self, context)

    # go through all areas until sequence editor is found
    for area in bpy.context.screen.areas:
        if area.type == "SEQUENCE_EDITOR":
            override = bpy.context.copy()
            # change context to the sequencer
            override["area"] = area
            override["region"] = area.regions[-1]
            # run the command with the correct context
            with bpy.context.temp_override(**override):
                bpy.ops.sequencer.view_all()
            break


def arrange_strips():
    # Check if SEQUENCE_EDITOR is one of the areas in the current screen
    is_vse_open = any(
        area.type == 'SEQUENCE_EDITOR' for area in bpy.context.screen.areas)

    if is_vse_open:
        strips = bpy.context.scene.sequence_editor.sequences
        movie_strips = [s for s in strips if s.type == 'MOVIE']

        pairs = []

        for movie in movie_strips:
            movie_name_without_extension = movie.name.rsplit('.', 1)[0]
            associated_audio_name = f"{movie_name_without_extension}.001"

            associated_audio = next((audio for audio in strips if audio.name ==
                                    associated_audio_name and audio.type == 'SOUND'), None)

            # Pair the movie with the audio if found, otherwise with None
            pairs.append((movie, associated_audio))

        pairs.sort(key=lambda x: x[0].frame_final_duration, reverse=True)

        meta_strips = []
        next_channel = 3

        for movie, audio in pairs:
            bpy.ops.sequencer.select_all(action='DESELECT')
            movie.select = True
            if audio:  # Only select the audio if it exists
                audio.select = True

            bpy.ops.sequencer.meta_make()

            meta_strip = bpy.context.scene.sequence_editor.active_strip
            meta_strips.append(meta_strip)

            meta_strip.channel = next_channel
            next_channel += 1

        meta_strips.sort(key=lambda x: x.frame_final_duration, reverse=True)

        for idx, meta in enumerate(meta_strips, start=2):
            meta.channel = idx
            meta.frame_start = 1

        movie_and_meta_strips = [
            s for s in strips if s.type in ['MOVIE', 'META']]
        if movie_and_meta_strips:


            longest_strip = sorted(movie_and_meta_strips,
                                   key=lambda x: x.frame_final_duration, reverse=True)[0]
            
            # Deselect all strips and select only the longest strip.
            bpy.ops.sequencer.select_all(action='DESELECT')
            longest_strip.select = True
            print(longest_strip.name)
            # Adjust the VSE view range to fit the selected strip.
            bpy.ops.sequencer.view_all()
            bpy.ops.sequencer.set_range_to_strips()
            bpy.ops.sequencer.sound_strip


        print("Finished processing and arranging strips.")
        adjust_preview_transforms()
    else:
        print("Please switch to the Video Sequence Editor.")


def adjust_preview_transforms():
    # Fetch the scene's render resolution
    render = bpy.context.scene.render
    render_width = render.resolution_x
    render_height = render.resolution_y

    strips = bpy.context.scene.sequence_editor.sequences
    movie_strips = [s for s in strips if s.type == 'MOVIE' or s.type == 'META']

    num_clips = len(movie_strips)

    if num_clips == 0:
        print("No movie strips found!")
        return

    grid_cols = int(num_clips ** 0.5)
    grid_rows = (num_clips + grid_cols - 1) // grid_cols

    # Calculate the width and height of each cell in pixels
    cell_width = render_width / grid_cols
    cell_height = render_height / grid_rows

    for idx, strip in enumerate(movie_strips):
        # Determine grid position
        row = idx // grid_cols
        col = idx % grid_cols

        # Scale each strip so it fits within its grid cell
        strip.transform.scale_x = 1 / grid_cols
        strip.transform.scale_y = 1 / grid_rows

        # Positioning from center of screen in pixel units
        strip.transform.offset_x = -render_width/2 + (col + 0.5) * cell_width
        strip.transform.offset_y = render_height/2 - (row + 0.5) * cell_height






def check_string_format(string):
    # Split the string by colon ":"
    parts = string.split(":")
    print(parts)
    # Check if the string has exactly 4 parts separated by colons
    if len(parts) != 4:
        return False

    # Check if each part is a two-digit number
    for part in parts:
        if not part.isdigit() or len(part) != 2:
            return False

    return True


def setWaterMasterTime(self, context):

    scene = bpy.context.scene
    sequences = bpy.data.scenes[bpy.context.scene.name].sequence_editor.sequences
    # print(sequences)
    calc_master_frame = bpy.data.scenes[bpy.context.scene.name].mm_master_time_frame

    for sequence in sequences:
        if sequence.type == 'TEXT':
            if sequence.name == '@master.time':
                sequences.remove(sequence)
                break
    
    empty_channel = find_empty_channel(sequences)
    text_strip = bpy.data.scenes[bpy.context.scene.name].sequence_editor.sequences.new_effect(
        name="@master.time",
        type='TEXT',
        frame_start=scene.frame_start,
        frame_end=scene.frame_end,
        channel=empty_channel
    )
    text_strip.text = ''
    # Set the font and size for the text strip
    text_strip.font_size = 50.0
    # Set the position and alignment of the text strip
    text_strip.location = (0.05, 0.1)  # Set the position of the text strip
    text_strip.use_shadow = False
    text_strip.use_box = True
    text_strip.shadow_color = (0, 0, 0, 0)  # Set the shadow color
    # text_strip.wrap_width = 300  # Set the wrap width of the text strip
    text_strip.align_x = 'LEFT'  # Set the horizontal alignment
    text_strip.align_y = 'CENTER'  # Set the vertical alignment


def find_empty_channel(sequences):
    """Find the channel just above the highest occupied one."""
    max_channel = 0
    for seq in sequences:
        if seq.channel > max_channel:
            max_channel = seq.channel

    return max_channel + 1  # Return one above the highest occupied



class MM_OT_Master_Clock_Button_Move(Operator):
    bl_idname = "movematch.master_button_operator_move"
    bl_description = "Move the selected clip according to master clock"
    bl_label = "The strip might get over another clip"

    def execute(self, context):
        # button_function(self, context)
        # Get all markers

        # Calculates the difference between the marker and the specific adaptation time and moves the strip accordingly
        calculate_execute_the_strip_move(self, context, False)

        return {'FINISHED'}

    def invoke(self, context, event):

        is_moving_back = calculate_execute_the_strip_move(self, context, True)

        if is_moving_back:
            return context.window_manager.invoke_confirm(self, event)
        else:
            return self.execute(context)


def calculate_execute_the_strip_move(self, context, justcalc):

    # We need a marker for this operation
    markers = bpy.context.scene.timeline_markers
    # Get sequence editor
    seq_editor = bpy.context.scene.sequence_editor
    # Get the marker that is placed over the strip within its range and consider this the "orginin" frame
    for marker in markers:
        if seq_editor.active_strip.frame_final_start <= marker.frame <= seq_editor.active_strip.frame_final_end:
            
            # Projected frames from master clock
            int_master_frame = bpy.data.scenes[bpy.context.scene.name].mm_master_time_frame
            str_master_time = bpy.data.scenes[bpy.context.scene.name].mm_master_time
            str_master_time_adaption = bpy.data.scenes[bpy.context.scene.name].mm_master_time_adaption
            

            ################################
            # If timer is used 00:00:00:10 #
            ################################
            if str_master_time.startswith("00:00"):
                


                int_frame_from_master_clock = frame_from_smpte(str_master_time)
                markers_frame = marker.frame

                int_adapted_time_frame = frame_from_smpte(
                    str_master_time_adaption)



                str_smtp_at_zero = bpy.utils.smpte_from_frame(
                    (0 + int_frame_from_master_clock - int_master_frame))

                print("int_frame_from_master_clock")
                print(int_frame_from_master_clock)
                print("")
                print("")
                int_frames_at_zero = frame_from_smpte(str_smtp_at_zero)
                print("Where is the master clock zero time?")
                print(int_frames_at_zero)
         
                int_move_strip_frames = int_adapted_time_frame - int_frames_at_zero


                the_frame_change = markers_frame - int_move_strip_frames
                print("Where is the markerframe?")
                print(markers_frame)

                if markers_frame > int_frames_at_zero:
                    print("The marker is positive from master clock zero")
                    print(markers_frame - int_frames_at_zero)
                    print("I want the marker to end up at: ",
                          int_adapted_time_frame + int_frames_at_zero)
                    print("The difference between the marker and the strip_start = ",
                          seq_editor.active_strip.frame_start - markers_frame)

                    the_frame_change = (int_adapted_time_frame + int_frames_at_zero) - abs(seq_editor.active_strip.frame_start - markers_frame)

                elif markers_frame < int_frames_at_zero:
                    print("The marker is negative from master clock zero")
                    print(markers_frame - int_frames_at_zero)
                    print("I want the marker to end up at: ",
                          int_adapted_time_frame + int_frames_at_zero)
                    print("The difference between the marker and the strip_start = ", 
                          seq_editor.active_strip.frame_start - markers_frame)

                    the_frame_change = (int_adapted_time_frame + int_frames_at_zero) - abs(seq_editor.active_strip.frame_start - markers_frame)


                # Sends back a bool if the function only wanted to provide if the move is negative, see difference at def invoke
                if justcalc:
                    if the_frame_change > 0:
                        return True
                    else:
                        return False

                if the_frame_change < 0:
                    seq_editor.active_strip.frame_start = the_frame_change
                    bpy.context.scene.timeline_markers.remove(
                        bpy.context.scene.timeline_markers[marker.name])
                    bpy.context.window.scene.frame_current = round(
                        int_move_strip_frames)
                elif the_frame_change > 0:
                    seq_editor.active_strip.frame_start = the_frame_change
                    bpy.context.scene.timeline_markers.remove(
                        bpy.context.scene.timeline_markers[marker.name])
                    bpy.context.window.scene.frame_current = round(
                        int_move_strip_frames)
                elif the_frame_change == 0:
                    return {'FINISHED'}
                # Break to avoid it finding more markers and doing the loop again
                break

            ################################
            # If TIME is used 09:30:13:10  #
            ################################

            else:
                
                # Projected frames from master clock
                calc_master_frame = bpy.data.scenes[bpy.context.scene.name].mm_master_time_frame
                calc_master_time = bpy.data.scenes[bpy.context.scene.name].mm_master_time
                calc_master_time_adaption = bpy.data.scenes[bpy.context.scene.name].mm_master_time_adaption
                frames_from_master_clock = frame_from_smpte(calc_master_time)
                initial_frame = marker.frame

                frame_from_time_pusher = frame_from_smpte(
                    calc_master_time_adaption)

                smtp_at_zero = bpy.utils.smpte_from_frame(
                    (0 + frames_from_master_clock - calc_master_frame))

                
                frames_at_zero = frame_from_smpte(smtp_at_zero)

                actual_time_frame_from_pusher = frame_from_time_pusher - frames_at_zero

                the_frame_change = initial_frame - actual_time_frame_from_pusher

                # Sends back a bool if the function only wanted to provide if the move is negative, see difference at def invoke
                if justcalc:
                    if the_frame_change > 0:
                        return True
                    else:
                        return False

                if the_frame_change < 0:
                    seq_editor.active_strip.frame_start += abs(
                        the_frame_change)
                    bpy.context.scene.timeline_markers.remove(
                        bpy.context.scene.timeline_markers[marker.name])
                    bpy.context.window.scene.frame_current = round(
                        actual_time_frame_from_pusher)
                elif the_frame_change > 0:
                    seq_editor.active_strip.frame_start -= abs(
                        the_frame_change)
                    bpy.context.scene.timeline_markers.remove(
                        bpy.context.scene.timeline_markers[marker.name])
                    bpy.context.window.scene.frame_current = round(
                        actual_time_frame_from_pusher)
                elif the_frame_change == 0:
                    return {'FINISHED'}
                # Break to avoid it finding more markers and doing the loop again
                break


def frame_to_time(frame, fps):
    total_seconds = frame / fps
    h, remainder1 = divmod(total_seconds, 3600)
    m, remainder2 = divmod(remainder1, 60)
    s, ms = divmod(remainder2, 1)
    ms = round(ms * 1000)  # Convert fractional seconds to milliseconds
    return "{:02}:{:02}:{:02}.{:03}".format(int(h), int(m), int(s), ms)


def create_batch_file(commands, bat_filename):
    with open(bat_filename, 'w') as bat_file:
        bat_file.write("@echo off\n\n")

        bat_file.write("echo Here are the commands that will be executed:\n\n")

        for cmd in commands:
            bat_file.write("echo " + cmd + "\n")

        bat_file.write("\n")
        bat_file.write(
            'set /p user_input=Do you want to continue? (y/n): \n\n')

        bat_file.write('if /I "%user_input%"=="y" (\n')
        bat_file.write('    echo Running the commands...\n\n')

        for cmd in commands:
            bat_file.write("    " + cmd + "\n")

        bat_file.write(") else (\n")
        bat_file.write("    echo Aborting...\n")
        bat_file.write("    exit\n")
        bat_file.write(")\n")
        bat_file.write("pause\n")


def create_ffpmpeg():
    scene = bpy.context.scene
    # Correctly calculate the FPS
    fps = scene.render.fps / scene.render.fps_base
    sequences = bpy.data.scenes[bpy.context.scene.name].sequence_editor.sequences
    fps_rounded = round(fps, 2)
    # Get the full path
    full_path = bpy.data.filepath

    # Extract the file name from the path
    file_name = os.path.basename(full_path)
    file_name_without_extension = os.path.splitext(file_name)[0]
    ffmpeg_commands = []

    

    for sequence in sequences:
        if sequence.type == 'TEXT':
            text_sequence = sequence
            name = sequence.name
            first_name = name.split("_")[0]
            second_name = name.split("_")[0]

            if first_name == '@scene' or first_name == '@calibration':
                print(name)

                #######################################
                #          Let´s pack them up         #
                #######################################
                global_start_frame = int(text_sequence.frame_start)
                global_end_frame = int(text_sequence.frame_start + text_sequence.frame_final_duration)
                



                for strip in bpy.context.scene.sequence_editor.sequences:
                    if strip.type == 'META':
                        for sub_strip in strip.sequences:
                            if sub_strip.type == 'MOVIE':
                                video_name = sub_strip.name
                                break
                        else:
                            continue
                    elif strip.type == 'MOVIE':
                        video_name = strip.name
                    else:
                        continue
                    
                    video_name_no_extension = video_name

                    # Calculate start time
                    if strip.frame_start <= global_start_frame:
                        diff_start_frame = global_start_frame - strip.frame_start
                    else:
                        diff_start_frame = 0
                    cut_start_time = frame_to_time(
                        diff_start_frame, fps_rounded)
                    print("diff_start_frame ", diff_start_frame)

                    # Calculate end time
                    end_frame = strip.frame_start + strip.frame_final_duration
                    if end_frame >= global_end_frame:
                        diff_end_frame = strip.frame_final_duration - \
                            (end_frame - global_end_frame)
                    else:
                        diff_end_frame = (strip.frame_final_duration +
                                          strip.frame_start) - global_start_frame

                    cut_end_time = frame_to_time(diff_end_frame, fps_rounded)
                    print("diff_end_frame ", diff_end_frame)

                    ignore_sound = bpy.data.scenes[bpy.context.scene.name].mm_ignore_sound
                    if ignore_sound:
                        print("Ignore Sound")
                        ffmpeg_command = f"ffmpeg -i {video_name_no_extension} -ss {cut_start_time} -to {cut_end_time} -an {file_name_without_extension}/{text_sequence.name}/cut_{video_name_no_extension}"
                    else:
                        ffmpeg_command = f"ffmpeg -i {video_name_no_extension} -ss {cut_start_time} -to {cut_end_time} {file_name_without_extension}/{text_sequence.name}/cut_{video_name_no_extension}"
                    # Updated command to output in the 'movematch' directory
                    
                    ffmpeg_commands.append(ffmpeg_command)

    # Save commands to a .bat file
    script_directory = os.path.dirname(bpy.data.filepath)
    for sequence in sequences:
        if sequence.type == 'TEXT':
            text_sequence = sequence
            name = sequence.name
            first_name = name.split("_")[0]
            second_name = name.split("_")[0]

            if first_name == '@scene' or first_name == '@calibration':
                if not os.path.exists(os.path.join(script_directory, f"{file_name_without_extension}/{text_sequence.name}")):
                    os.makedirs(os.path.join(
                        script_directory, f"{file_name_without_extension}/{text_sequence.name}"))

    batch_file_path = os.path.join(
        script_directory, f"{file_name_without_extension}.bat")
    create_batch_file(ffmpeg_commands, batch_file_path)
    print(f"Commands saved to: {batch_file_path}")


