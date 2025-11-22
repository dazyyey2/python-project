import os
import matplotlib.pyplot as plt
import json


# Clear terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


# Lists available .txt files in the current directory
# Allows users to type a filename
# Handles file not found errors gracefully
# Processes files line-by-line (never load entire file into memory)
# Display files in current directory and get file based on user input
def get_file():
    user_input = ''
    while user_input.lower() != 'x':
        cwd = os.getcwd()
        file_path = ''
        files = os.listdir(cwd)
        txt_files = []

        # Print .txt files and filesize from current directory
        print('Files in current directory (.txt): ')
        for i in range(0, len(files), 1):
            if files[i].endswith('.txt'):
                txt_files.append(files[i])
        if len(txt_files) != 0:
            for i in range(0, len(txt_files), 1):
                print(
                    f'{txt_files[i]} : '
                    f'{os.path.getsize(txt_files[i])} bytes'
                )
        else:
            print(f'No .txt files found in current directory ({cwd})')

        # Get filename from user input
        user_input = input(
            '\nInput the name of the .txt file (Write \'x\' to cancel): '
        )
        file_path = cwd + '/' + user_input
        if os.path.exists(file_path) and user_input != '':
            return file_path
        if os.path.exists(file_path + '.txt'):
            return file_path + '.txt'
        elif user_input.lower() != 'x':
            # Ask user for valid filename after file is not found
            print('Please enter a valid filename from the current directory')

    return None  # Return None if selection was cancelled


# Basic statistics: bar chart of text composition and pie chart of
# character types
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

    # Go through file line-by-line and save basic statistics in dictionary
    try:
        with open(file, 'r', encoding='utf-8') as file_stream:
            line = file_stream.readline()  # Read first line of the file
            while line != '':
                # Create separate variable without newline and blankspace
                line_filtered = line.strip()
                line_counter += 1

                statistics['total_words'] += len(line.split())
                statistics['total_characters'] += len(line)
                line_filtered = line_filtered.replace(' ', '')
                statistics['total_characters_no_spaces'] += len(line_filtered)

                line = file_stream.readline()
    except Exception as e:
        print(f'Unknown error reading file: {e}')

    if line_counter != 0:
        statistics['total_lines'] = line_counter
        statistics['avg_words_per_line'] = round(
            statistics['total_words'] / statistics['total_lines'], 3
        )
        statistics['avg_characters_per_word'] = round(
            statistics['total_characters_no_spaces'] /
            statistics['total_words'],
            3
        )
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
    words_above_6_chars = 0

    try:
        with open(file, 'r', encoding='utf-8') as file_stream:
            line = file_stream.readline()  # Read first line of the file
            while line != '':
                # Remove newlines/blankspaces and make it lowercase
                line = line.strip().lower()
                clean_text = ''

                # Clean text by only including words (no digits etc)
                for word in line:
                    if word.isalpha() or word.isspace():
                        clean_text += word
                    else:
                        clean_text += ''

                line_filtered = clean_text.split()

                for word in line_filtered:
                    unique_words.add(word.capitalize())
                    word_lengths_duplicates.append(len(word))
                    # Count words above 6 chars (for LIX score)
                    if len(word) > 6:
                        words_above_6_chars += 1

                    # Count how many times each word duplicates and save
                    # it in common_words
                    if word.capitalize() in common_words:
                        common_words[word.capitalize()] += 1

                    else:
                        common_words[word.capitalize()] = 1

                line = file_stream.readline()
    except Exception as e:
        print(f'Unknown error reading file: {e}')

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

    # Package statistics in dictionary
    statistics = {}
    statistics['words_only_once_count'] = len(words_only_once)
    statistics['unique_words_count'] = unique_words_count
    statistics['word_lengths_unique'] = word_lengths_unique
    statistics['word_lengths_duplicates'] = word_lengths_duplicates
    statistics['words_above_6_chars'] = words_above_6_chars

    return statistics, top_10_words, unique_words


