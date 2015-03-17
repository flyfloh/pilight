import socket
import sys
from thread import *
import RPi.GPIO as GPIO
import time

 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 5005 # Arbitrary non-privileged port

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        handle(data)
        reply = 'OK...' + data
        if not data:
            break
     
        conn.sendall(reply)
     
    #came out of loop
    conn.close()
 
def serve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'
     
    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error , msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
         
    print 'Socket bind complete'
     
    #Start listening on socket
    s.listen(10)
    print 'Socket now listening'
 
    #now keep talking with the client
    while 1:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
         
        #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        start_new_thread(clientthread ,(conn,))
     
    s.close()

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    
def handle(data):
    pins = []
    red = 18
    green = 23
    blue = 24

    GPIO.output(red, False)
    GPIO.output(green, False)
    GPIO.output(blue, False)

    if int(data[1:2]):
        pins.append(red)

    if int(data[3:4]):
        pins.append(green)

    if int(data[5:6]):
        pins.append(blue)
    
    for pin in pins:
        GPIO.output(pin, True)

init_gpio()
print 'Starting server at port ' + str(PORT)
serve()
GPIO.cleanup()
 
