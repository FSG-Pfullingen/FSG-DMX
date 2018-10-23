from flask import Flask
from flask import request, render_template, session, redirect, url_for, Response
import json
import dmx as dmxsender

#Setup empty lists
adresses = [0] * 513
channels = [''] * 513
states = []
#Get all usable Lights
with open('data/lights.json', 'r') as f:
    all_lights = json.loads(f.read())

#Setup Flask
app = Flask(__name__)
#--------------------------------Webservice--------------------
@app.route("/index")
@app.route("/")
def index():
    """
    Just some info Page
    """
    global states
    with open('data/states.json', 'r') as f:
        states = json.loads(f.read())
    # COLORS: https://www.w3schools.com/w3css/w3css_colors.asp
    return render_template('UI.html', main_color="orange", adresses=map(str, adresses), channels=channels, options=all_lights.keys(), states=states)

@app.route("/set")
def set():
    """
    Set a DMX-Adress to a specified value
    """
    #Get values
    dmx = int(request.args.get('dmx'))
    value = int(request.args.get('value', default="-1"))
    color = request.args.get('color', default="#000000").strip("#")
    #Check if in usable range
    #Dismantle colors
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:7], 16)
    c,m,y,k = rgb_to_cmyk(r, g, b)
    fixture = channels[dmx].split(" | ")[0]
    print fixture
    """
    max_count = len(all_lights[fixture])
    print max_count
    """
    prev_fix = fixture
    if r+g+b != 0:
        count = -1
        while(True):
            if count >= 512:
                break
            count += 1
            if channels[count] == "":
                continue
            fixture = channels[count].split(" | ")[0]
            if fixture != prev_fix:
                continue
            name = channels[count].split(" | ")[1]
            print name
            if name == "R":
                adresses[count] = r
            if name == "G":
                adresses[count] = g
            if name == "B":
                adresses[count] = b
            if name == "C":
                adresses[count] = c
            if name == "M":
                adresses[count] = m
            if name == "Y":
                adresses[count] = y
            if name == "K":
                adresses[count] = k
    else:
        if not  0 <= value <= 255:
            return "Invalid Value"
        adresses[dmx] = value
    dmxsender.send(adresses)
    #Return Debug information
    return json_back()

@app.route("/get")
def get():
    """
    Get the current state of the program
    """
    #Return the corresponding value
    return json_back()

@app.route("/new_light")
def new_light():
    """
    Put a new light in the Library
    """
    name = request.args.get('name')
    types = request.args.get('channels').split(",")
    all_lights[name] = types
    print name, all_lights[name]
    with open('data/lights.json', 'w') as f:
        f.write(json.dumps(all_lights))
        return json_back()
    return "ERROR"

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
    custom_name = request.args.get('name', default="")
    force = bool(request.args.get('force', default=0))
    #See if the type of light already exists
    if typus in all_lights:
        num = len(all_lights[typus])
        attr = all_lights[typus]
    else:
        return "Light not in Database"

    if not force:
        for i in range(dmx, (dmx+num)):
            if not channels[i] == '':
                return "Channels already in use, force with parameter force=1"
                break

    if custom_name == "":
        custom_name = typus + str(dmx)
    #Setup the name channels
    for i in range(num):
        channels[dmx + i] = (str(custom_name) + " | " + attr[i])
        print str(dmx+i) + str(channels[dmx+i])
    return json_back()

@app.route("/store_state")
def store_state():
    """
    Store the current values for later use
    """
    global states
    dmxes = request.args.get("dmxes").split(",")
    pos = int(request.args.get("position", default=-1))
    name = request.args.get("name", default='')
    with open('data/states.json', 'r') as f:
        states = json.loads(f.read())
    savestate = {"name":name}
    for dmx in dmxes:
        if "-" in dmx:
            print dmx
            fromto = dmx.split("-")
            for addr in range(int(fromto[0]), int(fromto[1])+1):
                print addr
                savestate[addr] = adresses[int(addr)]
        else:
            savestate[dmx] = adresses[int(dmx)]
    print str(len(states)) + ":" + str(pos)
    if pos >= 0 and pos < len(states):
        states[pos] = savestate
    else:
        states.append(savestate)
        pos = len(states)-1
    with open('data/states.json', 'w') as f:
        f.write(json.dumps(states))
    return json_back()

@app.route("/delete_state")
def delete_state():
    global states
    pos = request.args.get("position")
    print "deleting" + pos
    with open('data/states.json', 'r') as f:
        states = json.loads(f.read())
    print states[int(pos)]
    del states[int(pos)]
    with open('data/states.json', 'w') as f:
        f.write(json.dumps(states))
    return json_back()

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
        print "Pos valid"
        for adress in states[pos].keys():
            if not adress == "name":
                print str(adress) + ":" + str(states[pos][adress])
                adresses[int(adress)] = states[pos][adress]
            else:
                print "Property Name"
        dmxsender.send(adresses)
        return json_back()
    return "INVALID KEY"

@app.route("/save")
def save():
    """
    Save current setup to file (default both values and names)
    """
    filename = request.args.get("filename", default="book")
    if '.json' not in filename:
        filename += ".json"
    with open('data/' + filename, 'w') as f:
        f.write(json.dumps(channels))
        return json_back()
    return "ERROR"

@app.route("/load")
def load():
    """
    Load the saved values and names from file
    """
    global channels
    filename = request.args.get("filename", default="book")
    if '.json' not in filename:
        filename += ".json"
    with open('data/' + filename, 'r') as f:
        count = 0
        for channel in json.loads(f.read()):
            if not channel == "":
                print channel
                channels[count] = channel
            count += 1
        return json_back()
    return "ERROR"

@app.route("/channels")
def view_channels():
    return json.dumps(channels)

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

def json_back():
	return Response(json.dumps([channels, adresses, all_lights.keys(), states], separators=(',',':')), mimetype="application/json")

#Run!
if __name__ == '__main__':
    """
    Run the Webserver
    """
    dmxsender.start()
    app.run(host="0.0.0.0", port=5000)
