import speech_recognition as sr
from commands import parseCommand

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say a command:")
    audio = r.listen(source)

# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    strCommand = r.recognize_google(audio)
    print("We've got something!")
    command = parseCommand(strCommand)
    if command is None:
        print("Command unrecognized: " + strCommand)
    else:
        print("Command recognized: " + command.name + ":" + command.dataRefs["sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot"].value)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
