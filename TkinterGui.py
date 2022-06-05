from tkinter import *
from PIL import ImageTk, Image
from scipy.io.wavfile import write
import sounddevice as sd
import Main
import os
import json
from tkinter import filedialog as fd
from tkinter.messagebox import *
from pathlib import Path


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
    sentenselabel.config(text=Main.translateText(
        'en', 'fa', subtitles[index]["sentence"]))
    sentencestarttimelabel.config(text=subtitles[index]["sentenceStartTime"])
    sentenceendtimelabel.config(text=subtitles[index]["sentenceEndTime"])
    sentencetimelenlabel.config(text=subtitles[index]["sentenceTimeLen"])
    indexlabel.config(text=index+1)


def Decrease():
    global index
    global subtzitles
    index = index-1
    if index < 0:
        index = 0
    sentenselabel.config(text=Main.translateText(
        'en', 'fa', subtitles[index]["sentence"]))
    sentencestarttimelabel.config(text=subtitles[index]["sentenceStartTime"])
    sentenceendtimelabel.config(text=subtitles[index]["sentenceEndTime"])
    sentencetimelenlabel.config(text=subtitles[index]["sentenceTimeLen"])
    indexlabel.config(text=index+1)


def finish():
    global root
    path = r"B:\Work\DU\dubassistant\Camtasia Project.tscproj"
    jsonFileName = "CamtasiaProject.json"
    CamtasiaProjectFileName = "CamtasiaProject.tscproj"
    camtasiaTemplate = open(os.path.join(path, jsonFileName), "r")
    json_object = json.load(camtasiaTemplate)
    a_file = open(os.path.join(path, CamtasiaProjectFileName), "w")
    json.dump(json_object, a_file)
    a_file.close()
    root.destroy()


def changeFrame():
    introFrame.pack_forget()
    mainFrame.pack()