# Sentence analysis (average words per sentence, longest and shortest,
# sentence distribution)
# Average words per sentence
# • Longest and shortest sentences
# • Sentence length distribution
# Histogram of sentence lengths + bar chart of common lengths
def sentence_analysis(file):
    current_sentence = ''
    sentences = []
    sentence_stoppers = ['.', '?', '!']
    avg_words_per_sentence = 0
    total_words = 0

    try:
        with open(file, 'r', encoding='utf-8') as file_stream:
            line = file_stream.readline()  # Read first line of the file
            while line != '':
                # Count total words
                for word in line.split():
                    total_words += 1
                # Split line into sentences
                for char in line:
                    current_sentence += char
                    if char in sentence_stoppers:
                        sentence = current_sentence.strip()
                        # If there are more than 2 words in the sentence
                        # add it, otherwise skip
                        if len(sentence.split()) >= 2:
                            # If sentence isn't empty and is not something
                            # like ..
                            if (
                                sentence != '' and
                                sentence not in sentence_stoppers
                            ):
                                sentences.append(sentence)
                        current_sentence = ''

                line = file_stream.readline()
    except Exception as e:
        print(f'Unknown error reading file: {e}')

    if len(sentences) != 0:
        avg_words_per_sentence = total_words / len(sentences)
    else:
        print('No sentences found in file.')

    # Count characters per sentence
    sentence_char_length = []
    for i in sentences:
        sentence_char_length.append(len(i) - 1)
    # Put the sentence and wordcount into tuple
    sentence_lengths = []
    for sentence in sentences:
        sentence_lengths.append((len(sentence.split()), sentence.split()))

    # Find shortest and longest sentence
    shortest_sentence = []
    longest_sentence = []
    min_sentence_length = 0
    max_sentence_length = 0
    for length, words in sentence_lengths:
        if min_sentence_length == 0 or length < min_sentence_length:
            min_sentence_length = length
            shortest_sentence = words
        if max_sentence_length == 0 or length > max_sentence_length:
            max_sentence_length = length
            longest_sentence = words
    # Get only the length of sentences
    only_lengths = []
    for lengths, words in sentence_lengths:
        only_lengths.append(lengths)
    # 10 most common lengths
    top_10_sentences = {}
    lengths_counted = {}
    for length in only_lengths:
        if length in lengths_counted:
            lengths_counted[length] += 1
        else:
            lengths_counted[length] = 1
    counter = 0
    for length in sorted(
        lengths_counted, key=lengths_counted.get, reverse=True
    ):
        if counter < 10:
            top_10_sentences[length] = lengths_counted[length]
        counter += 1
    # Convert longest and shortest senteces to strings
    longest_sentence_str = ''
    for word in longest_sentence:
        longest_sentence_str += word + ' '
    shortest_sentence_str = ''
    for word in shortest_sentence:
        shortest_sentence_str += word + ' '
    # Package data
    statistics = {}
    statistics['top_10_sentence_lengths'] = top_10_sentences
    statistics['sentence_lengths'] = sentence_lengths
    statistics['only_lengths'] = only_lengths
    statistics['shortest_sentence'] = shortest_sentence
    statistics['shortest_sentence_str'] = shortest_sentence_str
    statistics['longest_sentence'] = longest_sentence
    statistics['longest_sentence_str'] = longest_sentence_str
    statistics['avg_words_per_sentence'] = avg_words_per_sentence

    return statistics


# Character Analysis:
# • Letter frequency distribution
# • Punctuation statistics
# • Case distribution (uppercase vs lowercase)
# Bar chart of most common letters + pie chart of character types
def character_analysis(file):
    letter_counts = {}
    punctuation_counts = {}
    sentence_stoppers = ['.', '?', '!']
    total_upper = 0
    total_lower = 0
    total_digits = 0
    total_spaces = 0
    total_chars = 0
    try:
        with open(file, 'r', encoding='utf-8') as file_stream:
            for line in file_stream:
                for char in line:
                    total_chars += 1
                    if char.isalpha():
                        if letter_counts.get(char.lower()):
                            letter_counts[char.lower()] += 1
                        else:
                            letter_counts[char.lower()] = 1
                        if char.isupper():
                            total_upper += 1
                        else:
                            total_lower += 1
                    elif char.isdigit():
                        total_digits += 1
                    elif char.isspace():
                        total_spaces += 1
                    elif char in sentence_stoppers:
                        if punctuation_counts.get(char):
                            punctuation_counts[char] += 1
                        else:
                            punctuation_counts[char] = 1
    except Exception as e:
        print(f'Unknown error reading file: {e}')

    # Extract most common letters
    sorted_letters = {}
    counter = 0
    for letter in sorted(letter_counts, key=letter_counts.get, reverse=True):
        if counter < 12:
            sorted_letters[letter] = letter_counts[letter]
        counter += 1

    total_letters = sum(letter_counts.values())
    total_punct = sum(punctuation_counts.values())
    # Any other chars (like %&¤ etc)
    other_chars = total_chars - (
        total_letters + total_punct + total_digits + total_spaces
    )

    # Package data
    statistics = {}
    statistics['total_letters'] = total_letters
    statistics['letter_counts'] = letter_counts
    statistics['punctuation_counts'] = punctuation_counts
    statistics['total_upper'] = total_upper
    statistics['total_lower'] = total_lower
    statistics['total_digits'] = total_digits
    statistics['total_spaces'] = total_spaces
    statistics['total_chars'] = total_chars
    statistics['total_punctuations'] = total_punct
    statistics['other_chars'] = other_chars

    return statistics, sorted_letters


