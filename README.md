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

[Download ffmpeg from official site: ](https://ffmpeg.org/download.html)

### Blender

Detailed information or points related to Subsection 1.2.
[Download blender from official site: ](https://www.blender.org/download/)



### MoveMatch - blender addon
Install addon in blender: 
Blender -> Edit -> Preferences -> Add-ons -> Install -> Find zip file and enable (the left check box)
Under Video Sequencer - New File - Video Editing -> Sequencer toggle "n" panel, see MoveMatch tab

[Download this addon](https://github.com/Rockfella/movematch/archive/refs/heads/main.zip)


---

## How to use


### Add your recordings and arrange clips

Start by adding your recordings, it can be one large file or multiple smaller ones:

Link to gif scene 0...


### Set Master Clock

After that, set the master clock and move the clips using the Move function. 

[See how](https://i.imgur.com/2u7YDm0.gif)

### Set Cuts - annotation

Press the Calibration or Scene button

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