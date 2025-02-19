import zmq
import json

# Receive integer input between minVal and maxVal
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

# Get user input and direct communication with the Microservice
def main():
    option = 1
    # set up ZeroMQ
    context = zmq.Context()
    print("Connecting to server…")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    while (option != 0):
        # get user input for Option
        print("Select an option [0,1,2,3], where the values are as follows:")
        print("Option 0: Quit this service")
        print("Option 1: Search for rules by keyword")
        print("Option 2: Search for Spells/Feats by keyword")
        print("Option 3: Search for game mechanics (rulesets) by keyword")
        option = getInt(0, 3)

        # get further information if user does not quit
        if (option != 0):
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
        else:
            # user chose to quit
            # set up dictionary input to communicate quitting
            dict = {
                "option":option,
                "searchTerm":"",
                "category":0,
            }
            jsonInput = json.dumps(dict, default=str)
            print(f"Request sent: {jsonInput}")
            socket.send_string(jsonInput)
            message = socket.recv()
            decoded = message.decode('utf-8')
            print(f"Response sent back: {decoded}")
            print("Exiting the test program.")

if __name__ == "__main__":
    main()

