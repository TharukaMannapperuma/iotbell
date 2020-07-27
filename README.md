# IoT Bell <img alt="GitHub release (latest by date including pre-releases)" src="https://img.shields.io/github/v/release/tharukamannapperuma/iotbell?include_prereleases"> <img alt="GitHub All Releases" src="https://img.shields.io/github/downloads/tharukamannapperuma/iotbell/total?color=green"> <img alt="GitHub" src="https://img.shields.io/github/license/tharukamannapperuma/iotbell">

## IoT Smart Door Bell

- This Project was done using Raspberry Pi and Pi Camera with various libraries like face_recognition, paho mqtt and etc. Main focus of this project wes to create a door bell with face recognition and voice output which user can give command and it will convert into voice. Raspbian Lite was used with SSH access for configuration purposes

## Features

1.  Face Recognition
2.  Auto Door unlock / lock
3.  Remote Door unlock / lock
4.  Owner can see the visitor
5.  Owner can give voice commands to the visitor
6.  Owner can add users for face recognition

## Feature Implimentation

### Face Recognition

- Using <a href = "https://github.com/ageitgey/face_recognition">this</a> face recognition library which was developed by Adam Geitgey (aka <a href = "https://github.com/ageitgey">ageitgey</a>). This is avery simple library yet powerful. Documentation can be found in his repo. We can do face recognition while code is running but it is slow since we run on a raspberry pi. we can train face modals and we can save them as a pickle file to improve speed since training part was already done.

### Text to Speech

- Using pyttsx3 python library we can convert text messages which user send to the raspberry into a voice. more information can be found <a href="https://pypi.org/project/pyttsx3/">here</a>

### Raspberry Pi Camera

- Using <a href="https://pypi.org/project/picamera/">this</a> library we can attach raspberry pi camera to capture video and stills. Dcoumentation can be found in mentioned link

### MQTT Communication

- Using <a href="https://pypi.org/project/paho-mqtt/">this</a> library we can do MQTT communications with the MQTT server of our choice.

### GPIO of Raspberry Pi

- Using <a href="https://pypi.org/project/RPi.GPIO/">this</a> library we can control GPIO pins of the raspberry pi.