def calculate_lix(file):
    # Total words
    o = get_basic_statistics(file)['total_words']
    # Total sentences
    m = len(sentence_analysis(file)['sentence_lengths'])
    # Amount of words above 6 characters (access statistics dict from tuple
    # with [0])
    l = word_analysis(file)[0]['words_above_6_chars']

    LIX = (o / m) + ((l * 100) / o)
    return round(LIX, 1)


def export_statistics(file_to_analyse, comprehensive=False, json_export=False):
    cwd = os.getcwd()
    file_name = ''

    print('Exporting...')

    basic_statistics = get_basic_statistics(file_to_analyse)
    word_analysis_stats, top_words, unique_words = word_analysis(
        file_to_analyse
    )
    sentence_analysis_statistics = sentence_analysis(file_to_analyse)
    char_analysis_stats, sorted_letters = character_analysis(file_to_analyse)
    lix = calculate_lix(file_to_analyse)

    if comprehensive:
        file_name = 'comprehensive_export'
    else:
        file_name = 'normal_export'

    if json_export:
        file_name += '.json'
    else:
        file_name += '.txt'

    if os.path.exists(cwd + '/' + file_name):
        print(
            f'Prevented overwriting. {file_name} already exists, please '
            'rename or remove it.'
        )
        return

    if comprehensive:
        # Comprehensive report, text file
        if not json_export:
            try:
                with open(file_name, 'w', encoding='utf-8') as file_stream:
                    file_stream.write('===== Basic Statistics =====\n')
                    for key in basic_statistics.keys():
                        file_stream.write(f'{key} : {basic_statistics[key]}\n')
                    file_stream.write(f'LIX: {str(lix)}')

                    file_stream.write('\n===== Word Analysis =====\n')
                    for key in word_analysis_stats.keys():
                        file_stream.write(
                            f'{key} : {word_analysis_stats[key]}\n'
                        )
                    file_stream.write('----- Top 10 words -----\n')
                    for key in top_words.keys():
                        file_stream.write(
                            f'{key} appears {top_words[key]} times\n'
                        )
                    file_stream.write('----- List of unique words -----\n')
                    for word in unique_words:
                        file_stream.write(f'{word}, ')

                    file_stream.write('\n\n===== Sentence Analysis =====\n')
                    for key in sentence_analysis_statistics.keys():
                        file_stream.write(
                            f'{key} : {sentence_analysis_statistics[key]}\n'
                        )

                    file_stream.write('\n===== Character Analysis =====\n')
                    for key in char_analysis_stats.keys():
                        file_stream.write(
                            f'{key} : {char_analysis_stats[key]}\n'
                        )
                    file_stream.write('----- Top 12 Letters -----\n')
                    for letter in sorted_letters.keys():
                        file_stream.write(
                            f'{letter} appears {sorted_letters[letter]} times\n'
                        )
            except Exception as e:
                print(f'Error exporting text file: {e}')
                return
        # Comprehensive report, JSON
        else:
            try:
                json_export_dict = {}

                json_export_dict['basic_statistics'] = basic_statistics
                json_export_dict['LIX_score'] = lix
                json_export_dict['word_analysis'] = word_analysis_stats
                json_export_dict['top_10_words'] = top_words
                json_export_dict['sentence_stats'] = sentence_analysis_statistics
                json_export_dict['char_stats'] = char_analysis_stats
                json_export_dict['sorted_letters'] = sorted_letters

                with open(file_name, 'w', encoding='utf-8') as json_fs:
                    json.dump(
                        json_export_dict,
                        json_fs,
                        indent=4,
                        ensure_ascii=False
                    )

            except Exception as e:
                print(f'Error exporting JSON: {e}')
                return
    else:
        # Normal report, text file
        if not json_export:
            try:
                with open(file_name, 'w', encoding='utf-8') as file_stream:
                    file_stream.write('===== Basic Statistics =====\n')
                    for key in basic_statistics.keys():
                        file_stream.write(f'{key} : {basic_statistics[key]}\n')
                    file_stream.write(f'LIX: {str(lix)}')

                    file_stream.write('\n===== Word Analysis =====\n')
                    for key in word_analysis_stats.keys():
                        # Don't include these in simple report
                        if key not in (
                            'word_lengths_unique', 'word_lengths_duplicates'
                        ):
                            file_stream.write(
                                f'{key} : {word_analysis_stats[key]}\n'
                            )
                    file_stream.write('----- Top 10 words -----\n')
                    for key in top_words.keys():
                        file_stream.write(
                            f'{key} appears {top_words[key]} times\n'
                        )

                    file_stream.write('\n\n===== Sentence Analysis =====\n')
                    for key in sentence_analysis_statistics.keys():
                        # Don't include these in simple report
                        if key not in (
                            'sentence_lengths', 'only_lengths',
                            'longest_sentence', 'shortest_sentence'
                        ):
                            file_stream.write(
                                f'{key} : {sentence_analysis_statistics[key]}\n'
                            )

                    file_stream.write('\n===== Character Analysis =====\n')
                    for key in char_analysis_stats.keys():
                        file_stream.write(
                            f'{key} : {char_analysis_stats[key]}\n'
                        )
                    file_stream.write('----- Top 12 Letters -----\n')
                    for letter in sorted_letters.keys():
                        file_stream.write(
                            f'{letter} appears {sorted_letters[letter]} times\n'
                        )
            except Exception as e:
                print(f'Error exporting text file: {e}')
                return
        # Normal report, JSON
        else:
            try:
                json_export_dict = {}
                word_analysis_statistics_filtered = {}
                sentence_analysis_statistics_filtered = {}

                for key in word_analysis_stats:
                    if key not in (
                        'word_lengths_unique', 'word_lengths_duplicates'
                    ):
                        word_analysis_statistics_filtered[key] = (
                            word_analysis_stats[key]
                        )
                for key in sentence_analysis_statistics:
                    if key not in (
                        'sentence_lengths', 'only_lengths',
                        'longest_sentence', 'shortest_sentence'
                    ):
                        sentence_analysis_statistics_filtered[key] = (
                            sentence_analysis_statistics[key]
                        )

                json_export_dict['basic_statistics'] = basic_statistics
                json_export_dict['LIX_score'] = lix
                json_export_dict['word_analysis'] = (
                    word_analysis_statistics_filtered
                )
                json_export_dict['top_10_words'] = top_words
                json_export_dict['sentence_stats'] = (
                    sentence_analysis_statistics_filtered
                )
                json_export_dict['char_stats'] = char_analysis_stats
                json_export_dict['sorted_letters'] = sorted_letters

                with open(file_name, 'w', encoding='utf-8') as json_fs:
                    json.dump(
                        json_export_dict,
                        json_fs,
                        indent=4,
                        ensure_ascii=False
                    )

            except Exception as e:
                print(f'Error exporting JSON: {e}')
                return

    print(f'Export successful, {file_name} created in current directory.')
    return


