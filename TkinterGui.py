from tkinter import *
from PIL import ImageTk, Image
from scipy.io.wavfile import write
import sounddevice as sd
import Main
import os
import json


def record():
    global index
    global subtitles
    secondInCamtasia = 30
    durationTime = subtitles[index]["sentenceTimeLen"]*secondInCamtasia
    sentenceStartTime = subtitles[index]["sentenceStartTime"]

    hour = sentenceStartTime.hour
    min = sentenceStartTime.minute
    sec = sentenceStartTime.second
    min = min + hour*60
    sec = sec+min*60
    startTime = sec * 30

    # Sampling frequency
    freq = 44100
    # Recording duration
    duration = subtitles[index]["sentenceTimeLen"]
    recording = sd.rec(int(duration * freq),
                       samplerate=freq, channels=2)
    # Record audio for the given number of seconds
    sd.wait()
    # This will convert the NumPy array to an audio
    # file with the given sampling frequency
    audioName = "recording-"+str(index+1) + ".wav"
    audionameindex = "recording-"+str(index+1)
    path = r"B:\Work\DU\dubassistant\Camtasia Project.tscproj"
    write(os.path.join(path, audioName), freq, recording)
    # Read the Camtasia Json Template
    jsonFileName = "CamtasiaProject.json"
    camtasiaTemplate = open(os.path.join(path, jsonFileName), "r")
    json_object = json.load(camtasiaTemplate)
    camtasiaTemplate.close()
    json_object["timeline"]["id"] = len(subtitles)+1
    medias = json_object["timeline"]["sceneTrack"]["scenes"][0]["csml"]["tracks"][0]["medias"]

    media = {"id": len(subtitles)+index+2, "_type": "AMFile", "src": index+1, "trackNumber": 0, "attributes": {"ident": str(audionameindex), "gain": 1, "mixToMono": False, "loudnessNormalization": True},
             "channelNumber": "0,1", "effects": [], "start": startTime, "duration": durationTime, "mediaStart": 0, "mediaDuration": durationTime, "scalar": 1, "metadata": {"clipSpeedAttribute": False}, "animationTracks": {}}

    medias.append(media)
    json_object["timeline"]["sceneTrack"]["scenes"][0]["csml"]["tracks"][0]["medias"] = medias
    # Sources
    sourceBin = json_object["sourceBin"]
    source = {"id": index+1, "src": str(audioName), "rect": [0, 0, 0, 0], "lastMod": "20220214T112013", "loudnessNormalization": True, "sourceTracks": [{"range": [0, duration*10000000], "type": 2, "editRate": 10000000, "trackRect": [
                                           0, 0, 0, 0], "sampleRate": 44100, "bitDepth": 32, "numChannels": 2, "integratedLUFS": -49.6945558155127, "peakLevel": 0.022308349609375, "metaData": ""}], "metadata": {"timeAdded": "20220214T113239.084520"}}
    sourceBin.append(source)
    json_object["sourceBin"] = sourceBin
    a_file = open(os.path.join(path, jsonFileName), "w")
    json.dump(json_object, a_file)
    a_file.close()


def Increase():
    global index
    global subtitles
    length = len(subtitles)
    index = index+1
    if index > length-1:
        index = length-1
    sentenselabel.config(text=subtitles[index]["sentence"])
    sentencestarttimelabel.config(text=subtitles[index]["sentenceStartTime"])
    sentenceendtimelabel.config(text=subtitles[index]["sentenceEndTime"])
    sentencetimelenlabel.config(text=subtitles[index]["sentenceTimeLen"])
    indexlabel.config(text=index+1)


def Decrease():
    global index
    global subtitles
    index = index-1
    if index < 0:
        index = 0
    sentenselabel.config(text=subtitles[index]["sentence"])
    sentencestarttimelabel.config(text=subtitles[index]["sentenceStartTime"])
    sentenceendtimelabel.config(text=subtitles[index]["sentenceEndTime"])
    sentencetimelenlabel.config(text=subtitles[index]["sentenceTimeLen"])
    indexlabel.config(text=index+1)


text = ""
index = 0


