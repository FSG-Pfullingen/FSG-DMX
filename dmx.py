import array
from ola.ClientWrapper import ClientWrapper

client = None
wrapper = None
universe = 1

def start():
    global client
    global wrapper
    wrapper = ClientWrapper()
    client = wrapper.Client()

def send(adresses):
    global client
    data = array.array('B', adresses)
    client.SendDmx(universe, data, DmxSent)
    wrapper.Run()

def DmxSent(state):
    global wrapper
    wrapper.Stop()
