import os
import matplotlib.pyplot as plt

#Clear terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
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
        if os.path.exists(file_path) and user_input != '':
            return file_path
        if os.path.exists(file_path + '.txt'):
            return file_path + '.txt'
        elif user_input.lower() != 'x':
            print('Please enter a valid filename from the current directory') #Ask user for valid filename after file is not found
        
    return None #Return None if selection was cancelled
# Basic statistics: bar chart of text composition and pie chart of character types      
# Total number of lines
# Total number of words
# Total number of characters (with and without spaces)
# Average words per line
# Average characters per word
def get_basic_statistics(file):
    line_counter = 0
    statistics = {}
    statistics['total_words'] = 0
    statistics['total_lines'] = 0
    statistics['total_characters'] = 0
    statistics['total_characters_no_spaces'] = 0
    statistics['avg_words_per_line'] = 0
    statistics['avg_characters_per_word'] = 0
    
    #Go through file line-by-line and save basic statistics in dictionary
    try:
        with open(file, 'r', encoding='utf-8') as file_stream:
            line = file_stream.readline() #Read first line of the file
            while line != '':
                line_filtered = line.strip() #Create separate variable without newline and blankspace
                line_counter += 1
                
                statistics['total_words'] += len(line.split())
                statistics['total_characters'] += len(line)
                line_filtered = line_filtered.replace(' ', '')
                statistics['total_characters_no_spaces'] += len(line_filtered)

                line = file_stream.readline()
    except:
        print('Unknown error reading file.')
    
    if line_counter != 0:
        statistics['total_lines'] = line_counter
        statistics['avg_words_per_line'] = round(statistics['total_words']/statistics['total_lines'], 3)
        statistics['avg_characters_per_word'] = round(statistics['total_characters_no_spaces']/statistics['total_words'], 3)
    else:
        print('File was empty.')
    return statistics
# Word analysis: bar chart of most common words and histogram of word lengths
# Most common words (top 10)
# • Word length distribution
# • Unique word count
# • Words appearing only once
def word_analysis(file):
    unique_words = set()
    word_lengths_unique = []
    word_lengths_duplicates = []
    unique_words_count = 0
    common_words = {}
    
    try:
        with open(file, 'r', encoding='utf-8') as file_stream:
            line = file_stream.readline() #Read first line of the file
            while line != '':
                line = line.strip().lower() #Create separate variable without newline and blankspace
                clean_text = ''
                
                #Clean text by only including words (no digits etc)
                for word in line:
                    if word.isalpha() or word.isspace():
                        clean_text += word
                    else:
                        clean_text += ''
                
                line_filtered = clean_text.split()
                
                for word in line_filtered:
                    unique_words.add(word.capitalize())
                    word_lengths_duplicates.append(len(word))
                    #Count how many times each word duplicates and save it in common_words
                    if word.capitalize() in common_words:
                        common_words[word.capitalize()] += 1

                    else:
                        common_words[word.capitalize()] = 1

                line = file_stream.readline()
    except:
        print('Unknown error reading file.')
            
    for word in unique_words:
        word_lengths_unique.append(len(word))
    
    top_10_words = {}    
    words_only_once = []
    counter = 0
    for i in sorted(common_words, key=common_words.get, reverse=True):
        if counter < 10:
            top_10_words[i] = common_words[i]
        if common_words[i] == 1:
            words_only_once.append(i)
        counter += 1
   
    unique_words_count = len(unique_words)
    
    #Package statistics in dictionary
    statistics = {}
    statistics['words_only_once_count'] = len(words_only_once)
    statistics['unique_words_count'] = unique_words_count
    statistics['word_lengths_unique'] = word_lengths_unique
    statistics['word_lengths_duplicates'] = word_lengths_duplicates

    return statistics, top_10_words, unique_words
#Creates and displays pie chart
def create_pie_chart(labels, sizes, title=''):
    plt.subplots(figsize=(8, 5))
    
    colors = ["#4D6DA1", '#55A868', '#C44E52', '#8172B2', '#CCB974']
    
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'black', 'linewidth': 0.8})
    plt.title(title, fontsize=16, fontweight='bold', pad=15)
    plt.axis('equal')
    plt.show()   
