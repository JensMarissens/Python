import os

def addFile():
    invoer = input("Enter preferred file name: ")
    extention = input("Choose file extention type (without dot): ")
    fileName = invoer + "." + extention

    cDir = os.listdir("C:\\Users\\The Hub\\Documents") #collect all files in Documents folder
    if fileName in cDir: #check if the filename already exists for the specified extention type if yes, get new input, if no create file
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
        if folderName in cDir: #check for identical folder names
            folderName = input("This folder already exists, provide a different name: ")
            os.mkdir(folderName) #create folder
        else:
            os.mkdir(folderName)
        os.chdir(r"C:\Users\The Hub\Documents\\" + folderName) #auto redirect to the newly created folder
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
