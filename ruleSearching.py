import zmq
import requests
import json

"""
Expected input format: jsonified dictionary (let "" represent a null (empty) string)
input_dict = {
    "option": [value is 1, 2, or 3],
    "searchTerm": [value is a string, cannot be ""],
    "category" [value is "" for option 1 or 3, but string value is required for 2.]
}
"""

def main():
    # set up ZeroMQ
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    # Binds REP socket to tcp://*:5555
    socket.bind("tcp://localhost:5555")

    # Wait for next request from client
    message = socket.recv()
    print(f"Received request: {message}")

    # convert byte string message to json
    decoded = json.loads(message.decode('utf-8'))
    print(f"Decoded request: {decoded}")

    # send response to client
    socket.send(message)


# Search rules by keyword
def findKeyword():
    print("1")

# search for spells/abilities by name
def findSpellsAbilities():
    print("2")

# search for game mechanics by keyword
def findMechanics():
    print("3")


if __name__ == "__main__":
    main()



"""
Receiver.py
#   Binds REP socket to tcp://*:5555
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


#  Wait for next request from client
message = socket.recv()
print(f"Received request: {message}")

socket.send(message)
"""

