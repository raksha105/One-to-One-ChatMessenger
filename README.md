Instant messaging system consisting of server and client processes.
 
Each client process will connect to the server over a socket connection and register a user name at the server. After registering, a client program can request to be connected to another registered client by giving a registered user name.
 
The user is expected to know the names of the users she wants to talk to. When one registered client requests to be connected to another, a logical connection will be made inside the server. From that point, any messages typed at one client will be sent to the server which will relay it to the other connected client. The operation is similar for any number of messaging clients.

If one client of a connected set logs off, dies or becomes disconnected the other client is notified. Once a client is connected to another client then neither can make another connection until they disconnect or logoff. The server should displays the messages that come through each client.
