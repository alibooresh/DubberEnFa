import json
import os
a_file = open("data.json", "r")
json_object = json.load(a_file)
a_file.close()
name = "recording-0.wav"
sourceBin = json_object["sourceBin"]
source = {"id": 1, "src": str(name), "rect": [0, 0, 0, 0], "lastMod": "20220214T112013", "loudnessNormalization": True, "sourceTracks": [{"range": [0, 50000000], "type": 2, "editRate": 10000000, "trackRect": [
                                       0, 0, 0, 0], "sampleRate": 44100, "bitDepth": 32, "numChannels": 2, "integratedLUFS": -49.6945558155127, "peakLevel": 0.022308349609375, "metaData": ""}], "metadata": {"timeAdded": "20220214T113239.084520"}}
sourceBin = [source]
json_object["sourceBin"] = sourceBin
metadata = json_object["metadata"]
metadata["CanvasZoom"] = 100
json_object["metadata"] = metadata
print(json_object["timeline"]["sceneTrack"]
      ["scenes"][0]["csml"]["tracks"][0]["medias"])
a_file = open("data.json", "w")
json.dump(json_object, a_file)
a_file.close()


# Data to be written
# dictionary = {
#     "name": "sathiyajith",
#     "rollno": 56,
#     "cgpa": 8.6,
#     "phonenumber": "9976770500"
# }
# path = r"B:\Work\DU\dubassistant\Camtasia Project.tscproj"
#
# # Serializing json
# json_object = json.dumps(dictionary, indent=4)
# name = "sss.json"
# # Writing to sample.json
# with open(os.path.join(path, name), "w") as outfile:
#     outfile.write(json_object)
#
