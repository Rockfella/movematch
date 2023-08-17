@echo off

echo Here are the commands that will be executed:

echo ffmpeg -i 20150515024952_M0502N_0016.MP4 -ss 00:00:00.433 -to 00:00:32.632 movematch/cut_20150515024952_M0502N_0016.MP4
echo ffmpeg -i 20150220034906_M0779N_0008.MOV -ss 00:00:03.536 -to 00:00:35.735 movematch/cut_20150220034906_M0779N_0008.MOV

set /p user_input=Do you want to continue? (yes/no): 

if /I "%user_input%"=="yes" (
    echo Running the commands...

    ffmpeg -i 20150515024952_M0502N_0016.MP4 -ss 00:00:00.433 -to 00:00:32.632 movematch/cut_20150515024952_M0502N_0016.MP4
    ffmpeg -i 20150220034906_M0779N_0008.MOV -ss 00:00:03.536 -to 00:00:35.735 movematch/cut_20150220034906_M0779N_0008.MOV
) else (
    echo Aborting...
    exit
)
pause
