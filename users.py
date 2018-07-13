import re
import requests

from tabulate import tabulate


def get_users(content):
    users = {}
    regex = '\d\d:\d\d\s-\s(.*?):\s'
    for x in content:
        x = x.rstrip()
        user = re.findall(regex, x)
        if len(user) == 1:
            if not user[0] in users and not user[0] == []:
                users[user[0]] = {}
    return users


def get_gender(name):
    url = 'https://api.genderize.io/?name=' + name
    r = requests.get(url=url)
    if r.json()['gender'] is None:
        return 'Not identified'
    return r.json()['gender']


def get_messages(content, user):
    messages = []
    regex = user + ': (.*)'

    for x in content:
        x = x.rstrip()
        msg = re.findall(regex, x)
        if(len(msg) != 0):
            messages.append(msg[0])
    return messages


def get_nfiles(messages):
    n = 0
    for msg in messages:
        if msg == '<Archivo omitido>':
            n += 1
    return n

# Get the number of elem(files or links) sent every 100 messages


def get_ratio(n_messages, elem):
    return elem * 100 / n_messages

# Get the most common word of a user


def get_most_common_words(messages):
    words = []
    for x in messages:
        for y in x.split(' '):
            words.append(y)
    return max(set(words), key=words.count)


def get_nlinks(messages):
    n_links = 0
    for m in messages:
        n = re.findall(
            'http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[\/.?&+!*=\-])+(?![^,!;:\s)])', m)
        n_links = n_links + len(n)
    return n_links


def get_mpd(n, days):
    return n / days


def print_info(users):
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


def print_info_pretty(users):
    all_users = []
    for user in users:
        all_users.append([
            user,
            users[user]['gender'],
            str(users[user]['n_messages']),
            str(users[user]['most_common_word']),
            str(round(users[user]['mpd'], 4)),
            str(users[user]['n_files']),
            str(round(users[user]['ratio_files_and_messages'], 2)),
            str(users[user]['n_links']),
            str(round(users[user]['ratio_links_and_messages'], 2))
        ])

    headers = [
        'User', 'Gender', 'Messages', 'MCM', 'MPD', 'Files', '% Files', 'Links', '% Links'
    ]
    print(tabulate(all_users, headers=headers, tablefmt="grid"))
    print('\n\tMCM: Most common word.')
    print('\tMPD: Messages per day.')
    print('\% Files and % Links: Files and/or links sent every 100 messages.\n')


def main(content, metadata):
    users = get_users(content)
    for user in users:
        gender = get_gender(user)
        messages = get_messages(content, user)
        n_messages = len(messages)
        if(n_messages == 0):
            n_files = ratio_files_and_messages = 0
            most_common_words = ''
            n_links = 0
            mpd = 0
        else:
            most_common_words = get_most_common_words(messages)

            n_files = get_nfiles(messages)
            ratio_files_and_messages = get_ratio(n_messages, n_files)

            n_links = get_nlinks(messages)
            ratio_links_and_messages = get_ratio(n_messages, n_links)

            mpd = get_mpd(n_messages, metadata['days'])

        users[user] = {
            'gender': gender,
            'messages': messages,
            'n_messages': n_messages,
            'most_common_word': most_common_words,
            'n_files': n_files,
            'ratio_files_and_messages': ratio_files_and_messages,
            'n_links': n_links,
            'ratio_links_and_messages': ratio_links_and_messages,
            'mpd': mpd
        }

    print_info_pretty(users)
