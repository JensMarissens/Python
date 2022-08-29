import os

def addFile():
    invoer = input("Enter preferred file name: ")
    extention = input("Choose file extention type: ")
    fileName = invoer + extention

    cDir = os.listdir("C:\\Users\\The Hub\\Documents")
    if fileName in cDir:
        invoer = input("A file with this name already exists, please provide another: ")
        fileName = invoer + extention
        file = open(fileName, "w+")
    else:
        file = open(fileName, "w+")


def addFolder():
    invoer = input("Would you like to create a new Document folder? (y/n): ")
    if invoer.lower() == 'y':
        folderName = input("Folder name: ")

        cDir = os.listdir("C:\\Users\\The Hub\\Documents")
        if folderName in cDir:
            folderName = input("This folder already exists, provide a different name: ")
            os.mkdir(folderName)
        else:
            os.mkdir(folderName)
        os.chdir(r"C:\Users\The Hub\Documents\\" + folderName)
        addFile()
    elif invoer.lower() == 'n':
        addFile()
    else:
        print("Invalid input, existing..")


def main():
    print("\n####################### FILE EDITOR #######################")
    os.chdir(r"C:\Users\The Hub\Documents")
    print("Changing directory location to: " + os.getcwd() + "\n")
    addFolder()

    print("\nProgram exectued succesfully")
    print("##################### END FILE EDITOR #####################")


if __name__ == "__main__":
    main()
