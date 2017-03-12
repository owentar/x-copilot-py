import speech_recognition as sr
from commands import parseCommand
from recognizer import Recognizer

r = Recognizer()
with sr.Microphone() as source:
    print("Say a command:")
    audio = r.listen(source)

# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    strCommand = r.recognize_sphinx2(audio)
    print("We've got something! --> " + strCommand)
    command = parseCommand(strCommand)
    if command is None:
        print("Command unrecognized: " + strCommand)
    else:
        print("Command recognized: " + command.name + ":" + str(command.dataRefs["sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot"]))
except sr.UnknownValueError:
    print("Sphinx Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
