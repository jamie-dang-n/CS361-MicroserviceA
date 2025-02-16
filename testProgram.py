import zmq
import json

def main():
    # set up dictionary
    dict = {
        "option":1,
        "searchTerm":"yes",
        "category":""
    }

    # jsonify the dictionary -- can only send a string
    jsonInput = json.dumps(dict, default=str)

    # set up ZeroMQ
    context = zmq.Context()
    print("Connecting to server…")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # send request
    print(f"Request sent: {jsonInput}")
    socket.send_string(jsonInput)

    # get the response
    message = socket.recv()
    print(f"Response sent back: {message}")

if __name__ == "__main__":
    main()

"""
Sender.py
#   Connects REQ socket to tcp://localhost:5555
import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  send request
socket.send(b"This is a messsage from CS361")

# get the response
message = socket.recv()
print(f"Request sent: {message}")
"""