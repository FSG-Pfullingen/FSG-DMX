from flask import Flask
from flask import request, render_template
import numpy as np

main_book = dict()
all_lights = {"Lamp":[["Brigthness"], []], "JBLED-A7":[["Brigthness", "Shutter", "R", "G", "B"], []]}

app = Flask(__name__)

@app.route("/")
def main():
    return "Running go localhost:5000/set?dmx=23&value=255 to turn light 23 to full brigthness"

@app.route("/set")
def set():
    """
    Set a DMX-Adress to a specified value
    """
    dmx = getdmx()
    value = request.args.get('value')
    if not  0 < int(value) < 255:
        return "Invalid Value"
    main_book[dmx] = value
    return "Worked!"

@app.route("/get")
def get():
    dmx = getdmx()
    if dmx in main_book:
        return main_book[dmx]
    else:
        return "Unused DMX"

def get_type():
    dmx = getdmx()

@app.route("/setup")
def setup():
    dmx = getdmx()
    typus = request.args.get('type', default="Lamp")
    channels = request.args.get('channels', default="1")
    if typus in all_lights:
        channels = len(all_lights[typus][1])
    for channel in range(int(channels)):
        main_book[str(int(dmx)+channel)] = 0
    return "Setup done: dmx=" + str(dmx) + " type=" + typus + " num of channels:" + str(channels)

@app.route("/save")
def save():
    filename = request.args.get("filename", default="book")
    try:
        np.save(filename + '.npy', main_book)
    except:
        return "ERROR!"
    else:
        return "Saved!"

@app.route("/load")
def load():
    filename = request.args.get("filename", default="book")
    main_book = np.load(filename + '.npy').item()
    return str(main_book)


def getdmx():
    dmx = request.args.get('dmx')
    if not 0 < int(dmx) < 512:
        return "Invalid DMX"
    else:
        return dmx

app.run()
