def start():
    print("####################### TERMINAL #######################\n")

    rooms = ["Living Room", "Kitchen", "Dining Room", "Bathroom", "Hallway", "Bedroom 1", "Bedroom 2", "Garage",
             "Front Porch", "Back Porch"]

    arrPrint = [[rooms[0], rooms[1], rooms[2]],
                [rooms[3], rooms[4], rooms[5]],
                [rooms[6], rooms[7], rooms[8]],
                [rooms[9]]]

    for r in arrPrint:
        for c in r:
            print(c, end="\t\t")
        print()
    print()
    slc = int(input("Please select the room you would like to adjust: "))
    roomSelect(rooms, slc)

def roomSelect(rooms, slc):
    temp = rooms[slc - 1]
    editRoom(temp)


def editRoom(temp):
    print("\n###################### " + temp.upper() + " ######################\n")




class Room:
    def __init__(self, lights, hifi, temperature):
        self.lights = lights
        self.hifi = hifi
        self.temperature = temperature


# In the CLI we by room, then service
# In the GUI we go by both


def main():
    start()


if __name__ == "__main__":
    # execute only if run as a script
    main()
