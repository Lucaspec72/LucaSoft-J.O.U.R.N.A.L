import time, sys, hashlib, datetime, json, os, texteditor, winsound, pyAesCrypt, shutil, getpass, msvcrt
bufferSize = 64 * 1024 
dataFolder = 'C:/LucaSoft J.O.U.R.N.A.L/'
writeSpeed = 0.03

#PROGRAM VERSION
progVer = "0.7.4 (write() integration WIP version)"

month = ['January','February','March','April','May','June','July','August','September','October','November','December']
class dialogue:
    def loginMain():
        text=[f'Welcome to the ','J.O.U.R.N.A.L',', please enter your name : ']
        style=[colors.message,colors.special,colors.message]
        return text,style
    def loginCancel():
        text=['Understood, closing program. Have a good day.']
        style=['']
        return text,style
    def loginPwdPrompt():
        text=['Please enter your password : ']
        style=['']
        return text,style
    def loginGreet1():
        text=['Good morning, ',f'{currentUser}','.']
        style=[colors.message,colors.special,colors.message]
        return text,style
    def loginGreet2():
        text=['Good afternoon, ',f'{currentUser}','.']
        style=[colors.message,colors.special,colors.message]
        return text,style
    def loginGreet3():
        text=['Good evening, ',f'{currentUser}','.']
        style=[colors.message,colors.special,colors.message]
        return text,style
    def loginErrPwd():
        text=['/!\\ incorrect Password /!\\']
        style=[colors.red]
        return text,style
    def loginEmptyUsr():
        text=['/!\\ Username Cannot be Empty /!\\']
        style=[colors.red]
        return text,style
    def loginNewUsrPrompt():
        text=['The user "',f'{currentUser}','" does not currently exists, do you want to create it ? (press ','Y',') ']
        style=['',colors.special,colors.message,colors.label,colors.message]
        return text,style
    def loginNewUsrPwd():
        text=['Please enter a password : ']
        style=['']
        return text,style
    def loginNewUsrPwdCfrm():
        text=['Please confirm your password : ']
        style=['']
        return text,style
    def loginNewUsrPwdErr():
        text=['/!\\ incorrect Password /!\\']
        style=[colors.red]
        return text,style
    def loginNewUsrCancel():
        text=['Acknowledged, returning to Login menu.']
        style=['']
        return text,style
    def mainMenu():
        text=['========[','MAIN MENU',']=========','  Logged User : ',f'{currentUser}','  Number of Entries : ',{len(folderFiles)},'    1. ','Create a New Entry','    2. ','List Entries','    3. ','View Entry','    4. ','Read all Entries','    5. ','Import Logs','    6. ','Export Logs','    0. ','Exit','Please Select a Option : ']
        style=[f'{colors.label}',colors.data,colors.label,'\n\n',colors.special,f'\n{colors.label}',colors.special,f'\n\n{colors.label}',colors.data,f'\n{colors.label}',colors.data,f'\n{colors.label}',colors.data,f'\n{colors.label}',colors.data,f'\n\n{colors.label}',colors.data,f'\n{colors.label}',colors.data,f'\n\n{colors.label}',colors.data,f'\n\n{colors.message}']
        return text,style
    def createLog1():
        text=[f'Creating Log N°{len(folderFiles)+1}']
        style=['']
        return text,style
    def createLog2():
        text=[f'Written File - Log N°{len(folderFiles)+1}']
        style=['']
        return text,style
    def createLog3():
        text=['No contents, aborting entry creation.']
        style=['']
        return text,style
    def listEntries1():
        text=['Currently, there is ',f'{len(folderFiles)}',' entry in the database.']
        style=['',colors.special,colors.message]
        return text,style
    def listEntries2():
        text=['currently, there are no entries in the database.']
        style=['']
        return text,style
    def listEntries3():
        text=['Currently, there are ',f'{len(folderFiles)}',' entries in the database.']
        style=['',colors.special,colors.message]
        return text,style
    def listEntries4():
        text=[" Here's a list of all existing log entries :"]
        style=['']
        return text,style
    def goBackToMain():
        text=['Press Enter to go back to Main Menu']
        style=[colors.message]
        return text,style
    def viewEntry1():
        text=['Select Which Entry to View : n°']
        style=['']
        return text,style
    def viewEntry2():
        text=['Entry found, Displaying Log...']
        style=['']
        return text,style
    def eol():
        text=['[}-----End of Log-----{]']
        style=[f'\n{colors.special}']
        return text,style
    def errWrongPwd():
        text=['/!\\ ERROR : Could not decrypt file, Password is incorrect /!\\','This log was encrypted using a different encryption key than yours.']
        style=[colors.red,f'\n{colors.darkRed}']
        return text,style
    def readAllEndMessage():
        text=['Finished printing entry n°',f'{entryNum}',' / ',f"{len(folderFiles)}"]
        style=['',colors.special,colors.message,colors.special]
        return text,style
    def continueOrExit():
        text=['Press Enter to continue, or type "exit" to stop : ']
        style=['']
        return text,style
    def importFiles1():
        text=['Are you sure you want to import your log files ? (press ','Y',')']
        style=['',colors.label,colors.message]
        return text,style
    def importFilesConfirm():
        text=['Please put all your log files in the "',f'{dataFolder}import_{currentUser}',f'" folder, with name formating entrynumber.log (exemple : ',f'1.log',' )','/!\\ DISCLAIMER : CURRENT ENTRIES WILL GET OVERWRITTEN /!\\',' You may want to back up your logs first.','Please type "','continue','" to continue, otherwise operation will be canceled : ']
        style=['',colors.data,colors.message,colors.data,colors.message,f'\n{colors.red}',colors.message,'\n',colors.data,colors.message]
        return text,style            
    def importFilesResult():
        text=['Imported ',f'{entriesImported}',' entries to folder "',f'{dataFolder}{currentUser}','"']
        style=['',colors.data,colors.message,colors.data,colors.message]
        return text,style
    def importedEntryMessage():
        text=['Inported entry ',f'{entry}']
        style=['',colors.message]
        return text,style
    def exportFiles1():
        text=['Are you sure you want to export all of your log files ? (press ','Y',')']
        style=['',colors.label,colors.message]
        return text,style
    def exportedEntryMessage():
        text=['Exported entry n°',f'{entryNum}']
        style=['',colors.message]
        return text,style
    def exportFilesResult():
        text=['Exported ',f'{iter}',' entries to folder "',f'{dataFolder}exported_{currentUser}','"']
        style=['',colors.data,colors.message,colors.data,colors.message]
        return text,style
    def exitMessage():
        text=['Logging off, Have a good day ',f'{currentUser}','.']
        style=['\n',colors.special,colors.message]
        return text,style
    def holder():
        text=[]
        style=[]
        return text,style

