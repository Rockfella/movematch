import bpy


from bpy.types import Panel


class MM_PT_Step3Panel(bpy.types.Panel):
    bl_label = "When video clips have been imported"
    bl_idname = "SEQUENCER_PT_step3_panel"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'MoveMatch'

    def draw(self, context):
        layout = self.layout

        # Place the button in the panel
        layout.operator("movematch.arrange_channels")


class MM_PT_Panel(Panel):
    bl_label = "Master Clock"
    bl_idname = "SEQUENCER_PT_movematch_panel"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'MoveMatch'

    def draw(self, context):
        layout = self.layout
        # Get sequence editor
        seq_editor = bpy.context.scene.sequence_editor

        # Get all markers
        markers = bpy.context.scene.timeline_markers
        # Add a button with a callback to the button_function
        
        # layout.operator("myaddon.round_fps_button_operator")
        layout.operator("movematch.master_button_operator")
        layout.prop(context.scene, "mm_master_time", text="Time",
                    expand=True)
        scene = bpy.context.scene
        for strip in scene.sequence_editor.sequences_all:
            if strip.type == 'TEXT':
                if strip.name == '@master.time':

                    layout.prop(context.scene, "mm_master_time_adaption", text="Adapt",
                                expand=True)
                    row = layout.row()

                    row = layout.row()
                    #row.operator("object.adaption_info_button",
                    #             text="", icon='QUESTION')

                    #layout.operator(
                    #    "movematch.master_button_operator_push", text="Adapt Clip to Master Clock")

                    # A new option to move the strip according the the master time will pop up, if there is a meta strip selected and there is a marker placed within its range, that one will be used to move the strip according to master clock
                    if seq_editor.active_strip:

                        if seq_editor.active_strip.type == 'META':

                            for marker in markers:
                                if seq_editor.active_strip.frame_final_start <= marker.frame <= seq_editor.active_strip.frame_final_end:

                                    layout.operator(
                                        "movematch.master_button_operator_move", text="Move Clip")



