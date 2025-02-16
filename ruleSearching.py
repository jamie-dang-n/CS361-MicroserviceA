"""
The Rule Searching Microservice (microservice A) uses ZeroMQ to send responses/requests of json-converted dictionaries between two independent programs. This microservice will process the given dictionary (formatted as below) to create an API call to https://api.open5e.com/?format=api. If the API call is successful, the program will respond with the API json entry. Note that you MUST convert the byte string in the response to a dictionary after receiving it.
"""

import zmq
import requests
import json

"""
Expected input format: jsonified dictionary (let "" represent a null (empty) string)
input_dict = {
    "option": [value is 1, 2, or 3],
    "searchTerm": [value is a string, cannot be ""],
    "category": [value is "" for option 1 or 3, but string value is required for 2.]
    "hasValidData": [value is 1 = True or 0 = False]
}
Option = 1 -> search for rules by keyword
Option = 2 -> search for Spells/Abilities by keyword
Option = 3 -> search for game mechanics by keyword
"""

# valid fields
valid_fields = ['option', 'searchTerm', 'category', 'hasValidData']

def main():
    # set up ZeroMQ
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    # Binds REP socket to tcp://*:5555
    socket.bind("tcp://localhost:5555")

    # Wait for next request from client
    # Requests will always come in byte string form
    message = socket.recv()
    print(f"Received request: {message}")

    # convert byte string message to json
    decoded = json.loads(message.decode('utf-8'))
    print(f"Decoded request: {decoded}")

    isValid = convertInt(decoded, valid_fields[3])
    if (isValid == 1):
        option = convertInt(decoded, valid_fields[0])
        if (option == 1):
            findKeyword()
        elif (option == 2):
            findSpellsAbilities()
        elif (option == 3):
            findMechanics()
        else:
            print(f"Invalid option chosen.")

    # send response to client
    socket.send(message)


# convertInt is used to convert fields
# from the input dictionary (hasValidData and option)
# to an integer. if conversion fails, the int = -1
def convertInt(dict, field):
    returnInt = 0
    try:
        if (dict[field]):
            returnInt = int(dict[field])
    except ValueError:
        returnInt = -1
    return returnInt


# Search rules by keyword
def findKeyword():
    print("1")

# search for spells/abilities by keyword
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

