# X-Copilot

[![Build Status](https://travis-ci.org/owentar/x-copilot.svg?branch=master)](https://travis-ci.org/owentar/x-copilot-py)

This is a Python plugin for [X-Plane](http://www.x-plane.com/) to support voice commands in the simulator.

## Installation

X-Copilot runs in python, so to be able to use it in X-Plane, you will need to have installed [Python 2](https://www.python.org/downloads/release) in your system and [Sandy Barbour's Python Interface plugin](http://www.xpluginsdk.org/python_interface.htm) in x-plane.

#### Installing dependencies

With python installed on your system, execute the ```install.bat``` file. This will install all the python packages required by the speech recognition library.

Check [dependencies](https://github.com/Uberi/speech_recognition#pyaudio-for-microphone-users) required by speech_recognition project to support pyaudio. Install the required packages for your platform.

> **Windows users:** make sure your python installation directory is on your PATH environment variable as well as the python/scripts directory. This should have be done automatically by the python installer. If not, try to reinstall python 2 and make sure to check the option to install python.exe in your PATH.

> **Mac users:** you need to have already installed 'portaudio' package. If you have homebrew you can just do 'brew install portaudio'. You may need to execute the install.sh file with sudo privileges.

#### Quick verification

You can verify that all dependencies are installed and X-Copilot is working properly running the ```try-it.bat``` file in the console. Make sure your Microphone is plugged in and is working properly. When you run it, it will ask you for a command, then say:

> "SET ATLIMETER TWO NINE NINE TWO"

The output should look like this:

> $ Say a command...

> $ Command recognized: SET_ALTIMETER:29.92

If the command is not recognized, the output should be:

> Command not recognized:

#### Installing and setting up the X-Plane plugin

Finally, copy the ```PI_xcopilot``` file and ```xcopilot``` folder into the PythonScripts folder (```<X-PLANE-INSTALLATION-DIR>\Resources\plugins\PythonScripts```).

In X-Plane, go to ```Settings -> Buttons: Adv -> custom cmnds from plugins``` and assign a key / button for ```xcopilot/record_voice_command```. Every time that you want to say a command to X-Copilot, just press this button once (no need to keep pressing it while recording) and say one of the supported commands. A window should popup in the sim notifying the current state of X-Copilot (Recoding, Command recognized or Command not recognized).

## Technical / Dev notes

### How does it work?

The process is quite simple:

1. Transcribe voice commands to text using [speech_recognition](https://github.com/Uberi/speech_recognition) project.
2. When the command is in a string format, it's parsed through a regular expression to identify and extract the data from the specified command
3. Once the command is recognized, it's translated to data ref operations (setting / getting one or more data refs in x-plane)

### Pocketsphinx configuration

Currently the language used by sphinx to recognize commands is specified in corpus.txt file.

To create the language model, go to: http://www.speech.cs.cmu.edu/tools/lmtool-new.html, upload the corpus.txt and get the LM and DIC files content and replace the existing ones defined in pockectsphinx-data/xp-XP folder.

### Test

> $ python -m unittest discover

### Package

> $ python setup.py sdist
