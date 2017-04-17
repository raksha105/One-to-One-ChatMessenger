#!/usr/bin/env python

import socket
import os
import re
from threading import Thread
from SocketServer import ThreadingMixIn
import sys, select
import time


#Client threads to perform asynchronous communication. It creates threads, for each message recieved, and prints messages when recieved.
#initialization class for each thread
class ClientThread(Thread):
    def __init__(self, sc,username):
        Thread.__init__(self)
        self.sc = sc
        self.username = username
# Run method that handles sending and recieving messages to and from server.
    def run(self):
        header_message = "HTTP/1.0 \r\nContent-Type: text\n\n"
        while (1):
            #Recieve Message from server
            new_message = self.sc.recv(2048)

            #Check if connection is closed
            if " closed connection" in new_message:
                print "\n"+new_message
                os.execl(sys.executable, sys.executable, *sys.argv)


            all_message = new_message.split(",")
            print all_message[0]
            print all_message[1]
            # print "\n" + new_message
            chat_message = raw_input(username + ": ")
            localtime = time.asctime(time.localtime(time.time()))
#Sending message to server
            sc.send(header_message+","+"Date: "+localtime+","+chat_message+","+str(len(chat_message)))

# Client tries to establish a TCP socket connection

TCP_IP = '127.0.0.1'
TCP_PORT = 62
BUFFER_SIZE = 1024
# MESSAGE = "Hello, World! to server from client 1"
sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.connect((TCP_IP, TCP_PORT))
threads = []
header_message = "GET  HTTP/1.1\r\nContent-Type: text/plain"

username = raw_input("Please enter your username")

# Checking valid user name
while re.match("^[a-zA-Z0-9]+$", username) is None:
    print " Invalid username, enter a valid username"
    username = raw_input("Please enter your username")

chatname = raw_input("enter the name of the person you want to chat with")
#Sending user names to Server
sc.send(username + " " + chatname)

while (1):

    check_new = sc.recv(2048)
    if "is online" in check_new:
        print check_new
#New thread for handling messages
        while (1):
            newthread = ClientThread(sc,username)
            newthread.start()
            threads.append(newthread)
            chat_message = raw_input(username + ": ")
            localtime = time.asctime(time.localtime(time.time()))
#Sending message to Server
            sc.send(header_message+","+"Date: "+localtime+","+chat_message+","+"Content-Length: "+str(len(chat_message)))
    else:
        while(1):
            print check_new
            break







