###INSTALL

- visit https://github.com/psychopy/psychopy/release and install PsychoPy2_PY3 (version 1.90.1)

###RUN

All files from this zip should be in the same folder
+ have a folder called "media" (/!\ no uppercase) inside this folder containing all the video files 

- Launch PsychoPy
- Click on File/


Run the file "run.py" from WITHIN PsychoPy

During the experiment :
	press SPACE key to skip to next video
	press ESCAPE anytime to quit everything


In the end output will be saved in current folder (with date of the expe in file name - no risk to overwrite previous files). 

###ADDITIONNALLY

- If psychopy was never installed, install this bunch of packages with command on the terminal:
  $ pip install numpy scipy matplotlib pandas pyopengl pyglet pillow moviepy lxml openpyxl configobj imageio cv2 pathlib

Needed on Windows:
$ pip install pypiwin32

Needed on macOS:
$ pip install pyobjc-core pyobjc-framework-Quartz


Then, still in the terminal : run 
$ python installScript.py (if anaconda was not on the laptop, install imageio)


Finally, find out which version of python your computer is running with:
$ python -V

If this is not a 3.something, then update to 3 using (still in terminal):
$ brew install python3 && cp /usr/local/bin/python3 /usr/local/bin/python

If you are lucky, that will be enough. For Alex, it was not enough. I had to:
- delete a bunch of dead links
- update brew
- brew update python
  Some of those steps were in hindsight not necessary, and they meant I lost the python2 installation I had.

NOTE: The VLC media player also needs to be installed on the psychopy computer.