def selectSubtitleFile():
    global startbutton
    global subtitles
    global sentence
    global sentenceStartTime
    global sentenceEndTime
    global sentenceTimeLen
    subtitleFileTypes = (
        ('subtitle files', '*.srt'),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(
        title=Main.persianTextReshape('انتخاب فایل زیرنویس'),
        initialdir='/',
        filetypes=subtitleFileTypes)

    if(len(filename) > 0):
        path = Path(filename)
        subtitles = Main.main(path)
        if len(subtitles) > 0:
            sentence = Main.translateText('en', 'fa', subtitles[0]['sentence'])
            sentenceStartTime = subtitles[0]["sentenceStartTime"]
            sentenceEndTime = subtitles[0]["sentenceEndTime"]
            sentenceTimeLen = subtitles[0]["sentenceTimeLen"]
            Increase()
            Decrease()
            startbutton.pack(pady=10)
        else:
            showerror(
                title='خطا',
                message='خطایی در پردازش زیرنویس رخ داده است.'
                )
    else:
        showwarning(
            title='اخطار',
            message='فایلی انتخاب نشد! لطفا یک فایل را انتخاب کنید.',
            )


text = ""
index = 0

root = Tk()
root.geometry("700x850")
root.title("DubberEnFa")
root.configure(bg='#1f1f1f')
logo = PhotoImage(file="logo.png")
img = ImageTk.PhotoImage(Image.open("logo.png"))
root.iconphoto(False, logo)

subtitles = [{'sentence': '', 'sentenceStartTime': '',
              'sentenceEndTime': '', 'sentenceTimeLen': ''}]

templateFile = open("CamtasiaTemplate.json", "r")
template = json.load(templateFile)
path = r"B:\Work\DU\dubassistant\Camtasia Project.tscproj"
jsonFileName = "CamtasiaProject.json"
for file in os.listdir(path):
    base_file, ext = os.path.splitext(file)
    if ext == '.wav':
        os.remove(path + '\\'+file)
# Serializing json
json_object = json.dumps(template, indent=4)
with open(os.path.join(path, jsonFileName), "w") as outfile:
    outfile.write(json_object)
sentence = subtitles[0]['sentence']
sentenceStartTime = subtitles[0]["sentenceStartTime"]
sentenceEndTime = subtitles[0]["sentenceEndTime"]
sentenceTimeLen = subtitles[0]["sentenceTimeLen"]

mainFrame = Frame(root)
mainFrame.configure(bg='#1f1f1f')
introFrame = Frame(root)
introFrame.configure(bg='#1f1f1f')
introFrame.pack()
filePickFrame = Frame(root)
filePickFrame.configure(bg='#1f1f1f')
filePickFrame.pack()
logoLabel = Label(mainFrame, image=img, bg='#1f1f1f')
logoLabel.pack()
appNameLabel = Label(mainFrame, text=Main.persianTextReshape(
    "نرم افزار دستیار دوبله DubberEnFa"), bg='#1f1f1f', fg="white", font="tahoma 18")
appNameLabel.pack()
logoLabel1 = Label(introFrame, image=img, bg='#1f1f1f')
logoLabel1.pack()
appNameLabel1 = Label(introFrame, text=Main.persianTextReshape(
    "نرم افزار دستیار دوبله DubberEnFa"), bg='#1f1f1f', fg="white", font="tahoma 18")
appNameLabel1.pack()
increasebutton = Button(mainFrame, text=Main.persianTextReshape(
    "جمله بعدی<<"), command=Increase, border=0, font="tahoma 14", fg="white", bg='#1d314f')
increasebutton.pack(pady=5)
decreasebutton = Button(mainFrame, text=Main.persianTextReshape(
    "جمله قبلی>>"), command=Decrease, border=0, font="tahoma 14", fg="white", bg='#1d314f')
decreasebutton.pack(pady=5)

# Index
indexlabelplaceholder = Label(mainFrame, text=Main.persianTextReshape(
    "شماره جمله:"), font="tahoma 12 bold", fg="white", bg='#1f1f1f')
indexlabelplaceholder.pack()
indexlabel = Label(mainFrame, text=index+1, font="14",
                   fg="white", bg='#2e2e2e')
indexlabel.pack(pady=5)
# Sentence
sentenselabelplaceholder = Label(mainFrame, text=Main.persianTextReshape(
    "جمله:"), font="tahoma 12 bold", fg="white", bg='#1f1f1f')
sentenselabelplaceholder.pack()
sentenselabel = Label(mainFrame, text=sentence,
                      font="tahoma 14", fg="white", bg='#2e2e2e')
sentenselabel.pack(pady=5)
# Sentence Start Time
sentencestarttimelabelplaceholder = Label(mainFrame, text=Main.persianTextReshape(
    "زمان شروع جمله:"), font="tahoma 8 bold", fg="white", bg='#1f1f1f')
sentencestarttimelabelplaceholder.pack()
sentencestarttimelabel = Label(
    mainFrame, text=sentenceStartTime, font="tahoma 14", fg="white", bg='#2e2e2e')
sentencestarttimelabel.pack(pady=5)
# Sentence End Time
sentenceendtimelabelplaceholder = Label(mainFrame, text=Main.persianTextReshape(
    "زمان پایان جمله:"), font="tahoma 8 bold", fg="white", bg='#1f1f1f')
sentenceendtimelabelplaceholder.pack()
sentenceendtimelabel = Label(
    mainFrame, text=sentenceEndTime, font="tahoma 14", fg="white", bg='#2e2e2e')
sentenceendtimelabel.pack(pady=5)
# Sentence Time Length
sentencetimelenlabelplaceholder = Label(mainFrame, text=Main.persianTextReshape(
    "طول جمله(ثانیه):"), font="tahoma 8 bold", fg="white", bg='#1f1f1f')
sentencetimelenlabelplaceholder.pack()
sentencetimelenlabel = Label(
    mainFrame, text=sentenceTimeLen, font="tahoma 14", fg="white", bg='#2e2e2e')
sentencetimelenlabel.pack(pady=5)
# Record form
recordbutton = Button(mainFrame, font="tahoma 13", border=0, fg="white",
                      bg='#325fbf', text=Main.persianTextReshape("ضبط صدا"), command=record)
recordbutton.pack(pady=10)

finishbutton = Button(mainFrame, font="tahoma 13", border=0, fg="white",
                      bg='#325fbf', text=Main.persianTextReshape("اتمام دوبله"), command=finish)
finishbutton.pack(pady=10)
startbutton = Button(introFrame, font="tahoma 13", border=0, fg="white",
                     bg='#325fbf', text=Main.persianTextReshape("شروع"), command=changeFrame)

open_button = Button(introFrame,
                     font="tahoma 13", border=0, fg="white",
                     bg='#325fbf', text=Main.persianTextReshape("انتخاب فایل زیرنویس"), command=selectSubtitleFile)

open_button.pack(expand=True)
root.mainloop()