class colors:
    label = '\033[38;2;220;140;60m'
    data = '\033[38;2;200;180;90m'
    green = '\033[32m'
    red = '\033[91m'
    darkRed = '\033[38;2;160;0;0m'
    white = '\033[0m'
    message = '\033[38;2;220;140;60m'
    special = '\033[38;2;180;150;120m'

#creates the Data folder ('C:/LucaSoft J.O.U.R.N.A.L/') if it doesn't exists
if(os.path.exists(f"{dataFolder}") == False):
    os.mkdir(f"{dataFolder}")

#function to print text with typewriter effect
def printText(str):
    global writeSpeed
    for letter in str:
        print(letter, end="")
        sys.stdout.flush()
        time.sleep(writeSpeed)
        if((letter == ",") or (letter == '.') and (writeSpeed != 0)):
            time.sleep(0.07)
        if msvcrt.kbhit():
            writeSpeed = 0
            msvcrt.getch()

#resets the writeSpeed if it was set to zero
def resetWriteSpeed():
    global writeSpeed
    writeSpeed = 0.03

#makes two beeps, mostly used after writing stuff on-screen.
def endLineSound():
    winsound.Beep(2200, 15)
    winsound.Beep(1900, 30)
    time.sleep(0.03)

def successSound():
    winsound.Beep(1700, 60)
    winsound.Beep(2000, 60)
    winsound.Beep(2300, 60)
    winsound.Beep(2600, 250)
