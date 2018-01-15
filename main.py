from flask import Flask
from flask import request, render_template, redirect
import json
import dmx as dmxsender

#Setup empty lists
adresses = [0] * 513
channels = [''] * 513
#Get all usable Lights
with open('data/lights.json', 'r') as f:
    all_lights = json.loads(f.read())

#Setup Flask
app = Flask(__name__)


#--------------------------------Webservice--------------------
@app.route("/")
def main():
    """
    Just some info Page
    """
    with open('data/states.json', 'r') as f:
        states = json.loads(f.read())
    return render_template('index2.html', options=all_lights.keys(), states=states)

@app.route("/test")
def test():
    """
    Just the Test Page
    """
    with open('data/states.json', 'r') as f:
        states = json.loads(f.read())
    return render_template('index.html', options=all_lights.keys(), states=states)

@app.route("/set")
def set():
    """
    Set a DMX-Adress to a specified value
    """
    #Get values
    dmx = getdmx(request)
    value = int(request.args.get('value'))
    color = request.args.get('color', default="#000000").strip("#")
    #Check if in usable range
    if not  0 <= value <= 255:
        return "Invalid Value"
    #Dismantle colors
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:7], 16)
    c,m,y,k = rgb_to_cmyk(r, g, b)
    #Put value in  list
    adresses[dmx] = value
    dmxsender.send(adresses)
    #Return Debug information
    return redirect("http://localhost:5000/", code=302)
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
    dmx = int(request.args.get('dmx', default="-1"))
    typus = request.args.get('type')
    force = bool(request.args.get('force', default=0))
    #See if the type of light already exists
    if typus in all_lights:
        num = len(all_lights[typus])
        attr = all_lights[typus]
    else:
        return "Light not in Database"
    if dmx == -1:
        counter = 0
        glob_count = 0
        for item in channels:
            print str(counter) + ":" + str(glob_count)
            if item == '':
                counter += 1
            else:
                counter = 0
            if counter == num:
                dmx = (glob_count - counter)+1
                print "Now on Adress: " + str(dmx)
                break
            glob_count += 1
    #Do you want to override existing settings?
    elif not force:
        for i in range(dmx, (dmx+num)):
            if not channels[i] == '':
                return "Channels already in use, force with parameter force=1"
                break
    #Setup the name channels
    for i in range(num):
        channels[dmx + i] = (str(typus) + " | " + attr[i])
        print str(dmx+i) + str(channels[dmx+i])
    return redirect("http://localhost:5000/", code=302)
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
    with open('data/states.json', 'r') as f:
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
    with open('data/states.json', 'w') as f:
        f.write(json.dumps(states))
    return redirect("http://localhost:5000/", code=302)
    return "SAVED:" + str(pos)

@app.route("/view_state")
def view_state():
    """
    View a state previously saved
    """
    global adresses
    pos = int(request.args.get("position", default=-1))
    with open('data/states.json', 'r') as f:
        states = json.loads(f.read())
    if not pos == -1 and pos < len(states):
        for adress in states[pos].keys():
            if not adress == "name":
                print str(adress) + ":" + str(states[pos][adress])
                adresses[int(adress)] = states[pos][adress]
        dmxsender.send(adresses)
        return redirect("http://localhost:5000/", code=302)
        return "LOADED"
    return "INVALID KEY"

@app.route("/get_state_names")
def get_state_names():
    """
    Get names of all stored states
    """
    with open('data/states.json', 'r') as f:
        states = json.loads(f.read())
    state_list = []
    for state in states:
        print state
        state_list.append(str(state["name"]) + ":" + str(states.index(state)))
    return str(state_list)


@app.route("/save")
def save():
    """
    Save current setup to file (default both values and names)
    """
    filename = request.args.get("filename", default="book")
    with open('data/' + filename + '.json', 'w') as f:
        f.write(json.dumps([adresses, channels]))
        return redirect("http://localhost:5000/", code=302)
        return "SAVED"

@app.route("/load")
def load():
    """
    Load the saved values and names from file
    """
    global adresses
    filename = request.args.get("filename", default="book")
    with open('data/' + filename + '.json', 'r') as f:
        adresses, channels = json.loads(f.read())
    return redirect("http://localhost:5000/", code=302)
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

def rgb_to_cmyk(r,g,b):
    cmyk_scale = 100
    if (r == 0) and (g == 0) and (b == 0):
        # black
        return 0, 0, 0, cmyk_scale

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / 255.
    m = 1 - g / 255.
    y = 1 - b / 255.

    # extract out k [0,1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    # rescale to the range [0,cmyk_scale]
    return c*cmyk_scale, m*cmyk_scale, y*cmyk_scale, k*cmyk_scale

#Run!
if __name__ == '__main__':
    """
    Run the Webserver
    """
    dmxsender.start()
    app.run()
