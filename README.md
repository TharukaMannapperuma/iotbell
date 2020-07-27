# IoT Bell
## IoT Smart Door Bell
- This Project was done using Raspberry Pi and Pi Camera with various libraries like face_recognition, paho mqtt and etc. Main focus of this project wes to create a door bell with face recognition and voice output which user can give command and it will convert into voice.

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