# Creates and displays pie chart
def create_pie_chart(labels, sizes, title=''):
    plt.subplots(figsize=(10, 6))

    colors = ['#4D6DA1', '#55A868', '#C44E52', '#8172B2', '#CCB974']

    wedges, texts, autotexts = plt.pie(
        sizes,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'black', 'linewidth': 0.8},
        pctdistance=1.12
    )

    plt.legend(wedges, labels, title='Categories', loc='center left')

    plt.title(title, fontsize=16, fontweight='bold', pad=15)
    plt.axis('equal')
    plt.show()


# Creates and displays bar graph
def create_bar_graph(
    labels, sizes, title='', x_label='', y_label='',
    textbox_text='', textbox_left=False, text_rotation=True
):
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = ['#4D6DA1', '#55A868', '#C44E52', '#8172B2', '#CCB974']

    bars = plt.bar(
        labels, sizes, color=colors, edgecolor='black', linewidth=0.8
    )
    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f'{bar.get_height()}',
            ha='center', va='bottom', fontsize=10
        )

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
    if textbox_left:
        ax.text(
            0.05, 0.95, textbox_text, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', horizontalalignment='left', bbox=props
        )
    else:
        ax.text(
            0.95, 0.95, textbox_text, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', horizontalalignment='right', bbox=props
        )

    if text_rotation:
        # Rotate xlabel text 20 degrees to make sure the text doesn't overlap
        plt.xticks(rotation=20, ha='right')

    ax.grid(True, linestyle='--', alpha=0.6)
    plt.title(title, fontsize=16, fontweight='bold', pad=15)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.tight_layout()
    plt.show()


