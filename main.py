import os
import matplotlib.pyplot as plt

#Lists available .txt files in the current directory
#Allows users to type a filename
#Handles file not found errors gracefully
#Processes files line-by-line (never load entire file into memory)

#Display files in current directory and get file based on user input
def GetFile():
    userInput = ''
    while(userInput.lower() != 'x'):
        cwd = os.getcwd()
        filePath = ''
        files = os.listdir(cwd)
        txtFiles = []
        
        #Print .txt files and filesize from current directory
        print('Files in current directory (.txt): ')
        for i in range(0, len(files), 1):
            if files[i].endswith('.txt'):
                txtFiles.append(files[i])
        if len(txtFiles) != 0:
            for i in range(0, len(txtFiles), 1):
                print(f'{txtFiles[i]} : {os.path.getsize(txtFiles[i])} bytes')
        else:
            print(f'No .txt files found in current directory ({cwd})')    
        
        userInput = input('\nInput the name of the .txt file (Write \'x\' to cancel): ') #Get filename from user input
        filePath = cwd + '/' + userInput
        if os.path.exists(filePath):
            return filePath
        if os.path.exists(filePath + '.txt'):
            return filePath + '.txt'
        elif userInput.lower() != 'x':
            print('Please enter a valid filename from the current directory') #Ask user for valid filename after file is not found
    return None #Return None if selection was cancelled
        
        # ------ OLD ---------
        # userInput = input('\nInput the name of the .txt file (Write \'x\' to cancel): ') #Get filename from user input
        # try:
        #     fullFile = open(cwd + '/' + userInput , 'r', encoding='utf-8') #Open selected file
        #     return fullFile
        # except FileNotFoundError:
        #     try:
        #         fullFile = open(cwd + '/' + userInput + '.txt', 'r', encoding='utf-8') #Test user input with .txt extension if file was not found
        #         return fullFile
        #     except FileNotFoundError:
        #         print('Please enter a valid filename from the current directory') #Ask user for valid filename after file is not found
        # except:
        #     print('Unspecified error opening file.')

#Read file line-by-line
# def ReadFile(file):
#     line = file.readline() #Read first line of the file
#     lineCounter = 0
#     charDictionary = {}
#     while line != '':
#         lineFiltered = line.strip() #Create separate variable without newline and blankspace
#         charDictionary[lineCounter] = len(lineFiltered)
#         lineCounter += 1
#         line = file.readline()
    
#     CreateBarGraph(charDictionary.keys(), charDictionary.values(), 'Bar graph', 'Line', 'Characters')

# Total number of lines
# Total number of words
# Total number of characters (with and without spaces)
# Average words per line
# Average characters per word
def GetBasicStatistics(file):
    lineCounter = 0
    charDictionary = {}
    
    with open(file, 'r', encoding='utf-8') as file:
        line = file.readline() #Read first line of the file
        while line != '':
            lineFiltered = line.strip() #Create separate variable without newline and blankspace
            charDictionary[lineCounter] = len(lineFiltered)
            lineCounter += 1
            line = file.readline()
    CreateBarGraph(charDictionary.keys(), charDictionary.values(), 'Bar graph', 'Line', 'Characters')
    totalLines = lineCounter
    



#Creates and displays bar graph
def CreateBarGraph(x, y, title, xLabel, yLabel):

    fig, ax = plt.subplots(figsize=(8, 5)) #Create figure and axis

    colors = ["#4D6DA1", '#55A868', '#C44E52', '#8172B2', '#CCB974'] #Define colors for bars

    bars = ax.bar(x, y, color=colors, edgecolor='black', linewidth=0.8) #Create bars

    ax.set_title(title, fontsize=16, fontweight='bold', pad=15)#Title
    ax.set_xlabel(xLabel, fontsize=12)#x label
    ax.set_ylabel(yLabel, fontsize=12)#y label

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2 ,yval + .5, f'{yval}',ha='center', va='bottom', fontsize=10, fontweight='bold') #Create text label with y-value over bar
    
    plt.tight_layout()
    plt.show()


    
def HandleChoices(choice, state):

    match choice:
        case '1':
            state['currentFile'] = GetFile()
            if state['currentFile'] != None:
                print('File loaded sucessfully!')
                #ReadFile(file)
            else:
                print('File selection was canceled.')
        case '2':
            if state.get('currentFile'):
                GetBasicStatistics(state['currentFile'])
            else:
                print('Please load a file first.')
        case '3':
            print('todo')
        case '4':
            print('todo')
        case '5':
            print('todo')
        case '6':
            print('todo')
        case 'x':
            return True #Exit program loop
        case _:
            print('Please enter a valid choice.')
    return False #Continue program loop
    
def PrintMenu():
#Load a text file
#Display basic statistics (with visualisation)
#Show word frequency analysis (with visualisation)
#Display sentence analysis (with visualisation)
#Display character analysis (with visualisation)
#Export results
#Exit programme
    print('1. Load a text file')
    print('2. Display basic statistics (with visualisation)')
    print('3. Show word frequency analysis (with visualisation)')
    print('4. Display sentence analysis (with visualisation)')
    print('5. Display character analysis (with visualisation)')
    print('6. Export results')
    print('x. Exit programme')

    userInput = input('Please enter choice: ')
    return userInput #Returns user choice

state = {}
exitBoolean = False
while not exitBoolean: #Program loop
    userChoice = PrintMenu()
    exitBoolean = HandleChoices(userChoice, state)
