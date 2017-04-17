import socket
from threading import Thread
from SocketServer import ThreadingMixIn
import sys, select
import time
all_users = []

sock_connections = {}

# Dictionary to store client connections
user_busy ={}
#Dictionary of busy flags


#thread initialization class for each client that needs to connect to server
#Initializes dictionary of users and connections
class ClientThread(Thread):
    def __init__(self, ip, port,users):
        Thread.__init__(self)
        # ip and port of established client
        self.ip = ip
        self.port = port
        self.users = users

        #print users
        all_users = users.split(" ")
        sock_connections[all_users[0]] = conn
        user_busy[all_users[0]] = 0
        print user_busy

        self.all_users = all_users
        self.sock_connections = sock_connections
        self.user_busy = user_busy
        print self.all_users[0]+" is connected on ip "+str(self.ip)+" and port "+str(self.port)


#Run class of server thread for each client to pass messages between two clients

    def run(self):
        while(1):
            try:
                #print self.all_users
                if self.all_users[1] in self.sock_connections:
                    print self.user_busy[self.all_users[1]]
                    # Busy Check
                    if self.user_busy[self.all_users[1]] == 0:

#Checking if user is online

                        self.sock_connections[self.all_users[0]].send(self.all_users[1]+" is online")
                        self.user_busy[self.all_users[1]] = 1


                        while(1):
                            print "receiving from "+self.all_users[0]
                            #Recieve message from client1
                            chatstr = self.sock_connections[self.all_users[0]].recv(2048)
                            #print chatstr
                            header_message = chatstr.split(",")
                            print header_message[0]
                            print header_message[1]
                            print header_message[3]
                            print header_message[2]
                            if header_message[2] == "q":
                                self.sock_connections[self.all_users[0]].send("You closed connection")
                                self.sock_connections[self.all_users[1]].send(self.all_users[0]+" closed connection")

                                self.sock_connections[self.all_users[0]].close()
                                break
                            localtime = time.asctime(time.localtime(time.time()))
#Send message to Client2
                            self.sock_connections[self.all_users[1]].send(self.all_users[0]+": "+header_message[2]+","+"Date: "+localtime)

                    else:
                        print "busy"
                        self.sock_connections[self.all_users[0]].send(self.all_users[1]+" is busy")


                else:
                    print "sending not online to "+ self.all_users[0]
                    self.sock_connections[self.all_users[0]].send(self.all_users[1] + " is not online")
            except socket.error:
                print " Client aborted connection"
                break
# Establish TCP Socket for server, and accept multiple client connections in the while loop

TCP_IP = '127.0.0.1'
TCP_PORT = 62
BUFFER_SIZE = 1024

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    #Accept multiple client connections

    try:
        tcpsock.listen(4)
        print "Waiting for incoming connections..."
        (conn, (ip, port)) = tcpsock.accept()
        users = conn.recv(2048)
        print users
        #New thread to handle messages
        newthread = ClientThread(ip, port,users)
        newthread.start()
        threads.append(newthread)
    except socket.error:
        print " Client aborted connection"
        conn.close()


for t in threads:
    t.join()