#returns the list of all files in the current user's folder that have the extension .entry
def updateFolderFiles():
    filesArray = []
    for root, dirs, files in os.walk(f"{dataFolder}{currentUser}"):
        for file in files:
            if file.endswith(".entry"):
                fileNum = file.replace(".entry","")
                filesArray.insert(int(fileNum)-1,file)
                # filesArray.append(file)
    return filesArray 

#PROTOTYPE writing system that handles the swapping between printText and print
def write(obj,list=0):
    arrayText=obj[0]
    arrayDiv=obj[1]
    i=0
    if(len(arrayText) == len(arrayDiv)):
        print('\n')
        for Text in arrayText:
            winsound.Beep(1650, 20)
            print(arrayDiv[i], end="")
            printText(Text)
            i += 1
        print(colors.message, end="")
        if(list == 0):
            print(colors.message, end="")
            endLineSound()
            resetWriteSpeed()
            

#returns the list of all files in the current user's IMPORT folder that have the extension .log, only used once currently i think. 
def updateFolderFilesImport():
    filesArray = []
    for root, dirs, files in os.walk( f"{dataFolder}import_{currentUser}"):
        for file in files:
            if file.endswith(".log"):
                filesArray.append(file)
    return filesArray 

#defines clear()
cl = lambda: os.system('cls')
def clear():
    cl()
    print(f"{colors.data}J.O.U.R.N.A.L      {colors.label}v{progVer}{colors.data}        (C) Copyright 2021 Lucasoft\n{colors.label}")

def askUser():
    prompt = input(f"{colors.special}")
    print(f'{colors.message}',end="")
    return prompt

def longestInArray(array):
    max_len = -1
    for element in array: 
        if(len(element) > max_len): 
          max_len = len(element) 
          #longest = element not currently used, might be useful later
          return max_len

#open users json dictionary, or define it if it doesn't exists.
if os.path.exists(f"{dataFolder}users.json"):
    f = open(f"{dataFolder}users.json")
    user = json.load(f)
else:
    user = {}

def removeTemptxt():
    if(os.path.exists(f'{dataFolder}temp.txt')):
        os.remove(f'{dataFolder}temp.txt')

#sets userConnected to false, it's the flag that keeps the login loop going.
userConnected = False
#Login Loop
while(userConnected == False):
    time.sleep(0.5)
    clear()
    write(dialogue.loginMain())
    currentUser = askUser()
    if(currentUser == "exit"):
        write(dialogue.loginCancel())
        if msvcrt.kbhit():
            msvcrt.getch()
        print(f'{colors.white}', end="")
        cl()
        raise SystemExit(0)
    if currentUser in user:
        write(dialogue.loginPwdPrompt())
        currentPassword = getpass.getpass("")
        currentPassword = currentPassword.encode("utf8")
        dgst = hashlib.sha1(currentPassword).hexdigest()
        if dgst == user[currentUser]['password'] :
            currentTime = datetime.datetime.now()
            userConnected = True
            if currentTime.hour < 12:
                write(dialogue.loginGreet1())
            elif 12 <= currentTime.hour < 18:
                write(dialogue.loginGreet2())
            else:
                write(dialogue.loginGreet3())
        else:
            write(dialogue.loginErrPwd())
    elif(currentUser == ""):
        write(dialogue.loginEmptyUsr())
    else:
        write(dialogue.loginNewUsrPrompt())
        char = msvcrt.getch()
        if (char.lower() == b'y'):
            #note : askUser() is used instead of getpass.getpass() to actually see what you're writing.
            write(dialogue.loginNewUsrPwd())
            currentPassword = askUser()
            write(dialogue.loginNewUsrPwdCfrm())
            currentPassword2 = askUser()
            if((currentPassword==currentPassword2) & (currentPassword != "")):
                del(currentPassword2)
                currentPassword = currentPassword.encode("utf8")
                dgst = hashlib.sha1(currentPassword).hexdigest()
                user[currentUser] = {'password': dgst}
                with open(f"{dataFolder}users.json", 'w') as f:
                    json.dump(user, f)
                if(os.path.exists(f"{dataFolder}{currentUser}") == False):
                    os.mkdir(f"{dataFolder}{currentUser}")
                currentTime = datetime.datetime.now()
                userConnected = True
                if currentTime.hour < 12:
                    write(dialogue.loginGreet1())  
                elif 12 <= currentTime.hour < 18:
                    write(dialogue.loginGreet2())
                else:
                    write(dialogue.loginGreet3())
            else:
                write(dialogue.loginNewUsrPwdErr())
        else:
            write(dialogue.loginNewUsrCancel())

