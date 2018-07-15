from tabulate import tabulate


def print_metadata(metadata):
    '''
    prints basic info about the chat
    '''
    print('First message: ' + metadata['first_day_date'])
    print('Last message: ' + metadata['last_day_date'])
    print('Number of days: ' + str(metadata['days']))
    print('Number of messages: ' + str(metadata['nmessages']))


def print_user_info(users):
    '''
    prints basic info about users and their messages
    '''

    print('\n')
    print('Number of messages:')
    for user in users:
        print('\t' + user + '(' + users[user]['gender'] + '): ')
        print('\t\t' + 'Messages: ' + str(users[user]['n_messages']))
        print('\t\t' + 'Most common word: ' +
              str(users[user]['most_common_word']))
        print('\t\t' + 'MPD: ' + str(users[user]['mpd']))
        print('\t\t' + 'Files sent: ' + str(users[user]['n_files']))
        print('\t\t' + 'Files sent every 100 messages: ' +
              str(round(users[user]['ratio_files_and_messages'], 2)) + " %")

        print('\t\t' + 'Links sent: ' + str(users[user]['n_links']))
        print('\t\t' + 'Links sent every 100 messages: ' +
              str(round(users[user]['ratio_links_and_messages'], 2)) + " %")

        print('\n')


def print_longest_messages(users):
    '''
    prints the length and the message of the longest message for every user 
    '''

    print('********* LONGEST MESSAGES *********\n')
    for user in users:
        print(user + " (" + str(users[user]['len_longest_message']) + '): ')
        print("\t" + users[user]['longest_message'] + "\n\n")
    print('\n\n')


def print_info_table(users):
    '''
    prints a table with short and basic info about users
    '''

    rows = []
    for user in users:
        rows.append([
            user,
            users[user]['gender'],
            str(users[user]['n_messages']),
            str(users[user]['most_common_word']),
            str(users[user]['len_longest_message']),
            str(users[user]['n_emojis']),
            str(round(users[user]['mpd'], 4)),
            str(users[user]['n_files']),
            str(round(users[user]['ratio_files_and_messages'], 2)),
            str(users[user]['n_links']),
            str(round(users[user]['ratio_links_and_messages'], 2))
        ])

    headers = [
        'User', 'Gender', 'Messages', 'MCM', 'LM', 'Emojis', 'MPD', 'Files', '% Files', 'Links', '% Links'
    ]
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    print('\n\tMCM: Most common word.')
    print('\tLM: Longest message (length). Just below you can see the message for every user.')
    print('\tMPD: Messages per day.')
    print('\t% Files and % Links: Files and/or links sent every 100 messages.\n\n')

    print_longest_messages(users)
