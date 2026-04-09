# TCP Three-Way Handshake

**Built in:** [Week 8](../weeks/week-08-2026-02-23.md)
**Code:** [network/tcp/3_way_handshake.py](https://github.com/RGirish/monorepo/blob/main/network/tcp/3_way_handshake.py)

---

## What It Is

A simulation of the TCP three-way handshake — the process by which two hosts establish a TCP connection before any data is exchanged. The handshake ensures both parties are ready to communicate and agree on initial sequence numbers.

## The Protocol

The handshake involves three messages exchanged between a client and server:

```
Client                          Server
  |                                |
  |------- SYN (seq=x) ---------->|   Client initiates, picks ISN x
  |                                |
  |<------ SYN-ACK (seq=y, ack=x+1) --- Server picks ISN y, acknowledges x
  |                                |
  |------- ACK (ack=y+1) -------->|   Client acknowledges y
  |                                |
  |<====== Connection Established =====>|
```

### Step 1: SYN (Synchronize)
Client sends a SYN packet with a randomly chosen Initial Sequence Number (ISN). This asks the server to open a connection.

### Step 2: SYN-ACK (Synchronize-Acknowledge)
Server responds with a SYN-ACK: it acknowledges the client's ISN (ACK = client ISN + 1) and sends its own ISN. This confirms the server is listening and ready.

### Step 3: ACK (Acknowledge)
Client sends an ACK acknowledging the server's ISN. Both sides have now synchronized sequence numbers and the connection is established.

## Why Three Messages

Two messages would leave the server uncertain whether the client received the SYN-ACK. The third ACK confirms the bidirectional channel is working. (A two-way handshake would be sufficient for a unidirectional channel.)

## Implementation

The simulation models each host as a state machine with states: `CLOSED → SYN_SENT → ESTABLISHED` (client) and `LISTEN → SYN_RECEIVED → ESTABLISHED` (server). Messages are Python objects passed between state machine instances.

## Why This Matters

TCP connection establishment is a foundational networking concept. Understanding it is essential for debugging connectivity issues, understanding TLS (which runs on top of TCP), and grasping why TCP has higher latency than UDP for short-lived connections (3 round trips before data can flow).
