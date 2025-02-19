# Prerequisites
This microservice is written in Python and requires the use of **ZeroMQ** to pipe communications between two independent Python processes. The microservice **must be started up and listening** to make calls to the API. To start up the microservice, you can write: 
```
python ruleSearching.py
```
**Packages required to send/receive data are ```zmq``` and ```json```.** The microservice will continually listen until it receives a certain type of input, explained in the section below.

# How to REQUEST Data
ALL data must be sent as a dictionary, encoded into a byte string. The expected dictionary format is as follows:
```
input_dict = {
    "option": [value is 0, 1, 2, or 3],
    "searchTerm": [value is a string, cannot be ""],
    "category": [value is 1, 2, or ""]
}
```
```option``` = 0 indicates quitting the microservice. The microservice will continue listening for a request otherwise.
```option``` = 1 indicates searching for rules by keyword. 
```option``` = 2 indicates searching for spells/feats by keyword. 
```option``` = 3 indicates searching for game mechanics by keyword. 
The keyword to search by is stored in ```searchTerm```. 
```category``` is only required when searching for spells/feats by keyword. In that case, ```category``` = 1 indicates searching for a spell, ```category``` = 2 indicates searching for a feat.

The requesting Python application must set up a ZeroMQ context. The Rule Searching microservice listens on ```tcp://localhost:5555``` and expects a byte string, which will require using the ```json``` package. An example of sending a request is as follows:
```python
# set up dictionary input
dict = {
    "option":3,          # search for spells/feats
    "searchTerm":"aCiD", # keyword is "acid" (case insensitive)
    "category":1,        # search for spells specifically
}

# jsonify the dictionary -- can only send a byte string
jsonInput = json.dumps(dict, default=str)

# set up ZeroMQ
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# send request (the byte string!)
socket.send_string(jsonInput)
```

# How to RECEIVE Data
Data will be sent through ZeroMQ as a list of ```json``` objects (basically dictionaries), encoded as a byte string. Before using the object, the program receiving data from Rules Searching must decode the response back to a list of ```json``` objects. An example of receiving a response is as follows:
```python
# get the response -- IT WILL BE A BYTE STRING
message = socket.recv()

# convert byte string message to json
decoded = json.loads(message.decode('utf-8'))
json_loaded = json.loads(decoded)
json_array = json.dumps(json_loaded, indent=3, sort_keys=True) # indent changes the output format, sort_keys sorts the keys alphabetically each time

# print the json list
print(f"Response sent back: {json_array}")
```
# UML Sequence Diagram
![UML Sequence Diagram for Rule Searching Microservice](https://github.com/jamie-dang-n/CS361-MicroserviceA/blob/main/MicroserviceA-UML.png)
