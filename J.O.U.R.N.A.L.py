import os
try:
    import time, sys, hashlib, datetime, json, texteditor, winsound, pyAesCrypt, shutil, getpass, msvcrt, io
    from pytimedinput import timedInput
except:
    print("Error, missing modules. Trying to download the required modules...")
    os.system("python -m pip install -r requirements.txt --quiet")
try:
    import time, sys, hashlib, datetime, json, texteditor, winsound, pyAesCrypt, shutil, getpass, msvcrt, io
    from pytimedinput import timedInput
except:
    print('Could not load program, missing modules')
    raise SystemExit
BUFFERSIZE = 64 * 1024 
DATAFOLDER = 'C:/LucaSoft J.O.U.R.N.A.L/'
WRITESPEED = 0.03

#PROGRAM VERSION
progVer = "0.7.7"

def encrypt(data, pwd):
    try:
        pwd.decode("utf8")
    except UnicodeError:
        pwd = pwd.encode("utf8")
    data = bytes(data,'UTF-8')
    input = io.BytesIO(data)
    output = io.BytesIO()
    pyAesCrypt.encryptStream(input, output, str(pwd), BUFFERSIZE)
    return output.getvalue()

def decrypt(encryptedData, pwd):
    try:
        pwd.decode("utf8")
    except UnicodeError:
        pwd = pwd.encode("utf8")
    input = io.BytesIO(encryptedData)
    output = io.BytesIO()
    ctlen = len(encryptedData)
    pyAesCrypt.decryptStream(input, output, str(pwd), BUFFERSIZE, ctlen)
    return output.getvalue()

def toText(input):
    return str(input.decode("utf-8"))

def getEntry(input):
    return bytes.fromhex(input['entry'])

def readEntryFile(entry,user=False):
    if(user == False):
        user = currentUser
    fullPath = f'{DATAFOLDER}{user}/{entry}'
    if(os.path.exists(fullPath)):
        try:
            with open(fullPath,'r', encoding="utf-8") as file:
                return json.load(file)
        except:
            return False

def writeEntryFile(user,pwd,entry):
    folderFiles = updateFolderFiles()
    try:
        pwd.decode("utf8")
    except UnicodeError:
        pwd = pwd.encode("utf8")
    hashKey = hashlib.sha1(pwd).hexdigest()
    writeToFile = {'user': user,'hashKey': hashKey,'entry': entry.hex()}
    if(len(folderFiles) > 0):
        lastEntry = int(folderFiles[-1].replace(".entry",""))
    else:
        lastEntry = 0
    with open(f'{DATAFOLDER}{user}/{lastEntry+1}.entry', 'w', encoding="utf-8") as file:
        json.dump(writeToFile, file)

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
    def loginGreet(timeofday):
        text=[f'Good {timeofday}, ',f'{currentUser}','.']
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
        text=['Entry ',f'{entryToView}',' found, Displaying Log...']
        style=['',colors.special,colors.message]
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
        text=['Please put all your log files in the "',f'{DATAFOLDER}import_{currentUser}',f'" folder, with name formating entrynumber.log (exemple : ',f'1.log',' )','/!\\ DISCLAIMER : CURRENT ENTRIES WILL GET OVERWRITTEN /!\\',' You may want to back up your logs first.','Please type "','continue','" to continue, otherwise operation will be canceled : ']
        style=['',colors.data,colors.message,colors.data,colors.message,f'\n{colors.red}',colors.message,'\n',colors.data,colors.message]
        return text,style            
    def importFilesResult():
        text=['Imported ',f'{iter}',' entries to folder "',f'{DATAFOLDER}{currentUser}','"']
        style=['',colors.data,colors.message,colors.data,colors.message]
        return text,style
    def importedEntryMessage():
        text=['Inported entry ',f'{entry}']
        style=[colors.message,colors.data]
        return text,style
    def exportFiles1():
        text=['Are you sure you want to export all of your log files ? (press ','Y',')']
        style=['',colors.label,colors.message]
        return text,style
    def exportedEntryMessage():
        text=['Exported entry n°',f'{entryNum}']
        style=[colors.message,colors.data]
        return text,style
    def exportFilesResult():
        text=['Exported ',f'{iter}',' entries to folder "',f'{DATAFOLDER}exported_{currentUser}','"']
        style=['',colors.data,colors.message,colors.data,colors.message]
        return text,style
    def exitMessage():
        text=['Logging off, Have a good day ',f'{currentUser}','.']
        style=['\n',colors.special,colors.message]
        return text,style
    def errReadFile(filename):
        text=[f'There was a error while reading {filename}, it is either corrupted or in a incompatible format.']
        style=[colors.red]
        return text,style

class colors:
    label = '\033[38;2;220;140;60m'
    data = '\033[38;2;200;180;90m'
    readable = '\033[32m'
    unreadable = '\033[91m'
    encrypted = '\033[38;2;255;221;0m'
    green = '\033[32m'
    red = '\033[91m'
    darkRed = '\033[38;2;160;0;0m'
    white = '\033[0m'
    message = '\033[38;2;220;140;60m'
    special = '\033[38;2;180;150;120m'
    def get(color):
        try:
            return getattr(colors, color)
        except:
            return colors.white

