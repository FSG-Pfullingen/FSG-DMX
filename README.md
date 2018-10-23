# FSG-DMX
A System to control DMX Lights with a Computer/Laptop/RaspberryPi and a USB to DMX converter made by the FSG-Pfullingen. Feel free to build your own application based on the Webhooks provided, for further features or if you found a bug, please open a issue.

## Quickstart:
Add to  /etc/apt/sources.list
* Debian: ```deb   http://apt.openlighting.org/debian  squeeze main```
* Raspian: ```deb   http://apt.openlighting.org/raspbian  wheezy main```

Then Install:
```
apt-get update
apt-get install ola ola-python
```
Clone from Github:
```
git clone https://github.com/FSG-Pfullingen/FSG-DMX.git
cd FSG-DMX
```
Install Python stuff:
```
python install.py
```
Start with
```
python main.py
```
Then navigate to ```[YOURIP]:5000/``` in your Browser

## HTML-Webhook Overview:
All Words in [] are the parameters you have to give, all in {} are parameters you can give optionally
* Main Page: ```url:5000/```
Displays just the Main Page with controls and everything
* set: ```url:5000/set?dmx=[DMX]&value={VALUE}&color={HEXCODE}```
DMX is your DMX-Adress and VALUE is the value you want to set it to. If you pass a color, you don't have to pass a value. The color is parsed in this Format #RRGGBB.
* get: ```url:5000/get```
Get the current state of the program (all values e.g. channels, adresses, states, all_lights).
* setup: ```url:5000/setup?dmx={STARTDMX}&type=[TYPE]&force={FORCE}```
STARTDMX is the DMX-Adress where your adress range for your light begins (if you pass -1, the next free Adress range is used.), TYPE is the type of Lamp (if it is not in our library, just add it), which also sets up the names and numbers of channels used, and lastly FORCE is just if you want to override a fixture, thats already there.
* new_light: ```url:5000/new_light?name=[NAME]&channels=[CHANNELS]```
NAME is the name of the Light and CHANNELS are the names of the channels (e.g. Brightness), the number of channels you give determines the number of channels set up.
* store_state: ```url:5000/store_state?dmxes=[DMXLIST]&pos={POS}```
DMXLIST is the list of DMX-Adresses, you want to save (e.g. '1,2,3,4,5') and POS is the position you want to save it to, just pass this argument if you want to override a existing one.
* delete_state: ```url:5000/delete_state?position=[POSITION]```
POSITION is the position in the List/Array of states.
Give this to delete the state.
* view_state: ```url:5000/view_state?position=[POS]```
Sets the dmx adresses to the corresponding values stores in the storage position POS
* save: ```url:5000/save?filename={FILENAME}```
Save the DMX-Values and the channel names to a file with name FILENAME.json (the .json gets added automatically) (default=book.json)
* load: ```url:5000/load?filename={FILENAME}```
Load the DMX-Values and the channel names from a file with the name FILENAME.json (the .json gets added automatically) (default=book.json)
