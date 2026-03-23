"""
WebSocket server for the collaborative CRDT editor.

- First browser tab to connect becomes "alice"
- Second becomes "bob"
- Each tab's edits are applied to that user's CRDT replica and synced to the other
- Supports going offline/online via a button in the UI
"""

import asyncio
import json
import websockets
from crdt import Document, Network

net = Network()
alice = Document(machine_id="alice", network=net)
bob   = Document(machine_id="bob",   network=net)
net.subscribe(alice)
net.subscribe(bob)

docs     = {"alice": alice, "bob": bob}
offline  = set()                        # users currently offline
sockets  = {}                           # user -> websocket


async def broadcast():
    """Send each connected client their own document's current text."""
    for user, ws in list(sockets.items()):
        try:
            await ws.send(json.dumps({
                "user":    user,
                "text":    docs[user].text(),
                "offline": user in offline,
                "peers":   {u: docs[u].text() for u in docs if u != user},
            }))
        except websockets.ConnectionClosed:
            pass


async def handler(ws):
    # assign a slot
    if "alice" not in sockets:
        user = "alice"
    elif "bob" not in sockets:
        user = "bob"
    else:
        await ws.send(json.dumps({"error": "only 2 users supported"}))
        return

    sockets[user] = ws
    print(f"{user} connected")

    # send initial state
    await broadcast()

    try:
        async for raw in ws:
            msg = json.loads(raw)
            kind = msg["type"]

            if kind == "insert":
                docs[user].insert_at(msg["pos"], msg["char"])

            elif kind == "delete":
                docs[user].delete_at(msg["pos"])

            elif kind == "offline":
                if user not in offline:
                    net.go_offline(docs[user])
                    offline.add(user)

            elif kind == "online":
                if user in offline:
                    net.go_online(docs[user])
                    offline.discard(user)

            await broadcast()

    except websockets.ConnectionClosed:
        pass
    finally:
        print(f"{user} disconnected")
        del sockets[user]


async def main():
    print("server running on ws://localhost:8765")
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
