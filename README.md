# MoveMatch

MoveMatch is an addon designed for Blender that facilitates the synchronization of video material intended for use with "experimental" move.ai applications. By providing a user-friendly interface to add, order, and sync multiple video clips based on a master clock or specific events, MoveMatch streamlines the video preparation process.

---

## Table of Contents

1. [Installation](#Installation)
2. [How to use](#How-to-use)
3. [Concluding Remarks](#Concluding-Remarks)
4. [License](#License)


---

## Installation

Requirements
Blender: This addon is designed for Blender version 3.5.1. Make sure to have this version or newer installed.

FFmpeg: The automatic video processing feature requires FFmpeg to be installed on your system.

### ffmpeg

[Download ffmpeg from official site](https://ffmpeg.org/download.html)

### Blender


[Download blender from official site](https://www.blender.org/download/)



### MoveMatch - blender addon
Install addon in blender: 
Blender -> Edit -> Preferences -> Add-ons -> Install -> Find zip file and enable (the left check box)
Under Video Sequencer - New File - Video Editing -> Sequencer toggle "n" panel, see MoveMatch tab

[Download this addon](https://github.com/Rockfella/movematch/archive/refs/heads/main.zip)


---

## How to use
Before you get started there a few things that are important. Make sure that the video files does not have any special caracters in their name. 

Basic folder structure:
ProjectX
    -Cam1_Footage.mp4
    -Cam2_Footage.mp4
    -Cam3_Footage.mp4
    -Cam4_Footage.mp4
    -Cam5_Footage.mp4
    -Cam6_Footage.mp4
    -ProjectX.blend
    -"ProjectX.bat" - is created when done, open it and run
    -"ProjectX folder"
        -@Calibration
        -@Scene_1
        -@Scene_2 etc..

When you are selecting the "master time" and "move time" be sure to select the frame where the second is changeing. If timer is used, remember that there is milliseconds in the end the input 00:00:00:00,
is format HH:MM:SS:FF where FF is frames. SO if you pick the "second change" make sure to have FF = 00. 

### Add your recordings and arrange clips

Start by adding your recordings, it can be one large file or multiple smaller ones:

[See how](https://i.imgur.com/ssB1Rv3.gif)

IF YOU EXPERIENCE LAG WHEN ADDING MULTIPLE CLIPS, PLEASE TOGGLE "n" INSIDE THE PREVIEW WINDOW. VIEW -> USE PROXIES -> PROXY RENDER 25%-50%


### Set Master Clock

After that, set the master clock and move the clips using the Move function. 

[See how](https://i.imgur.com/EtameVt.gif)


### Set Cuts - annotation

Press the Calibration or Scene button, make sure that all videos "on each channel" is within the start - end frame of the annotations. Otherwise it will fail to cut the video later on. 

### Create ffmpeg script and run

Remember to save the .blend file in the same directory as the video clips, then press the Create FFMPEG button. 
This creates a .bat file with the same file name as the blend file. Open it in the same directory as the clips and blend file. 

The .bat file uses ffmpeg to cut out the right portions of the video clips and copies them to a new project folder. 

---

---

## Concluding Remarks

I hope this addon will help users who are experimenting with move.ai

---

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.