# Creates and displays bar graph
def create_histogram(
    data, bins, title='', x_label='', y_label='',
    textbox_text='', textbox_left=False
):
    fig, ax = plt.subplots(figsize=(10, 6))

    color = '#CE882C'
    n, bins_edges, patches = plt.hist(
        data, bins=bins, color=color, edgecolor='black', linewidth=0.8
    )

    for i in range(0, len(patches), 1):
        height = n[i]
        x_pos = patches[i].get_x() + patches[i].get_width() / 2
        ax.text(
            x_pos, height, f'{int(height)}',
            ha='center', va='bottom', fontsize=10
        )

    # Create textbox
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
    if textbox_left:
        ax.text(
            0.05, 0.95, textbox_text, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', horizontalalignment='left', bbox=props
        )
    else:
        ax.text(
            0.95, 0.95, textbox_text, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', horizontalalignment='right', bbox=props
        )

    ax.grid(True, linestyle='--', alpha=0.6)
    plt.title(title, fontsize=16, fontweight='bold', pad=15)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.tight_layout()
    plt.show()


# Handle user choices from the menu
def handle_choices(choice, state):
    match choice.lower():
        # LOAD FILE
        case '1':
            clear_terminal()
            state['current_file'] = get_file()
            if state.get('current_file'):
                print('\nFile loaded sucessfully!')
            else:
                print('\nFile selection was canceled.')
        # BASIC STATISTICS
        case '2':
            # If a file has been loaded, fetch basic statistics; print it
            # and show a bar graph
            if state.get('current_file'):
                clear_terminal()
                statistics = get_basic_statistics(state['current_file'])
                lix = calculate_lix(state['current_file'])

                # Create bar graph of basic statistics and LIX
                labels = [
                    'Lines', 'Words', 'Characters (w/ spaces)',
                    'Characters (no spaces)'
                ]
                sizes = [
                    statistics['total_lines'],
                    statistics['total_words'],
                    statistics['total_characters'],
                    statistics['total_characters_no_spaces']
                ]
                create_bar_graph(
                    labels,
                    sizes,
                    'Basic Statistics\n' + state['current_file'],
                    textbox_text=(
                        f"Average words per line: "
                        f"{statistics['avg_words_per_line']}\n"
                        f"Average characters per word: "
                        f"{statistics['avg_characters_per_word']}\n"
                        f"LIX score: {lix}"
                    ),
                    textbox_left=True
                )
            else:
                print('Please load a file first.')
        # WORD FREQUENCY ANALYSIS
        case '3':
            if state.get('current_file'):
                clear_terminal()
                statistics, top_10_words, unique_words = word_analysis(
                    state['current_file']
                )

                create_bar_graph(
                    top_10_words.keys(),
                    top_10_words.values(),
                    'Top 10 Words\n' + state['current_file'],
                    textbox_text=(
                        f"{statistics['unique_words_count']} unique words\n"
                        f"{statistics['words_only_once_count']} "
                        f"words only appear once"
                    )
                )
                create_histogram(
                    statistics['word_lengths_unique'],
                    bins=10,
                    title='Word length distribution\n' + state['current_file']
                )
            else:
                print('Please load a file first.')
        # SENTENCE ANALYSIS
        case '4':
            if state.get('current_file'):
                clear_terminal()
                statistics = sentence_analysis(state['current_file'])

                print(
                    f"Longest sentence: "
                    f"{statistics['longest_sentence_str']}\n"
                )
                print(
                    f"Shortest sentence: "
                    f"{statistics['shortest_sentence_str']}\n"
                )

                keys_as_strings = []
                for i in statistics['top_10_sentence_lengths'].keys():
                    keys_as_strings.append(str(i))

                create_histogram(
                    statistics['only_lengths'],
                    bins=10,
                    title=(
                        'Sentence length distribution\n' +
                        state['current_file']
                    ),
                    textbox_text=(
                        f"Average words per sentence: "
                        f"{round(statistics['avg_words_per_sentence'], 3)}\n"
                        f"Longest sentence: "
                        f"{len(statistics['longest_sentence'])} "
                        f"(Printed in terminal)\n"
                        f"Shortest sentence: "
                        f"{len(statistics['shortest_sentence'])} "
                        f"(Printed in terminal)"
                    )
                )
                create_bar_graph(
                    keys_as_strings,
                    statistics['top_10_sentence_lengths'].values(),
                    title=(
                        'Top 10 Lengths of Sentences\n' +
                        state['current_file']
                    ),
                    x_label='Sentence Length',
                    y_label='Amount',
                    text_rotation=False
                )
            else:
                print('Please load a file first.')
        # CHARACTER ANALYSIS
        case '5':
            if state.get('current_file'):
                clear_terminal()
                statistics, sorted_letters = character_analysis(
                    state['current_file']
                )

                create_bar_graph(
                    sorted_letters.keys(),
                    sorted_letters.values(),
                    title=f"Top 12 Letters\n{state['current_file']}",
                    x_label='Letters',
                    y_label='Amount',
                    textbox_text=(
                        f"Total letters: {statistics['total_letters']}\n"
                        f"Uppercase: {statistics['total_upper']}\n"
                        f"Lowercase: {statistics['total_lower']}"
                    ),
                    text_rotation=False
                )

                labels = [
                    'Letters', 'Punctuation', 'Digits', 'Spaces', 'Other'
                ]
                sizes = [
                    statistics['total_letters'],
                    statistics['total_punctuations'],
                    statistics['total_digits'],
                    statistics['total_spaces'],
                    statistics['other_chars']
                ]
                create_pie_chart(
                    labels,
                    sizes,
                    title=f"Character Type Distribution\n"
                    f"{state['current_file']}"
                )
            else:
                print('Please load a file first.')
        # EXPORT
        case '6':
            if state.get('current_file'):
                clear_terminal()
                user_input = input(
                    'Do you want a comprehensive report?\n'
                    '1. Comprehensive\n2. Normal\n'
                )
                if user_input == '1' or user_input.lower() == 'comprehensive':
                    clear_terminal()
                    user_input = input(
                        'Do you want the report as JSON or text file?\n'
                        '1. JSON\n2. Text\n'
                    )
                    if user_input == '2' or user_input.lower() == 'text':
                        export_statistics(
                            state['current_file'], comprehensive=True
                        )
                    elif user_input == '1' or user_input.lower() == 'json':
                        export_statistics(
                            state['current_file'],
                            comprehensive=True,
                            json_export=True
                        )
                    else:
                        print('Please enter a valid choice.')
                elif user_input == '2' or user_input.lower() == 'normal':
                    clear_terminal()
                    user_input = input(
                        'Do you want the report as JSON or text file?\n'
                        '1. JSON\n2. Text\n'
                    )
                    if user_input == '2' or user_input.lower() == 'text':
                        export_statistics(state['current_file'])
                    elif user_input == '1' or user_input.lower() == 'json':
                        export_statistics(
                            state['current_file'], json_export=True
                        )
                    else:
                        print('Please enter a valid choice.')
                else:
                    print('Please enter a valid choice.')

            else:
                print('Please load a file first.')
        case 'x':
            return state, True  # Exit program loop
        case _:
            print('Please enter a valid choice.')
    return state, False  # Continue program loop


# Print menu
def print_menu(state):
    # Load a text file
    # Display basic statistics (with visualisation)
    # Show word frequency analysis (with visualisation)
    # Display sentence analysis (with visualisation)
    # Display character analysis (with visualisation)
    # Export results
    # Exit programme
    print('--------------------------------')
    print('1. Load a text file')
    print('2. Display basic statistics')
    print('3. Display word frequency analysis')
    print('4. Display sentence analysis')
    print('5. Display character analysis')
    print('6. Export results')
    print('x. Exit programme')
    print('--------------------------------')
    if state.get('current_file'):
        print(f"Loaded file: {state['current_file']}")
    else:
        print('No file loaded.')
    print('--------------------------------')
    user_input = input('Please enter choice: ')
    return user_input  # Returns user choice


state = {}
exit_boolean = False
while not exit_boolean:  # Program loop
    user_choice = print_menu(state)
    state, exit_boolean = handle_choices(user_choice, state)


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
