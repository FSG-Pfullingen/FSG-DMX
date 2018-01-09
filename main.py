from flask import Flask
from flask import request, render_template

main_book = dict()
all_lights = {"Lamp":[1], "JBLED-A7":[12]}

app = Flask(__name__)

@app.route("/")
def main():
    return "Running go localhost:5000/set?dmx=23&value=255 to turn light 23 to full brigthness"

@app.route("/set")
def set():
    """
    Set a DMX-Adress to a specified value
    """
    dmx = request.args.get('dmx')
    value = request.args.get('value')
    if dmx > 512 or value > 255 or dmx < 0 or value < 0:
        return "Invalid Parameters"
    light = main_book[dmx]
    light[1] = value
    main_book[dmx] = light
    return "ARGS:" + str(main_book)

@app.route("/get")
def get():
    dmx = request.args.get('dmx')
    if dmx in main_book:
        return main_book[dmx]
    else:
        return "Unused DMX"

@app.route("/setup")
def setup():
    dmx = request.args.get('dmx')
    typus = request.args.get('type', default="Lamp")
    channels = request.args.get('channels', default=1)
    if typus in all_lights:
        channels, = all_lights[typus]

@app.route("/save")
def save():
    filename = request.args.get("filename")
    with open(filename, "w") as f:
        f.write(str(main_book))

@app.route("/load")
def load():
    filename = request.args.get("filename")
    with open(filename, "r") as f:
        main_book = eval(f.read()) #DANGER! could be abused, because python is executing all code in that file. DANGER!

app.run()
