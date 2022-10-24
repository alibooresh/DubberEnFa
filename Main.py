#!/usr/bin/python
import re
import datetime
from googletrans import Translator
import arabic_reshaper
from bidi.algorithm import get_display

translator = Translator()


def translateText(src: str, dest: str, text: str) -> str:
    if(len(text) > 0):
        result = translator.translate(src=src, dest=dest, text=text)
        return persianTextReshape(result.text)
    else:
        return ''


def persianTextReshape(text):
    reshaped_text = arabic_reshaper.reshape(text)    # correct its shape
    bidi_text = get_display(reshaped_text)
    return bidi_text


def strToDate(strTime) -> datetime:
    times = strTime.split(",")
    seperated = times[0].split(":")
    hour = 0
    minute = 0
    second = 0
    milisec = 0
    if(len(strTime) > 0):
        hour = int(seperated[0])
        minute = int(seperated[1])
        second = int(seperated[2])
        milisec = int(times[1])
    return (datetime.time(hour=hour, minute=minute,
                          second=second, microsecond=milisec))


def strToDateTime(strTime) -> datetime:
    times = strTime.split(",")
    seperated = times[0].split(":")
    hour = 0
    minute = 0
    second = 0
    milisec = 0
    if(len(strTime) > 0):
        hour = int(seperated[0])
        minute = int(seperated[1])
        second = int(seperated[2])
        milisec = int(times[1])
    return (datetime.datetime(year=2000, month=1, day=1, hour=hour,
                              minute=minute, second=second, microsecond=milisec))


def getTimeLen(lineStartTime, lineEndTime) -> int:
    diffLen = 0
    start = strToDateTime(lineStartTime)
    end = strToDateTime(lineEndTime)
    diffrent = end - start
    seconds_in_day = 24 * 60 * 60
    diffLen = divmod(
        diffrent.days * seconds_in_day + diffrent.seconds, 60)[1]
    if diffLen < 1:
        diffLen = 1
    return diffLen


def displaySentences(sentences):
    print('displaying sentences with order and structure \n')
    for sentence in sentences:
        print('******************************'
              + str(sentence['id'])+'********************************')
        print()
        print('Sentence is :'+'\t\t =>\t' + sentence['sentence'])
        print()
        print('Start Time is :'+'\t\t =>\t'
              + str(sentence['sentenceStartTime']))
        print()
        print('End Time is :'+'\t\t =>\t' + str(sentence['sentenceEndTime']))
        print()
        print('Time Length is :'+'\t\t =>\t'
              + str(sentence['sentenceTimeLen']))


def getSentenceType(text: str):
    return


def main(path: str) -> list:
    lineStartTime = ''
    lineEndTime = ''
    lineTimeLen = 0
    sentenceStartTime = ''
    sentenceEndTime = ''
    sentenceTimeLen = 0
    sentence = ''
    previousText = ''
    willAddOriginalSentence = ''
    id = 1
    sentences = []
    print("\t\t******** Starting Process... ********")
    print("\t\t******** Reading SRT File... ********")
    try:
        file = open(path, mode='r', encoding='utf-8')
    except:
        print('Error Reading File')
    subtitleLines = file.read()
    splited = subtitleLines.split('\n')
    lines = []
    for line in splited:
        if(len(line) > 0):
            lines.append(line)

    print("\t\t******** Processing Subtitles... ********")
    for index in range(0, len(lines)):
        sentence = lines[index]
        isTime = re.search(r'-->', sentence, re.M | re.I)
        isLineNum = re.search(r'^\s*\d+\s*$', sentence, re.M | re.I)
        isText = not(bool(re.search(r'-->', sentence, re.M | re.I))) and not(
            bool(re.search(r'^\s*\d+\s*$', sentence, re.M | re.I)))

        if(isTime):
            timeInfo = sentence.split("-->")
            lineStartTime = timeInfo[0]
            lineEndTime = timeInfo[1]
            sentenceStartTime = strToDate(lineStartTime)
            sentenceEndTime = strToDate(lineEndTime)
            sentenceTimeLen = getTimeLen(lineStartTime, lineEndTime)
        if(isLineNum):
            if(index > 0):
                tmpDic = {
                    "id": id,
                    "sentenceStartTime": sentenceStartTime,
                    "sentenceEndTime": sentenceEndTime,
                    "sentence": willAddOriginalSentence,
                    "sentenceTimeLen": sentenceTimeLen
                    }
                sentences.append(tmpDic)
                sentenceStartTime = ''
                sentenceEndTime = ''
                sentenceTimeLen = 0
                willAddOriginalSentence = ''
                id = id+1

        if(isText):  # Line have text
            isContainSentence = re.search(
                r'\s*[^.!?]*[.!?]', sentence, re.M | re.I)
            isCompleteSentense = re.search(
                r'\s*[^.!?]*[.!?]', sentence, re.M | re.I)
            textList = re.findall(r'\s*[^.!?]*[.!?]', sentence, re.M | re.I)
            if(isContainSentence):  # Text have sentence(es)
                sentenceLen = 0
                for lineIndex in range(0, len(textList)):
                    line = textList[lineIndex]
                    sentenceLen = + len(line)
                    isCompleteSentense = re.search(
                        r'\s*[^.!?]*[.!?]', line, re.M | re.I)
                    if(isCompleteSentense):  # Sentence is complete
                        # Add to previous text(non complete sentence)
                        completeSentense = previousText + ' ' + line
                        willAddOriginalSentence = willAddOriginalSentence + \
                            ' '+completeSentense
                        previousText = ''
                        if(lineIndex == len(textList)-1):
                            length = len(sentence)-sentenceLen
                            if(length > 0):
                                previousText = sentence[sentenceLen:len(
                                    sentence)]
                        if(index == (len(lines)-1)):  # If this is the last subtitle add it to
                            tmpDic = {
                                "id": id,
                                "sentenceStartTime": sentenceStartTime,
                                "sentenceEndTime": sentenceEndTime,
                                "sentence": willAddOriginalSentence,
                                "sentenceTimeLen": sentenceTimeLen
                                }
                            sentences.append(tmpDic)
                            sentenceStartTime = ''
                            sentenceEndTime = ''
                            sentenceTimeLen = 0
                            willAddOriginalSentence = ''
                    else:  # If it's not a complete sentence add it to previous text
                        previousText = previousText+' '+sentence
            else:  # If it haven't a complete sentence add it to previous text
                previousText = previousText+' '+sentence
    return sentences