#creates the Data folder ('C:/LucaSoft J.O.U.R.N.A.L/') if it doesn't exists
if(os.path.exists(f"{DATAFOLDER}") == False):
    os.mkdir(f"{DATAFOLDER}")

#function to print text with typewriter effect
def printText(str):
    global WRITESPEED
    for letter in str:
        print(letter, end="")
        sys.stdout.flush()
        time.sleep(WRITESPEED)
        if((letter == ",") or (letter == '.') and (WRITESPEED != 0)):
            time.sleep(0.07)
        if msvcrt.kbhit():
            WRITESPEED = 0
            msvcrt.getch()

#resets the WRITESPEED if it was set to zero
def resetWRITESPEED():
    global WRITESPEED
    WRITESPEED = 0.03

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
    for root, dirs, files in os.walk(f"{DATAFOLDER}{currentUser}"):
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
            resetWRITESPEED()
            

#returns the list of all files in the current user's IMPORT folder that have the extension .log, only used once currently i think. 
def updateFolderFilesImport():
    filesArray = []
    for root, dirs, files in os.walk( f"{DATAFOLDER}import_{currentUser}"):
        for file in files:
            if file.endswith(".log"):
                fileNum = file.replace(".log","")
                filesArray.insert(int(fileNum)-1,file)
                # filesArray.append(file)
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
if os.path.exists(f"{DATAFOLDER}users.json"):
    with open(f"{DATAFOLDER}users.json", encoding="utf-8") as f:
        user = json.load(f)
else:
    user = {}

def removeTemptxt():
    if(os.path.exists(f'{DATAFOLDER}temp.txt')):
        os.remove(f'{DATAFOLDER}temp.txt')

def fileStatus(file,user=False,password=False):
    if(password == False):
        password = currentPassword
    if(user == False):
        user = currentUser
    fileData = readEntryFile(file,user)
    if(fileData):
        try:
            decrypt(getEntry(fileData),password)
            return 2
        except:
            return 1
    else:
        return 0

def getTimeOfDay():
    getTime = datetime.datetime.now()
    if getTime.hour < 12:
        return 'morning'
    elif 12 <= getTime.hour < 18:
        return 'afternoon'
    else:
        return 'evening'
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
        hashKey = hashlib.sha1(currentPassword).hexdigest()
        if hashKey == user[currentUser]['password'] :
            userConnected = True
            write(dialogue.loginGreet(getTimeOfDay()))
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
                hashKey = hashlib.sha1(currentPassword).hexdigest()
                user[currentUser] = {'password': hashKey}
                with open(f"{DATAFOLDER}users.json", 'w', encoding="utf-8") as f:
                    json.dump(user, f)
                if(os.path.exists(f"{DATAFOLDER}{currentUser}") == False):
                    os.mkdir(f"{DATAFOLDER}{currentUser}")
                userConnected = True
                write(dialogue.loginGreet(getTimeOfDay()))
            else:
                write(dialogue.loginNewUsrPwdErr())
        else:
            write(dialogue.loginNewUsrCancel())

#checks if user folder doesn't exists, and creates it if it doesn't.
if(os.path.exists(f"{DATAFOLDER}{currentUser}") == False):
    os.mkdir(f"{DATAFOLDER}{currentUser}")
