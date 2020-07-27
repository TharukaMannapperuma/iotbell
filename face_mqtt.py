#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt # Import the MQTT library
import os
import face_recognition
import picamera
import numpy as np
import pyttsx3 #text to speech library
from datetime import datetime
import time
import ast

def text_to_speech(name,phase=150): 
    engine=pyttsx3.init()
    engine.setProperty('rate',phase)
    engine.say(name)
    engine.runAndWait()

def welcome_speech():
    now= datetime.now()
    dt_string=now.strftime("%H")
    hour=int(dt_string)
    if(hour<12):
        val='Good Morning. Please look at the camera'
    elif(12<= hour <=17):
        val = 'Good Afternoon. Please look at the camera'
    else:
        val='Good evening. Please look at the camera'
        
    engine=pyttsx3.init()
    engine.setProperty('rate',150)
    engine.say(val)
    engine.runAndWait()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("door_switch",2)
    client.subscribe("light_switch",2)
    client.subscribe("audiotext",2)

def on_message(client, userdata, msg):
    global door_state,light_state
    message_received=str(msg.payload)
    message_topic=msg.topic
    if (message_topic=="door_switch"):
        if ((message_received=="b'1'") and (door_state==0)):
            print("door opened")
            text_to_speech("Door opened",130)
            door_state=1
            GPIO.output(door_open, True)            
        elif(message_received=="b'0'" and door_state==1):
            print("door closed")
            door_state=0   
            GPIO.output(door_open, False)    

    elif(message_topic=="light_switch"):
        if ((message_received=="b'1'") and (light_state==0)):
            print("light on")
            light_state=1 
            GPIO.output(light_on, True)         
        elif((message_received=="b'0'") and (light_state==1)):
            print("light off")
            light_state=0
            GPIO.output(light_on, False)
        
    elif (message_topic=="audiotext"):
        payload = str(msg.payload)
        m_decode= payload[3:-2]
        m_decode = "{"+m_decode+"}"
        m_decode=ast.literal_eval(m_decode)
        print(m_decode['msg'])
        val = m_decode['msg']
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(val)
        engine.runAndWait()

def on_disconnect(client,userdata,rc):
    if rc != 0:
        print("Unexpected disconnection") 

#camera initializing
camera = picamera.PiCamera()
camera.resolution = (640, 480)
output = np.empty((480, 640, 3), dtype=np.uint8)
camera.rotation = 180

image_paths =[]
# Path for face image database
path = 'pictures'

for r,d,f in os.walk(path):
    for file in f:
        if '.jpg' in file:
            image_paths.append(os.path.join(r,file))


wait_led=10 #red LED
push_button=38 #buzzer connected
door_open=8 #yellow LED
light_on=40 #white LED 2

door_state=0 #open or close
light_state=0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(push_button, GPIO.IN) #Read output from push button
GPIO.setup(light_on, GPIO.OUT)  #LED output pin
GPIO.setup(door_open,GPIO.OUT)
GPIO.setup(wait_led,GPIO.OUT)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message    

client.connect("broker.hivemq.com", 1883, 120)
client.loop_start()

is_no_visitor=0
stranger_exception=0
text_to_speech("Initializing completed") # text to speech

while True:
    i=GPIO.input(push_button)
    
    time.sleep(1)
    print(i)

    if (i==0 and is_no_visitor==0) :#When input from push button is LOW
        print ("No visitors")
        client.publish("visitor_status",payload=0)
        GPIO.output(light_on, 0)  #Turn OFF LED
        is_no_visitor=1
        
    elif i==1:#When input from push button is HIGH
        GPIO.output(wait_led,1) #red led, show the precessing
        GPIO.output(light_on, 1)  #Turn ON LED, flasher for the camera
        light_state=1
        
        welcome_speech()#sound
        print ("Visitor detected")
        time.sleep(1)
        
        is_no_visitor=0
        
        client.publish("visitor_status",payload=1)
        
        camera.capture('unknown.jpg',quality=15) #two photos are taken. can improve!!!
        
        results=["results of face matchings"]
        results[0]=False 

        try:
            camera.capture(output, format="rgb")
            GPIO.output(wait_led,0)
            face_locations = face_recognition.face_locations(output)
            print("Found {} faces in image.".format(len(face_locations)))
            GPIO.output(wait_led,1)
            unknown_face_encoding = face_recognition.face_encodings(output, face_locations)[0] #only first image is considered here. peocessing power is not enough to process two images

            for count,pic_path in enumerate(image_paths):  
                picture_of_me = face_recognition.load_image_file(pic_path)
                face_locations = face_recognition.face_locations(picture_of_me)
                my_face_encoding = face_recognition.face_encodings(picture_of_me,face_locations)[0]

                results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding,tolerance=0.5)
                stranger_exception=1
                if results[0] == True:
                    name = image_paths[count].split("/")[1]
                    print(name)
                    client.publish("notification_name",name,0)
                    text_to_speech("Hi! {}".format(name[2:]))
                    
                    break
                   
        except IndexError:
            print ("Face is not clear")
            text_to_speech("Please press the bell again.",140)
            stranger_exception=0
        
        f=open("unknown.jpg", "rb")
        fileContent = f.read()
        byteArr = bytes(fileContent)
        client.publish("timage",byteArr,0)
        time.sleep(2)
        print("Image Upload Successfully")
        if results[0]==True:
            client.publish("namemy",name,0)
        elif stranger_exception ==1:
            print("stranger")
            client.publish("namemy","stranger",0)
            text_to_speech("Please wait",130)
            
        GPIO.output(wait_led,0) #red led
        light_state=0
        