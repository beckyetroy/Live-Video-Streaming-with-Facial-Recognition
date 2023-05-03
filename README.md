# Live-Video-Streaming-with-Facial-Recognition
This repository holds a Live Video Streaming Service with Facial Recognition as part of CA3 in module Distributed Systems.

The application, written in Python, is designed to recognise faces in the user’s camera video feed and stream it to a Real-Time Messaging Protocol (RTMP) server, where multiple clients can connect to the server and view the video feed.

The following instructions are tailored to Windows 11 Users and may need to be adjusted for other operating systems.

## Technologies
The application uses the following technologies:
- Flask / Flask-SocketIO
- OpenCV
- Face Recognition
- NumPY
- FFmpeg
- Nginx with RTMP module

## Prerequisites
To run the application, the user must have the following pre-installed on their system:
- Python
- Visual Studio / CMake
- Pip
- FFmpeg pre-compiled
- Nginx pre-compiled with RTMP module

### Installing dependencies
To install the required dependencies for the application, run the following command from the project directory:
```
pip install -r requirements.txt
```

## Launching the Application
To start the application and begin hosting the live stream, run the following command from the project directory:
```
python ./app.py
```

The application will then launch on port 5000 of your local IP address or localhost.

## Connecting to the Livestream
To view the livestream, clients can connect using the URL:
**rtmp://[host ip address]:1935/live/stream**

For the live stream to work, the client must be connected to the same network as the host system.
As well as this, the client must connect to the live stream using a player that supports the rendering of x264 media,
such as the VLC Player.

## Application Screenshots
### Live-streaming:
![System Screenshot1](https://user-images.githubusercontent.com/58404970/235916978-6008901f-efde-4dd0-a0f4-816ba33d20e8.png)

### Facial Recognition:
![System Screenshot2](https://user-images.githubusercontent.com/58404970/235917024-1d4875f9-b010-4705-8eea-c31c8e0fdb1d.png)