#checks if the temp.txt folder exists.


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
        #temporary error catch for the issue reported by the_programmer_2215
        try:
            logEntry = texteditor.open(encoding='utf8')
        except RuntimeError:
            write([["ERROR, Coudn't find the default text editor of the system, trying to use fallback method..."],[colors.red]])
            write([["when you finished writing your entry, press start : "],[]])
            open(f'{DATAFOLDER}temp.tmp', 'w', encoding="utf-8").close()
            os.startfile(f'{DATAFOLDER}temp.tmp')
            getpass.getpass("")
            with open(f'{DATAFOLDER}temp.tmp','r', encoding="utf-8") as file:
                logEntry = file.read()
            os.remove(f'{DATAFOLDER}temp.tmp')
        if(logEntry != ""):
             timeFormated = datetime.datetime.now()
             writeEntryFile(currentUser,currentPassword,encrypt(f"{currentUser}'s Journal, Entry N°{len(folderFiles)+1}. Written on {month[(timeFormated.month-1)]} {timeFormated.day} {timeFormated.year} at {format(timeFormated.hour, '02')}:{format(timeFormated.minute, '02')}\n\n{logEntry}",currentPassword))
             write(dialogue.createLog2())
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
            length = longestInArray(folderFiles)+3
            for file in folderFiles:
                offset = length - len(file)
                fileLabel = f'{file}' + (' ' * offset)
                isReadable = fileStatus(file)
                if(isReadable != 0):
                    fileData = readEntryFile(file)
                    if(isReadable == 1):
                        isReadable = "encrypted"
                    if(isReadable == 2):
                        isReadable = "readable"
                    offset = 11 - len(isReadable)
                    isReadableLabel = isReadable + (' ' * offset)
                    write([['    file: ',fileLabel,isReadableLabel,'   Registered Owner: ',fileData['user']],[colors.message,colors.data,colors.get(isReadable),colors.message,colors.special]],1)
                else:
                    isReadable = "unreadable"
                    isReadableLabel = isReadable + (' ' * offset)
                    write([['    file: ',fileLabel,isReadableLabel,'   There was a error while reading the file, it is either corrupted or in a incompatible format.'],[colors.message,colors.data,colors.get(isReadable),colors.red]],1)
        write(dialogue.goBackToMain())
        getpass.getpass("")
    elif(instruction == "3"):
        write(dialogue.viewEntry1())
        numEntryToView = askUser()
        entryToView = f'{numEntryToView}.entry'
        if(os.path.exists(f'{DATAFOLDER}{currentUser}/{entryToView}')):
            isReadable = fileStatus(entryToView)
            fileData = readEntryFile(entryToView)
            if(isReadable == 2):
                entry = toText(decrypt(getEntry(fileData),currentPassword))
                write(dialogue.viewEntry2())
                time.sleep(0.5)
                clear()
                for line in entry.splitlines():
                    printText(f'{line}\n')
                    winsound.Beep(1650, 20)
                    time.sleep(0.3)
                write(dialogue.eol())
            else :
                write(dialogue.errReadFile(entryToView))
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
                isReadable = fileStatus(entryToView)
                if(isReadable == 2):
                    fileData = readEntryFile(entryToView)
                    entry = toText(decrypt(getEntry(fileData),currentPassword))
                    write(dialogue.viewEntry2())
                    time.sleep(0.5)
                    clear()
                    for line in entry.splitlines():
                        printText(f'{line}\n')
                        winsound.Beep(1650, 20)
                        time.sleep(0.3)
                    write(dialogue.eol())
                    print('\n\n')
                    write(dialogue.readAllEndMessage())
                else:
                    write(dialogue.errReadFile(entryToView))
                write(dialogue.continueOrExit())
                print(colors.special, end="")
                stopReadLogs, timedOut = timedInput()
    elif(instruction == "5"):
        write(dialogue.importFiles1())
        confirmImport = msvcrt.getch()
        if (confirmImport.lower() == b"y"):
            if(os.path.exists(f"{DATAFOLDER}import_{currentUser}") == False):
                os.mkdir(f"{DATAFOLDER}import_{currentUser}")
            write(dialogue.importFilesConfirm())
            confirmImport = askUser()
            if(confirmImport.lower() == "continue"):
                iter = 0
                folderFiles = updateFolderFilesImport()
                for entry in folderFiles:
                    entryNum = entry.replace(".log","")
                    with open(f"{DATAFOLDER}import_{currentUser}/{entry}", 'r', encoding="utf-8") as file:
                        writeEntryFile(currentUser,currentPassword,encrypt(file.read(),currentPassword))
                    write(dialogue.importedEntryMessage(),1)
                    iter += 1
                    winsound.Beep(1650, 20)
                inportedFiles = updateFolderFiles()
                write(dialogue.importFilesResult())
                if(os.path.exists(f"{DATAFOLDER}import_{currentUser}") == True):
                    shutil.rmtree(f"{DATAFOLDER}import_{currentUser}")
                successSound()
                write(dialogue.goBackToMain())
                getpass.getpass('')
            else:
                if(os.path.exists(f"{DATAFOLDER}import_{currentUser}") == True):
                    shutil.rmtree(f"{DATAFOLDER}import_{currentUser}")
    elif(instruction == "6"):
        write(dialogue.exportFiles1())
        confirmExport = msvcrt.getch()
        if (confirmExport.lower() == b"y"):
            folderFiles = updateFolderFiles()
            if(os.path.exists(f"{DATAFOLDER}exported_{currentUser}") == False):
                os.mkdir(f"{DATAFOLDER}exported_{currentUser}")
            iter = 0
            for entry in folderFiles:
                entryNum = entry.replace(".entry","")
                isReadable = fileStatus(entry)
                if(isReadable == 2):
                    try:
                        fileData = readEntryFile(entry)
                        entryText = toText(decrypt(getEntry(fileData),currentPassword))
                        with open(f"{DATAFOLDER}exported_{currentUser}/{entryNum}.log", 'w', encoding="utf-8") as file:
                            file.write(entryText)
                        write(dialogue.exportedEntryMessage(),1)
                        iter += 1
                    except:
                        write(dialogue.errReadFile(entry))
                        time.sleep(0.5)
                else:
                    write(dialogue.errReadFile(entry))
                    time.sleep(0.5)
                winsound.Beep(1650, 20)
            exportedFiles = next(os.walk(f"{DATAFOLDER}exported_{currentUser}"))[2]
            write(dialogue.exportFilesResult())
            successSound()
            write(dialogue.goBackToMain())
            getpass.getpass('')
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
