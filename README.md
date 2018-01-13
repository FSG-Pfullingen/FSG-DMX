# FSG-DMX
 A System to control DMX Lights with a RaspberryPi made by the FSG-Pfullingen

## Usage:
All Words in [] are the parameters you have to give, all in {} are parameters you can give optionally
* set: ```url:5000/set?dmx=[DMX]&value=[VALUE]```
DMX is your DMX-Adress and VALUE is the value you want to set it to.
* get: ```url:5000/get?dmx=[DMX]```
DMX is your DMX-Adress.
* setup: ```url:5000/setup?dmx={STARTDMX}&type=[TYPE]&force={FORCE}```
STARTDMX is the DMX-Adress where your adress range for your light begins (if you don't pass it, the next free Adress range is used.), TYPE is the type of Lamp (if it is not in our library, just add it), which also sets up the names and numbers of channels used, and lastly FORCE is just if you want to override a fixture, thats already there.
* getfixture: ```url:5000/getfixture?dmx=[DMX]```
DMX is your DMX-Adress.
* store: ```url:5000/store?dmxes=[DMXLIST]&pos={POS}```
DMXLIST is the list of DMX-Adresses, you want to save (e.g. '1,2,3,4,5') and POS is the position you want to save it to, just parse this argument if you want to override a existing one.
* save: ```url:5000/save?filename={FILENAME}```
Save the DMX-Values and the channel names to a file with name FILENAME.json (the .json gets added automatically)
* load: ```url:5000/load?filename={FILENAME}```
Load the DMX-Values and the channel names from a file with the name FILENAME.json (the .json gets added automatically)

## Installation
### Requirements:
Add to  /etc/apt/sources.list
* Debian: ```deb   http://apt.openlighting.org/debian  squeeze main```
* Raspian: ```deb   http://apt.openlighting.org/raspbian  wheezy main```

Then Install:
```
apt-get update
apt-get install ola ola-python
```

Run our install script:
```
python install.py
```
in the main directory of our program (Cloned from GitHub).
### Program:
Clone from Github:
```
git clone https://github.com/FSG-Pfullingen/FSG-DMX.git
```
