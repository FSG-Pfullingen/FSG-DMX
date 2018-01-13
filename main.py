from flask import Flask
from flask import request
import json
import dmx

#Setup empty lists
adresses = [0] * 513
channels = [''] * 513
#Get all usable Lights
with open('lights.json', 'r') as f:
    all_lights = json.loads(f.read())
print all_lights

#Setup Flask
app = Flask(__name__)


#--------------------------------Webservice--------------------
@app.route("/")
def main():
    """
    Just some info Page
    """
    return "Running go localhost:5000/set?dmx=23&value=255 to turn light 23 to full brigthness"

@app.route("/set")
def set():
    """
    Set a DMX-Adress to a specified value
    """
    #Get values
    dmx = getdmx(request)
    value = int(request.args.get('value'))
    #Check if in usable range
    if not  0 <= value <= 255:
        return "Invalid Value"
    #Put value in  list
    adresses[dmx] = value
    dmx.send(adresses)
    #Return Debug information
    return "SET:" + str(dmx) + ":" + str(value)

@app.route("/get")
def get():
    """
    Get the currently stored value for that DMX-Adress
    """
    #Get DMX-Adress
    dmx = getdmx(request)
    #Return the corresponding value
    return "GET:" + str(dmx) + ":" + str(adresses[dmx])

@app.route("/setup")
def setup():
    """
    Put a name on the corresponding
    DMX-Adresses
    """
    global channels
    #Get all necessary values
    dmx = getdmx(request)
    typus = request.args.get('type')
    num = request.args.get('channels')
    force = bool(request.args.get('force', default=0))
    #See if the type of light already exists
    if typus in all_lights:
        num = len(all_lights[typus])
        attr = all_lights[typus]
    else:
        attr = num * ['']
    #Do you want to override existing settings?
    if not force:
        for i in range(dmx, (dmx+num)):
            if not channels[i] == '':
                return "Channels already in use, force with parameter force=1"
                break
    #Setup the name channels
    for i in range(num):
        channels[dmx + i] = (str(typus) + " | " + attr[i])
        print str(dmx+i) + str(channels[dmx+i])
    return str(channels)

@app.route("/getfixture")
def getfixture():
    """
    Get the name of the Fixture on that DMX-Adress
    """
    dmx = getdmx(request)
    return channels[dmx]

@app.route("/store_state")
def store_state():
    """
    Store the current values for later use
    """
    dmxes = request.args.get("dmxes").split(",")
    pos = int(request.args.get("position", default=-1))
    name = request.args.get("name", default='')
    with open('states.json', 'r') as f:
        states = json.loads(f.read())
    savestate = {"name":name}
    for dmx in dmxes:
        savestate[dmx] = adresses[int(dmx)]
    print str(len(states)) + ":" + str(pos)
    if pos >= 0 and pos < len(states):
        states[pos] = savestate
    else:
        states.append(savestate)
        pos = len(states)-1
    with open('states.json', 'w') as f:
        f.write(json.dumps(states))
    return "SAVED:" + str(pos)

@app.route("/view_state")
def view_state():
    """
    View a state previously saved
    """
    global adresses
    pos = int(request.args.get("position", default=-1))
    with open('states.json', 'r') as f:
        states = json.loads(f.read())
    if not pos == -1 and pos < len(states):
        for adress in states[pos].keys():
            if not adress == "name":
                print str(adress) + ":" + str(states[pos][adress])
                adresses[int(adress)] = states[pos][adress]
        dmx.send(adresses)
        return "LOADED"
    return "INVALID KEY"

def get_state_names():
    """
    Get names of all stored states
    """
    with open('states.json', 'r') as f:
        states = json.loads(f.read())
    for state in states:
        state["name"]


@app.route("/save")
def save():
    """
    Save current setup to file (default both values and names)
    """
    filename = request.args.get("filename", default="book")
    with open(filename + '.json', 'w') as f:
        f.write(json.dumps([adresses, channels]))
        return "SAVED"

@app.route("/load")
def load():
    """
    Load the saved values and names from file
    """
    global adresses
    filename = request.args.get("filename", default="book")
    with open(filename + '.json', 'r') as f:
        adresses, channels = json.loads(f.read())
    return str(adresses) + str(channels)

# --------------------------------Functions---------------------------------
def getdmx(request):
    """
    Get and validate the dmx adress
    """
    dmx = request.args.get('dmx')
    if not 0 <= int(dmx) <= 512:
        return "Invalid DMX"
    else:
        return int(dmx)

#Run!
if __name__ == '__main__':
    """
    Run the Webserver
    """
    dmx.start()
    app.run()
