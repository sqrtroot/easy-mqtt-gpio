import toml
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

#load the config
config = toml.load("config.txt")

#Subscribe on connecting
def on_connect(client, userdata, flags, rc):
    print("Connected")
    client.subscribe(list(map(lambda x: (x,2), config['gpio']['pins'].values())))

#Set pins on and of based on channel and message
def handle_message(client, userdata, msg):
    pins = [x for x,y in config["gpio"]["pins"].items() if y == msg.topic] 
    print("Pins", pins)
    for pin in pins:
        GPIO.output(pin, GPIO.HIGH if int(msg.payload) == 1 else GPIO.LOW)



#Setup gpio
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Set pins to output
for pin in config["gpio"]["pins"].keys():
        GPIO.setup(pin, GPIO.OUT)

#Create mqtt client     
client = mqtt.Client()
#Set event handlers
client.on_connect = on_connect
client.on_message = handle_message

#Connect to server
client.connect(
        config['mqtt']['server']['ip'],
        int(config['mqtt']['server']['port']),
        60)

#Run everything
client.loop_forever()