#checks if user folder doesn't exists, and creates it if it doesn't.
if(os.path.exists(f"{dataFolder}{currentUser}") == False):
    os.mkdir(f"{dataFolder}{currentUser}")
#checks if the temp.txt folder exists.
removeTemptxt()

#main loop
while(True):
    folderFiles = updateFolderFiles()
    time.sleep(0.5)
    clear()
    write(dialogue.mainMenu())
    instruction = askUser()
    folderFiles = updateFolderFiles()
    clear()
    if(instruction == "1"):
        write(dialogue.createLog1())
        logEntry = texteditor.open(encoding='utf8')
        if(logEntry != ""):
            with open(f"{dataFolder}temp.txt", 'w',encoding='utf8') as f:
                timeFormated = datetime.datetime.now()
                f.write(f"{currentUser}'s Journal, Entry N°{len(folderFiles)+1}. Written on {month[(timeFormated.month-1)]} {timeFormated.day} {timeFormated.year} at {format(timeFormated.hour, '02')}:{format(timeFormated.minute, '02')}\n\n{logEntry}")
            pyAesCrypt.encryptFile(f"{dataFolder}temp.txt", f"{dataFolder}{currentUser}/{len(folderFiles)+1}.entry", str(currentPassword), bufferSize) 
            write(dialogue.createLog2())
            removeTemptxt()
            successSound()
        else:
            write(dialogue.createLog3())
    elif(instruction == "2"):
        if(len(folderFiles) < 2):
            if(len(folderFiles) == 1):
                write(dialogue.listEntries1())
            else:
                write(dialogue.listEntries2())
        else:
            write(dialogue.listEntries3())
        if(len(folderFiles) != 0):
            write(dialogue.listEntries4())
            fileState = "Unknown"
            fileStateColor = colors.special
            print('\n')
            for file in folderFiles:
                print(colors.special, end="")
                removeTemptxt()
                try:
                    pyAesCrypt.decryptFile(f'{dataFolder}{currentUser}/{file}', f"{dataFolder}temp.txt", str(currentPassword), bufferSize) 
                    fileStateColor = colors.green
                    fileState = "Readable"

                except:
                    fileStateColor = colors.red
                    fileState = "Unreadable"
                removeTemptxt()
                length = longestInArray(folderFiles)+13
                toWrite = f"    file: {file}  "
                offset = length - len(toWrite)
                toWrite += ' ' * offset
                printText(toWrite) ; print(fileStateColor,end='') ; printText(f'{fileState}\n')
                winsound.Beep(1650, 20)
        write(dialogue.goBackToMain())
        getpass.getpass("")
    elif(instruction == "3"):
        write(dialogue.viewEntry1())
        entryToView = askUser()
        if(os.path.exists(f'{dataFolder}{currentUser}/{entryToView}.entry')):
            try:
                pyAesCrypt.decryptFile(f'{dataFolder}{currentUser}/{entryToView}.entry', f"{dataFolder}temp.txt", str(currentPassword), bufferSize)
                file = open(f'{dataFolder}temp.txt', 'r', encoding='utf-8')
                listOfLines = file.readlines()
                file.close()
                removeTemptxt()
                write(dialogue.viewEntry2())
                time.sleep(0.5)
                clear()
                for line in listOfLines:
                    printText(f'{line}\n')
                    winsound.Beep(1650, 20)
                    time.sleep(0.3)
                write(dialogue.eol())
            except ValueError :
                write(dialogue.errWrongPwd())

            write(dialogue.goBackToMain())
            getpass.getpass("")
    elif(instruction == "4"):
        folderFiles = updateFolderFiles()
        stopReadLogs = ""
        for entryToView in folderFiles:
            if(stopReadLogs.lower() == "exit"):
                break
            else:
                clear()
                entryNum = entryToView.replace(".entry","")
                try:
                    pyAesCrypt.decryptFile(f'{dataFolder}{currentUser}/{entryToView}', f"{dataFolder}temp.txt", str(currentPassword), bufferSize) 
                    file = open(f'{dataFolder}temp.txt', 'r', encoding='utf-8')
                    listOfLines = file.readlines()
                    file.close()
                    removeTemptxt()
                    for line in listOfLines:
                        printText(f'{line}\n')
                        winsound.Beep(1650, 20)
                        time.sleep(0.3)
                    write(dialogue.eol())
                    print('\n\n')
                    write(dialogue.readAllEndMessage())
                except ValueError:
                    write(dialogue.errWrongPwd())
                    #keep that for now, will change this when the new log file system is added
                    printText(f'\n[/!\] THIS IS A TEMPORARY ERROR MESSAGE [/!\]')
                    printText(f'\nERROR : could not print entry n°{entryNum} ({entryToView}).')
                    resetWriteSpeed()
                write(dialogue.continueOrExit())
                stopReadLogs = askUser()
    elif(instruction == "5"):
        write(dialogue.importFiles1())
        confirmImport = msvcrt.getch()
        if (confirmImport.lower() == b"y"):
            if(os.path.exists(f"{dataFolder}import_{currentUser}") == False):
                os.mkdir(f"{dataFolder}import_{currentUser}")
            write(dialogue.importFilesConfirm())
            confirmImport = askUser()
            if(confirmImport.lower() == "continue"):
                entriesImported = 0
                folderFiles = updateFolderFilesImport()
                for entry in folderFiles:
                    entryNum = entry.replace(".log","")
                    pyAesCrypt.encryptFile(f"{dataFolder}import_{currentUser}/{entry}", f'{dataFolder}{currentUser}/{entryNum}.entry', str(currentPassword), bufferSize) 
                    write(dialogue.importedEntryMessage(),1)
                    entriesImported += 1
                    winsound.Beep(1650, 20)
                inportedFiles = updateFolderFiles()
                write(dialogue.importFilesResult())
                if(os.path.exists(f"{dataFolder}import_{currentUser}") == True):
                    shutil.rmtree(f"{dataFolder}import_{currentUser}")
                successSound()
                write(dialogue.goBackToMain())
                getpass.getpass()
            else:
                if(os.path.exists(f"{dataFolder}import_{currentUser}") == True):
                    shutil.rmtree(f"{dataFolder}import_{currentUser}")
    elif(instruction == "6"):
        #batched modifications, test everything later
        write(dialogue.exportFiles1())
        confirmExport = msvcrt.getch()
        if (confirmImport.lower() == b"y"):
            folderFiles = updateFolderFiles()
            if(os.path.exists(f"{dataFolder}exported_{currentUser}") == False):
                os.mkdir(f"{dataFolder}exported_{currentUser}")
            iter = 0
            for entry in folderFiles:
                entryNum = entry.replace(".entry","")
                try:
                    pyAesCrypt.decryptFile(f'{dataFolder}{currentUser}/{entry}', f"{dataFolder}exported_{currentUser}/{entryNum}.log", str(currentPassword), bufferSize) 
                    write(dialogue.exportedEntryMessage(),1)
                    iter += 1
                except ValueError:
                    write(dialogue.errWrongPwd())
                    time.sleep(0.5)
                winsound.Beep(1650, 20)
            exportedFiles = next(os.walk(f"{dataFolder}exported_{currentUser}"))[2]
            write(dialogue.exportFilesResult())
            successSound()
            write(dialogue.goBackToMain())
            getpass.getpass()
    elif((instruction == "0") or (instruction.lower() == "exit")):
        cl()
        write(dialogue.exitMessage())
        winsound.Beep(2300, 100)
        winsound.Beep(2100, 20)
        winsound.Beep(1900, 75)
        winsound.Beep(1700, 20)
        winsound.Beep(1500, 130)
        print(f'{colors.white}', end="")
        if msvcrt.kbhit():
            msvcrt.getch()
        cl()
        raise SystemExit(0)


raise SystemExit(0)

# ACRONIM

# J   Just
# O   anOther
# U   User
# R   Redaction
#     &
# N   Navigation
# A   Assistant
#     by
# L   Lucaspec72