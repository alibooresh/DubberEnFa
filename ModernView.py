import tkinter
import tkinter.messagebox
import customtkinter
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
import pyloudnorm as pyln
import soundfile as sf


# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")
text = ""
index = 0
sentence=''
sentenceStartTime=''
sentenceEndTime=''
sentenceTimeLen=''

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # local variables
        
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
        global sentence
        global sentenceStartTime
        global sentenceEndTime
        global sentenceTimeLen
        sentence = subtitles[0]['sentence']
        sentenceStartTime = subtitles[0]["sentenceStartTime"]
        sentenceEndTime = subtitles[0]["sentenceEndTime"]
        sentenceTimeLen = subtitles[0]["sentenceTimeLen"]
        # configure window
        self.title("DubberEnFa")
        self.geometry(f"{1100}x{580}")

        # # configure grid layout (4x4)
        # self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure((0,2), weight=0)
        # self.grid_rowconfigure((0, 1, 2), weight=0)

        # configure logo
        image_path = os.path.join(os.path.dirname(os.path.realpath(
            __file__)), "./")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(
            image_path, "logo.png")), size=(100, 110))
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text='', image=self.logo_image,font=customtkinter.CTkFont(family="tahoma", size=25))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.title_label = customtkinter.CTkLabel(
            self.sidebar_frame, text=Main.persianTextReshape(
                "نرم افزار دستیار دوبله DubberEnFa"), font=customtkinter.CTkFont(family="tahoma", size=25))
        self.title_label.grid(row=1, column=0, padx=20, pady=(20, 10))

        self.sidebar_open_subtitle = customtkinter.CTkButton(
            self.sidebar_frame, text=Main.persianTextReshape("انتخاب فایل زیرنویس"), font=("tahoma", 15), command=self.open_subtite_file)
        self.sidebar_open_subtitle.grid(row=2, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text=Main.persianTextReshape("تم برنامه:"), font=("tahoma", 18), anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event, font=("tahoma", 15))
        self.appearance_mode_optionemenu.grid(
            row=6, column=0, padx=20, pady=(10, 10))

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(
            self.sidebar_frame, fg_color="transparent")
        self.slider_progressbar_frame.grid(
            row=3, column=0, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.progressbar_1 = customtkinter.CTkProgressBar(
            self.slider_progressbar_frame)

        # sentence detail
        ## labels
        # self.sentence_label = customtkinter.CTkLabel(
        #     self, text=Main.persianTextReshape(
        #         "جمله:"), font=("tahoma", 18))
        # self.sentence_label.grid(row=1, column=3, padx=(
        #     20, 20), pady=(20, 20), sticky="nsew")

        # self.entry_sentence = customtkinter.CTkEntry(
        #     self, width=120,height=25, placeholder_text="CTkEntry")
        # self.entry_sentence.grid(row=1, column=1, columnspan=2, padx=(
        #     20, 0), pady=(20, 20), sticky="nsew")



        # self.sentence_start_time_label = customtkinter.CTkLabel(
        #     self, text=Main.persianTextReshape(
        #         "زمان شروع جمله:"), font=("tahoma", 18))
        # self.sentence_start_time_label.grid(
        #     row=2, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        # self.sentence_end_time_label = customtkinter.CTkLabel(
        #     self, text=Main.persianTextReshape(
        #         "زمان پایان جمله:"), font=("tahoma", 18))
        # self.sentence_end_time_label.grid(
        #     row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        # self.sentence_time_len_label = customtkinter.CTkLabel(
        #     self, text=Main.persianTextReshape(
        #         "طول جمله(ثانیه):"), font=("tahoma", 18))
        # self.sentence_time_len_label.grid(
        #     row=4, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        ## inputs
        
        # self.sentence_label = customtkinter.CTkLabel(
        #     self, text='', font=("tahoma", 18))
        # self.sentence_start_time_label = customtkinter.CTkLabel(
        #     self, text='', font=("tahoma", 18))
        # self.sentence_end_time_label = customtkinter.CTkLabel(
        #     self, text='', font=("tahoma", 18))
        # self.sentence_time_len_label = customtkinter.CTkLabel(
        #     self, text='', font=("tahoma", 18))

        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=0, column=1, columnspan=2, padx=(
            20, 0), pady=(20, 20), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(
            master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=0, column=3, padx=(
            20, 20), pady=(20, 20), sticky="nsew")

        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=1, column=1, columnspan=2, padx=(
            20, 0), pady=(20, 20), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(
            master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=1, column=3, padx=(
            20, 20), pady=(20, 20), sticky="nsew")

        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=2, column=1, columnspan=2, padx=(
            20, 0), pady=(20, 20), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(
            master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=2, column=3, padx=(
            20, 20), pady=(20, 20), sticky="nsew")

        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(
            20, 0), pady=(20, 20), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(
            master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(
            20, 20), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(
            master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=4, column=1, padx=(
            20, 20), pady=(20, 20), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(
            master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=4, column=2, padx=(
            20, 20), pady=(20, 20), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(
            master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=4, column=3, padx=(
            20, 20), pady=(20, 20), sticky="nsew")

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(
            text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
    
    def open_subtite_file(self):
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
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()
        filename = fd.askopenfilename(
            title=Main.persianTextReshape('انتخاب فایل زیرنویس'),
            initialdir='/',
            filetypes=subtitleFileTypes)

        if (len(filename) > 0):
            path = Path(filename)
            self.progressbar_1.grid(row=1, column=0, padx=(
                20, 10), pady=(10, 10), sticky="ew")
            subtitles = Main.main(path)
            if len(subtitles) > 0:
                previousIndex = 0
                for i in range(len(subtitles)):
                    if subtitles[i]['sentence'] == '':
                        previousIndex = i
                    else:
                        if i > 0 and subtitles[i-1]['sentence'] == '':
                            subtitles[i-1]['sentence'] = splitSentence(
                                subtitles[i]['sentence'])[0]
                            subtitles[i]['sentence'] = splitSentence(
                                subtitles[i]['sentence'])[1]
                sentence = Main.translateText('en', 'fa', subtitles[0]['sentence'])
                sentenceStartTime = subtitles[0]["sentenceStartTime"]
                sentenceEndTime = subtitles[0]["sentenceEndTime"]
                sentenceTimeLen = subtitles[0]["sentenceTimeLen"]
                # self.sentence_label.grid(row=1, column=1, columnspan=2, padx=(
                #     20, 0), pady=(20, 0), sticky="nsew")
                # self.sentence_start_time_label.grid(
                #     row=2, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
                # self.sentence_end_time_label.grid(
                #     row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
                # self.sentence_time_len_label.grid(
                #     row=4, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
                Increase(self)
                Decrease(self)

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


def splitSentence(sentence: str):
    sentArray = sentence.split()
    sentLen = len(sentArray)
    part1 = round(sentLen/2)
    part1Len = 0
    for i in range(part1):
        part1Len += len(sentArray[i])+1
    result = []
    result.append(sentence[:part1Len])
    result.append(sentence[part1Len:])
    return result


def Increase(self):
    global index
    global subtitles
    length = len(subtitles)
    index = index+1
    if index > length-1:
        index = length-1
    self.sentence_label.configure(text=Main.translateText(
        'en', 'fa', subtitles[index]["sentence"]))
    self.sentence_start_time_label.configure(
        text=subtitles[index]["sentenceStartTime"])
    self.sentence_end_time_label.configure(
        text=subtitles[index]["sentenceEndTime"])
    self.sentence_time_len_label.configure(
        text=subtitles[index]["sentenceTimeLen"])
    


def Decrease(self):
    global index
    global subtzitles
    index = index-1
    if index < 0:
        index = 0
    self.sentence_label.configure(text=Main.translateText(
        'en', 'fa', subtitles[index]["sentence"]))
    self.sentence_start_time_label.configure(
        text=subtitles[index]["sentenceStartTime"])
    self.sentence_end_time_label.configure(
        text=subtitles[index]["sentenceEndTime"])
    self.sentence_time_len_label.configure(
        text=subtitles[index]["sentenceTimeLen"])

if __name__ == "__main__":
    app = App()
    app.mainloop()
