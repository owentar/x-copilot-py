# X-Copilot

This is a Python plugin for [X-Plane](http://www.x-plane.com/) to support voice commands in the simulator.

## Installation

X-Copilot runs in python, so to be able to use it in X-Plane, you will need to have installed [Python 2](https://www.python.org/downloads/release) in your system and [Sandy Barbour's Python Interface plugin](http://www.xpluginsdk.org/python_interface.htm) in x-plane.

#### Installing dependencies

With python installed on your system, execute the ```install.bat``` file. This will install all the python packages required by the speech recognition library.

> **Windows users:** make sure your python installation directory is on your PATH environment variable as well as the python/scripts directory. This should have be done automatically by the python installer. If not, try to reinstall python 2 and make sure to check the option to install python.exe in your PATH.

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

### Conver language model to binary
Execute from x-copilot root folder:
```bash
sphinx_lm_convert -i ./xcopilot/pocketsphinx-data/xp-XP/language-model.lm -o ./xcopilot/pocketsphinx-data/xp-XP/language-model.lm.bin
```

### Train sphinx

1. Download sphinxbase, pocketsphinx and sphinxtrain from the [Sphinx toolkit](https://cmusphinx.github.io/wiki/tutorialoverview/).
2. Install sphinxbase:
```bash
./autogen.sh
./configure
make
make install
```
Note: you may need to run ```make install``` with root privileges. Check [here](https://cmusphinx.github.io/wiki/tutorialpocketsphinx/) for more details on how to install this packages.
3. Install pocketsphinx:
```bash
export LD_LIBRARY_PATH=/usr/local/lib
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
./configure
make
make install
```
4. Install sphinxtrain:
```bash
./configure
make
make install
```
5. Download [en-US acoustic model](https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/US%20English/), make sure you download the **ptm** version of it (like '''cmusphinx-en-us--ptm-X.Y'''). This is necessary since we need the source code of the acoustic model, not the binaries. Put the en-US folder inside the '''train-speech''' folder.
6. Inside the '''train-speech''' execute the training scripts
```bash
./train-speech.sh
```
7. And finally, update acoustic model with the training data
```bash
./adapt-model-map.sh
```
8. Finally, try it again and verify if the accuracy has improved after the training. (Executing the '''try-it.sh''')

### Test

> $ python -m unittest discover

### Package

> $ python setup.py sdist
