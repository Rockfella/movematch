# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "MoveMatch",
    "author" : "Johan Sleman",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}
import bpy
from bpy.app.handlers import persistent
from . mm_panel import MM_PT_Panel, MM_PT_Step3Panel, MM_PT_Step4Panel, MM_PT_Step5Panel
from . mm_op import MM_OT_Master_Clock_Button, MM_OT_Master_Clock_Button_Move, MM_OT_ArrangeChannels, MM_OT_FfmpegCreate, MM_OT_NewCalibration, MM_OT_NewScene
from .mm_global import frame_from_smpte

classes = (MM_OT_Master_Clock_Button, MM_PT_Panel,
           MM_OT_Master_Clock_Button_Move, MM_PT_Step3Panel, MM_OT_ArrangeChannels, MM_OT_FfmpegCreate, MM_PT_Step5Panel, MM_OT_NewCalibration, MM_OT_NewScene, MM_PT_Step4Panel)

def master_time_updater(scene, depsgraph):

    # Projected frames from master clock
    calc_master_frame = bpy.data.scenes[bpy.context.scene.name].mm_master_time_frame
    calc_master_time = bpy.data.scenes[bpy.context.scene.name].mm_master_time
    
    frames_from_master_clock = frame_from_smpte(calc_master_time)

    for strip in scene.sequence_editor.sequences_all:
        if strip.type == 'TEXT':

            if strip.name == '@master.time':

                fps = bpy.context.scene.render.fps
                fps_base = bpy.context.scene.render.fps_base
                fps_real = fps / fps_base

                # Input SMPTE formatted string
                smpte_string_current = bpy.utils.smpte_from_frame(
                    (scene.frame_current + frames_from_master_clock - calc_master_frame), fps=fps, fps_base=fps_base)

                # Split the string using ":" as the delimiter
                hours_curr, minutes_curr, seconds_curr, frames_curr = smpte_string_current.split(
                    ":")

                strip.text = str(hours_curr) + ':' + str(minutes_curr) + \
                    ':' + str(seconds_curr) + '+' + str(frames_curr)


@persistent
def masterTimeUpdater(dummy):
    bpy.app.handlers.frame_change_pre.clear()
    bpy.app.handlers.frame_change_pre.append(master_time_updater)
    bpy.app.handlers.render_pre.append(master_time_updater)

def register():
    for c in classes:

        bpy.utils.register_class(c)

    bpy.types.Scene.mm_master_time = bpy.props.StringProperty(
        name="mm_master_time", default="00:00:00:00")
    bpy.types.Scene.mm_master_time_frame = bpy.props.IntProperty(
        name="mm_master_time_frame")
    bpy.types.Scene.mm_master_time_adaption = bpy.props.StringProperty(
        name="mm_master_time_adaption", default="00:00:00:00")
    bpy.app.handlers.load_post.append(masterTimeUpdater)

    bpy.types.Scene.mm_scene_free_channel = bpy.props.IntProperty(
        name="mm_scene_free_channel")
    bpy.types.Scene.mm_ignore_sound = bpy.props.BoolProperty(
        name="mm_ignore_sound", default=False)

    

def unregister():
    del bpy.types.Scene.mm_master_time
    del bpy.types.Scene.mm_master_time_adaption
    del bpy.types.Scene.mm_master_time_frame
    del bpy.types.Scene.mm_scene_free_channel
    del bpy.types.Scene.mm_ignore_sound

    for c in classes:

        bpy.utils.unregister_class(c)



