import zmq
import requests
import json

"""
The Rule Searching Microservice (microservice A) uses ZeroMQ to send responses/requests of json-converted dictionaries between two independent programs. This microservice will process the given dictionary (formatted as below) to create an API call to https://api.open5e.com/?format=api. If the API call is successful, the program will respond with the API json entry. Note that you MUST convert the byte string in the response to a dictionary after receiving it.

Expected input format: jsonified dictionary (let "" represent a null (empty) string)
input_dict = {
    "option": [value is 1, 2, or 3],
    "searchTerm": [value is a string, cannot be ""],
    "category": [value is "" for option == 1 or 3, but integer value (1 for spell or 2 for abilities) is required for option == 2.]
}
Option = 1 -> search for rules by keyword
Option = 2 -> search for Spells/Feats by keyword
Option = 3 -> search for game mechanics by keyword

Output Format: a list of matching JSON objects
"""

# valid fields for the input dictionary
valid_fields = ['option', 'searchTerm', 'category', 'hasValidData']

# valid fields for the "spell" part of the API
valid_spell_fields = ['range_unit', 'shape_size_unit', 'name', 'desc', 'higher_level', 'target_type', 'range_text', 'casting_time', 'material_specified', 'saving_throw_ability', 'duration']

# valid fields for the "feats" part of the API
# note: 'benefits' is itself a list of dictionaries-- search that separately
valid_feats_fields = ['name', 'desc', 'prerequisite']

# main() program to direct input
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

    # check validity -- searchTerm exists
    isValid = False
    if (len(decoded[valid_fields[1]]) > 0):
        isValid = True
    
    # if searchTerm exists, do the appropriate search and store
    # the matching results in returnArray
    returnArray = []
    if (isValid):
        option = convertInt(decoded, valid_fields[0])
        if (option == 1):
            returnArray = findRules(decoded)
        elif (option == 2):
            returnArray = findSpellsFeats(decoded)
        elif (option == 3):
            returnArray = findMechanics(decoded)
        else:
            print(f"Invalid option chosen.")

    # convert returnArray to byte string
    jsonReturnString = json.dumps(returnArray)
    returnByteString = jsonReturnString.encode('utf-8')

    # send response to client
    socket.send(returnByteString)


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
def findRules(dict_input):
    print("1")

# search for spells/feats by keyword
def findSpellsFeats(dict_input):
    outputArray = []
    if (dict_input['category']):
        category = convertInt(dict_input, valid_fields[2])
    if (category == 1):
        url = "https://api.open5e.com/v2/spells/?format=json"
        currResponse = requests.get(url)
        if (currResponse.status_code == 200):
                spells = currResponse.json()
                for spell in spells['results']:
                    for entry in valid_spell_fields:
                        if (spell[entry]):
                            found = spell[entry].find(dict_input['searchTerm'])
                            if (found != -1):
                                outputArray.append(spell)
    else:
        url = "https://api.open5e.com/v2/feats/?format=json"
        currResponse = requests.get(url)
        if (currResponse.status_code == 200):
                feats = currResponse.json()
                for feat in feats['results']:
                    for entry in valid_feats_fields:
                        if (feat[entry]):
                            found = feat[entry].find(dict_input['searchTerm'])
                            if (found != -1):
                                outputArray.append(feat)
                        if (feat['benefits']): 
                            for benefit in feat['benefits']:
                                for desc in benefit:
                                    found = benefit[desc].find(dict_input['searchTerm'])
                        
    return outputArray

# search for game mechanics by keyword
def findMechanics(dict_input):
    print("3")


if __name__ == "__main__":
    main()