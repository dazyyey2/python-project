import os
import matplotlib.pyplot as plt

#Lists available .txt files in the current directory
#Allows users to type a filename
#Handles file not found errors gracefully
#Processes files line-by-line (never load entire file into memory)

#Display files in current directory and get file based on user input
def get_file():
    user_input = ''
    while(user_input.lower() != 'x'):
        cwd = os.getcwd()
        file_path = ''
        files = os.listdir(cwd)
        txt_files = []
        
        #Print .txt files and filesize from current directory
        print('Files in current directory (.txt): ')
        for i in range(0, len(files), 1):
            if files[i].endswith('.txt'):
                txt_files.append(files[i])
        if len(txt_files) != 0:
            for i in range(0, len(txt_files), 1):
                print(f'{txt_files[i]} : {os.path.getsize(txt_files[i])} bytes')
        else:
            print(f'No .txt files found in current directory ({cwd})')    
        
        user_input = input('\nInput the name of the .txt file (Write \'x\' to cancel): ') #Get filename from user input
        file_path = cwd + '/' + user_input
        if os.path.exists(file_path):
            return file_path
        if os.path.exists(file_path + '.txt'):
            return file_path + '.txt'
        elif user_input.lower() != 'x':
            print('Please enter a valid filename from the current directory') #Ask user for valid filename after file is not found
    return None #Return None if selection was cancelled
        
# Total number of lines
# Total number of words
# Total number of characters (with and without spaces)
# Average words per line
# Average characters per word
def get_basic_statistics(file):
    lineCounter = 0
    charDictionary = {}
    
    with open(file, 'r', encoding='utf-8') as file:
        line = file.readline() #Read first line of the file
        while line != '':
            lineFiltered = line.strip() #Create separate variable without newline and blankspace
            charDictionary[lineCounter] = len(lineFiltered)
            lineCounter += 1
            line = file.readline()
    create_bar_graph(charDictionary.keys(), charDictionary.values(), 'Bar graph', 'Line', 'Characters')
    totalLines = lineCounter
    



#Creates and displays bar graph
def create_bar_graph(x, y, title, x_label, y_label):

    fig, ax = plt.subplots(figsize=(8, 5)) #Create figure and axis

    colors = ["#4D6DA1", '#55A868', '#C44E52', '#8172B2', '#CCB974'] #Define colors for bars

    bars = ax.bar(x, y, color=colors, edgecolor='black', linewidth=0.8) #Create bars

    ax.set_title(title, fontsize=16, fontweight='bold', pad=15)#Title
    ax.set_xlabel(x_label, fontsize=12)#x label
    ax.set_ylabel(y_label, fontsize=12)#y label

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2 ,yval + .5, f'{yval}',ha='center', va='bottom', fontsize=10, fontweight='bold') #Create text label with y-value over bar
    
    plt.show()


    
def handle_choices(choice, state):

    match choice:
        case '1':
            state['current_file'] = get_file()
            if state['current_file'] != None:
                print('File loaded sucessfully!')
                #ReadFile(file)
            else:
                print('File selection was canceled.')
        case '2':
            if state.get('current_file'):
                get_basic_statistics(state['current_file'])
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
    
def print_menu():
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

    user_input = input('Please enter choice: ')
    return user_input #Returns user choice

state = {}
exit_boolean = False
while not exit_boolean: #Program loop
    user_choice = print_menu()
    exit_boolean = handle_choices(user_choice, state)
