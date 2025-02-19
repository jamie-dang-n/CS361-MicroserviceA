import zmq
import json

def getInt(minVal, maxVal):
    invalidInput = True
    while (invalidInput):
        try:
            intVal = int(input("Enter your choice: "))
            if (intVal < minVal or intVal > maxVal):
                print("Invalid input. Please enter a valid value!")
            else:
                invalidInput = False
        except ValueError:
            print("Invalid input. Please enter an integer!")
    return intVal

def main():
    # get user input for Option
    print("Select an option [1,2,3], where the values are as follows:")
    print("Option 1: Search for rules by keyword")
    print("Option 2: Search for Spells/Feats by keyword")
    print("Option 3: Search for game mechanics (rulesets) by keyword")
    option = getInt(1, 3)

    # get user input for searchTerm
    searchTerm = input("Enter your search keyword: ")

    # set category if option == 2
    category = 0
    if (option == 2):
        print("Select a category [1,2], where the values are as follows:")
        print("Option 1: Search for Spells by keyword")
        print("Option 2: Search for Feats by keyword")
        category = getInt(1,2)

    # set up dictionary input
    dict = {
        "option":option,
        "searchTerm":searchTerm,
        "category":category,
    }

    # jsonify the dictionary -- can only send a byte string
    jsonInput = json.dumps(dict, default=str)

    # set up ZeroMQ
    context = zmq.Context()
    print("Connecting to server…")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # send request
    print(f"Request sent: {jsonInput}")
    socket.send_string(jsonInput)

    # get the response -- IT WILL BE A BYTE STRING
    message = socket.recv()

    # convert byte string message to json if message isn't emtpy
    if (len(message) != 0):
        decoded = message.decode('utf-8')
        json_loaded = json.loads(decoded)
        json_array = json.dumps(json_loaded, indent=3, sort_keys=True)
        print(f"Response sent back: {json_array}")

if __name__ == "__main__":
    main()