#Creates and displays bar graph
def create_bar_graph(labels, sizes, title='', x_label='', y_label='', textbox_text='', textbox_left=False):
    fig, ax = plt.subplots(figsize=(8, 5))
    
    colors = ["#4D6DA1", '#55A868', '#C44E52', '#8172B2', '#CCB974']
    
    bars = plt.bar(labels, sizes, color=colors, edgecolor='black', linewidth=0.8)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{bar.get_height()}', ha='center', va='bottom', fontsize=10)
        
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
    if textbox_left:
        ax.text(0.05, 0.95, textbox_text, transform=ax.transAxes, fontsize=14, verticalalignment='top', horizontalalignment='left', bbox=props)
    else:
        ax.text(0.95, 0.95, textbox_text, transform=ax.transAxes, fontsize=14, verticalalignment='top', horizontalalignment='right', bbox=props)
    
    ax.grid(True, linestyle='--', alpha=0.6)  
    plt.title(title, fontsize=16, fontweight='bold', pad=15)
    plt.xticks(rotation=20, ha='right') #Rotate xlabel text 20 degrees to make sure the text doesn't overlap
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.tight_layout()
    plt.show()
#Creates and displays bar graph
def create_histogram(data, bins, title='', x_label='', y_label='', textbox_text='', textbox_left=False):
    fig, ax = plt.subplots(figsize=(8, 5))
    
    color = "#CE882C"
    n, bins_edges, patches = plt.hist(data, bins=bins, color=color, edgecolor='black', linewidth=0.8)

    for i in range(0, len(patches), 1):
        height = n[i]
        x_pos = patches[i].get_x() + patches[i].get_width() / 2
        ax.text(x_pos, height, f'{int(height)}', ha='center', va='bottom', fontsize=10)
    
    #Create textbox
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
    if textbox_left:
        ax.text(0.05, 0.95, textbox_text, transform=ax.transAxes, fontsize=14, verticalalignment='top', horizontalalignment='left', bbox=props)
    else:
        ax.text(0.95, 0.95, textbox_text, transform=ax.transAxes, fontsize=14, verticalalignment='top', horizontalalignment='right', bbox=props)
    
    
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.title(title, fontsize=16, fontweight='bold', pad=15)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.tight_layout()
    plt.show()
#Handle user choices from the menu
def handle_choices(choice, state):
    match choice.lower():
        #LOAD FILE
        case '1':
            clear_terminal()
            state['current_file'] = get_file()
            if state.get('current_file'):
                print('\nFile loaded sucessfully!')
            else:
                print('\nFile selection was canceled.')
        #BASIC STATISTICS
        case '2':
            #If a file has been loaded, fetch basic statistics; print it and show a bar graph
            if state.get('current_file'):
                clear_terminal()
                statistics = get_basic_statistics(state['current_file'])
                #Print basic statistics in terminal
                print(f'\nTotal Lines: {statistics['total_lines']}')
                print(f'Total Words: {statistics['total_words']}')
                print(f'Total Characters (with spaces): {statistics['total_characters']}')
                print(f'Total Characters (without spaces): {statistics['total_characters_no_spaces']}')
                print(f'Average Words per Line: {statistics['avg_words_per_line']}')
                print(f'Average Characters per Word: {statistics['avg_characters_per_word']}\n')
                
                #Create bar graph of basic statistics
                labels = ['Lines', 'Words', 'Characters (w/ spaces)', 'Characters (no spaces)']
                sizes = [statistics['total_lines'], statistics['total_words'], statistics['total_characters'], statistics['total_characters_no_spaces']]
                create_bar_graph(labels, sizes, 'Basic Statistics\n' + state['current_file'],
                                 textbox_text=f'Average words per line: {statistics['avg_words_per_line']}\nAverage characters per word: {statistics['avg_characters_per_word']}',
                                 textbox_left=True)
            else:
                print('Please load a file first.')
        #WORD FREQUENCY ANALYSIS
        case '3':
            if state.get('current_file'):
                clear_terminal()
                statistics_dictionary, top_10_words, unique_words = word_analysis(state['current_file'])
                
                create_bar_graph(top_10_words.keys(), top_10_words.values(), 'Top 10 words\n' + state['current_file'], 
                                 textbox_text=f'{statistics_dictionary['unique_words_count']} Unique words\n{statistics_dictionary['words_only_once_count']} Words only appear once')
                create_histogram(statistics_dictionary['word_lengths_unique'], bins=10, title='Word length distribution\n' + state['current_file'])
            else:
                print('Please load a file first.')
        #SENTENCE ANALYSIS 
        case '4':
            print('todo')
        #CHARACTER ANALYSIS
        case '5':
            print('todo')
        #EXPORT
        case '6':
            print('todo')
        case 'x':
            return True #Exit program loop
        case _:
            print('Please enter a valid choice.')
    return False #Continue program loop
#Print menu 
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


# Dictionaries for counting words
# Lists for lengths
# Sets for unique words

# Basic statistics (number of lines, words, characters; average words per
# line, characters per word)
# ‣ Word analysis (top 10 words, word length distribution, unique words,
# words only appearing once)
# ‣ Sentence analysis (average words per sentence, longest and shortest,
# sentence distribution)
# ‣ Character analysis (letter frequency distribution, punctuation statistics,
# case distribution)