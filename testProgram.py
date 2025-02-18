import zmq
import json

def main():
    # set up dictionary
    dict = {
        "option":2,
        "searchTerm":"ace",
        "category":2,
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

    # convert byte string message to json
    decoded = json.loads(message.decode('utf-8'))
    print(f"Response sent back: {decoded}")

if __name__ == "__main__":
    main()
