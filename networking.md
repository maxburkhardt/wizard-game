# Wizard Game Networking Specification

## High level overview
Each client holds two socket connections open to the server:

* STOC
    * Server-to-client
    * Client blocks on recv() calls, puts received data in a synchronized queue
* CTOS
    * Client-to-server
    * Client periodically checks its send queue and then sends the data to the server
   
Each of these sockets is managed by a separate thread that reads/writes from the appropriate queues.

## Wire format
In general commands follow this syntax:

```
VERB OBJECT
```

The wire format is designed to be simple and easily parseable. For instance, most commands can be parsed
simply by splitting on " ".

## Command specification
### Send (CTOS)
```
SEND UUID
```

Register this client and establish this connection as a CTOS socket.
### Receive (CTOS)
```
RECV UUID
```

Register this client and establish this connection as a STOC socket.
### Ready (STOC)
```
READY
```

This message is sent from the server to the clients when all clients have joined and the game may start.
### New (STOC)
```
NEW SIGIL-OBJECT
```

A new unclaimed sigil is available. 
### Claim (CTOS)
```
CLAIM SIGIL-UUID
```

The client wishes to grab the sigil specified by `SIGIL-UUID`. 
### Claimed (CTOS)
```
CLAIMED PLAYER-UUID SIGIL-UUID
```

The client wishes to grab the sigil specified by `SIGIL-UUID`. 
### Cast (CTOS)
```
CAST SIGIL-UUID [SIGIL-UUID...]
```

The client wishes to cast this sigil (or combo of sigils).
### Cast Complete (STOC)
```
COMPLETE SIGIL-UUID [SIGIL-UUID...] PLAYER-UUID
```

The specified sigil or combo of sigils has completed its cast. _TODO: who cast it?_
### Health Update (STOC)
```
HEALTH PLAYER-UUID NEW-HEALTH
```

The player with the UUID specified now has health `NEW-HEALTH`.
### Game Over (STOC)
```
VICTOR PLAYER-UUID
```

The player with the specified UUID wins.