root = Tk()
root.geometry("700x850")
root.title("DubberEnFa")
root.configure(bg='#1f1f1f')
logo = PhotoImage(file="logo.png")
img = ImageTk.PhotoImage(Image.open("logo.png"))
root.iconphoto(False, logo)
subtitles = Main.main()
templateFile = open("CamtasiaTemplate.json", "r")
template = json.load(templateFile)
path = r"B:\Work\DU\dubassistant\Camtasia Project.tscproj"
jsonFileName = "CamtasiaProject.json"
# Serializing json
json_object = json.dumps(template, indent=4)
with open(os.path.join(path, jsonFileName), "w") as outfile:
    outfile.write(json_object)
sentence = subtitles[0]['sentence']
sentenceStartTime = subtitles[0]["sentenceStartTime"]
sentenceEndTime = subtitles[0]["sentenceEndTime"]
sentenceTimeLen = subtitles[0]["sentenceTimeLen"]
myframe = Frame(root)
myframe.pack()

logoLabel = Label(root, image=img, bg='#1f1f1f')
logoLabel.pack()
appNameLabel = Label(root, text=Main.persianTextReshape(
    "نرم افزار دستیار دوبله DubberEnFa"), bg='#1f1f1f', fg="white", font="tahoma 18")
appNameLabel.pack()
increasebutton = Button(root, text=Main.persianTextReshape(
    "جمله بعدی<<"), command=Increase, border=0, font="tahoma 14", fg="white", bg='#1d314f')
increasebutton.pack(pady=5)
decreasebutton = Button(root, text=Main.persianTextReshape(
    "جمله قبلی>>"), command=Decrease, border=0, font="tahoma 14", fg="white", bg='#1d314f')
decreasebutton.pack(pady=5)

# Index
indexlabelplaceholder = Label(
    text=Main.persianTextReshape("شماره جمله:"), font="tahoma 12 bold", fg="white", bg='#1f1f1f')
indexlabelplaceholder.pack()
indexlabel = Label(root, text=index+1, font="14", fg="white", bg='#2e2e2e')
indexlabel.pack(pady=5)
# Sentence
sentenselabelplaceholder = Label(
    text=Main.persianTextReshape("جمله:"), font="tahoma 12 bold", fg="white", bg='#1f1f1f')
sentenselabelplaceholder.pack()
sentenselabel = Label(root, text=sentence,
                      font="tahoma 14", fg="white", bg='#2e2e2e')
sentenselabel.pack(pady=5)
# Sentence Start Time
sentencestarttimelabelplaceholder = Label(
    text=Main.persianTextReshape("زمان شروع جمله:"), font="tahoma 8 bold", fg="white", bg='#1f1f1f')
sentencestarttimelabelplaceholder.pack()
sentencestarttimelabel = Label(
    root, text=sentenceStartTime, font="tahoma 14", fg="white", bg='#2e2e2e')
sentencestarttimelabel.pack(pady=5)
# Sentence End Time
sentenceendtimelabelplaceholder = Label(
    text=Main.persianTextReshape("زمان پایان جمله:"), font="tahoma 8 bold", fg="white", bg='#1f1f1f')
sentenceendtimelabelplaceholder.pack()
sentenceendtimelabel = Label(
    root, text=sentenceEndTime, font="tahoma 14", fg="white", bg='#2e2e2e')
sentenceendtimelabel.pack(pady=5)
# Sentence Time Length
sentencetimelenlabelplaceholder = Label(
    text=Main.persianTextReshape("طول جمله(ثانیه):"), font="tahoma 8 bold", fg="white", bg='#1f1f1f')
sentencetimelenlabelplaceholder.pack()
sentencetimelenlabel = Label(
    root, text=sentenceTimeLen, font="tahoma 14", fg="white", bg='#2e2e2e')
sentencetimelenlabel.pack(pady=5)
# Record form
recordbutton = Button(root, font="tahoma 13", border=0, fg="white",
                      bg='#325fbf', text=Main.persianTextReshape("ضبط صدا"), command=record)
recordbutton.pack(pady=10)
root.mainloop()
