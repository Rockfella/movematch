import bpy
import datetime
from bpy.types import Operator
from .mm_global import frame_from_smpte


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

        if check_string_format(context.scene.master_time):
            print("String is in the correct format.")
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


def aarrange_strips():

    # Check if SEQUENCE_EDITOR is one of the areas in the current screen
    is_vse_open = any(
        area.type == 'SEQUENCE_EDITOR' for area in bpy.context.screen.areas)

    if is_vse_open:
        strips = bpy.context.scene.sequence_editor.sequences
    
        # Debugging print statements
        print(f"Total sequences found: {len(strips)}")
    
        movie_strips = [s for s in strips if s.type == 'MOVIE']
    
        # Debugging print statements
        print(f"Movie sequences found: {len(movie_strips)}")
    
        pairs = []
    
        for movie in movie_strips:
            associated_audio = None
            for audio in strips:
                if audio.type == 'SOUND' and audio.frame_start == movie.frame_start and audio.frame_final_end == movie.frame_final_end:
                    associated_audio = audio
                    break
                
            if associated_audio:
                pairs.append((movie, associated_audio))
    
        # Debugging print statements
        print(f"Paired movie and audio: {len(pairs)}")
    
        pairs.sort(key=lambda x: x[0].frame_final_duration, reverse=True)
    
        meta_strips = []
        next_channel = 3
        for movie, audio in pairs:
            bpy.ops.sequencer.select_all(action='DESELECT')
            movie.select = True
            audio.select = True
    
            bpy.ops.sequencer.meta_make()
    
            meta_strip = bpy.context.scene.sequence_editor.active_strip
            meta_strips.append(meta_strip)
    
            meta_strip.channel = next_channel
            next_channel += 1
    
        # Debugging print statements
        print(f"Meta strips created: {len(meta_strips)}")
    
        meta_strips.sort(key=lambda x: x.frame_final_duration, reverse=True)
    
        for idx, meta in enumerate(meta_strips, start=2):
            meta.channel = idx
            meta.frame_start = 1
    
        print("Finished processing and arranging strips.")


def arrange_strips():
    # Check if SEQUENCE_EDITOR is one of the areas in the current screen
    is_vse_open = any(
        area.type == 'SEQUENCE_EDITOR' for area in bpy.context.screen.areas)

    if is_vse_open:
        strips = bpy.context.scene.sequence_editor.sequences

        # Collect all movie strips (we'll check audio associated with them)
        movie_strips = [s for s in strips if s.type == 'MOVIE']

        pairs = []  # This will store (movie, audio) pairs

        for movie in movie_strips:
            movie_name_without_extension = movie.name.rsplit('.', 1)[0]
            associated_audio_name = f"{movie_name_without_extension}.001"

            associated_audio = next((audio for audio in strips if audio.name ==
                                    associated_audio_name and audio.type == 'SOUND'), None)

            if associated_audio:
                pairs.append((movie, associated_audio))
        # Debugging print statements
        print(f"Paired movie and audio: {len(pairs)}")

        pairs.sort(key=lambda x: x[0].frame_final_duration, reverse=True)

        meta_strips = []
        next_channel = 3
        for movie, audio in pairs:
            bpy.ops.sequencer.select_all(action='DESELECT')
            movie.select = True
            audio.select = True

            bpy.ops.sequencer.meta_make()

            meta_strip = bpy.context.scene.sequence_editor.active_strip
            meta_strips.append(meta_strip)

            meta_strip.channel = next_channel
            next_channel += 1

        # Debugging print statements
        print(f"Meta strips created: {len(meta_strips)}")

        meta_strips.sort(key=lambda x: x.frame_final_duration, reverse=True)

        for idx, meta in enumerate(meta_strips, start=2):
            meta.channel = idx
            meta.frame_start = 1
        # ... [rest of the code remains unchanged]

        print("Finished processing and arranging strips.")
    else:
        print("Please switch to the Video Sequence Editor.")

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

    text_strip = bpy.data.scenes[bpy.context.scene.name].sequence_editor.sequences.new_effect(
        name="@master.time",
        type='TEXT',
        frame_start=scene.frame_start,
        frame_end=scene.frame_end,
        channel=4
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
