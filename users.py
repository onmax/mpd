import re
import requests


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

# Get the number of files sent every 100 messages


def get_ratio_files_and_messages(n_messages, n_files):
    return n_files * 100 / n_messages

# Get the most common word of a user


def get_most_common_words(messages):
    words = []
    for x in messages:
        for y in x.split(' '):
            words.append(y)
    return max(set(words), key=words.count)


def get_nlinks(messages):
    nlinks = 0
    for m in messages:
        n = re.findall(
            'http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[\/.?&+!*=\-])+(?![^,!;:\s)])', m)
        nlinks = nlinks + len(n)
    return nlinks


def print_info(users):
    print('\n')
    print('Number of messages:')
    for user in users:
        print('\t' + user + '(' + users[user]['gender'] + '): ' + str(users[user]['n_messages']) +
              ". Most common message: " + users[user]['most_common_word'])

    print('\n')
    print('Number of files sent:')
    for user in users:
        print('\t' + user + ': ' + str(users[user]['n_files']) +
              '. Ratio: ' +
              str(round(users[user]['ratio_files_and_messages'], 2)) + " %")

    print('\n')

    print('Number of links sent:')
    for user in users:
        print('\t' + user + ': ' + str(users[user]['nlinks']))

    print('\n')


def main(content):
    users = get_users(content)
    for user in users:
        gender = get_gender(user)
        messages = get_messages(content, user)
        n_messages = len(messages)
        if(n_messages == 0):
            n_files = ratio_files_and_messages = 0
            most_common_words = ''
            nlinks = 0
        else:
            n_files = get_nfiles(messages)
            ratio_files_and_messages = get_ratio_files_and_messages(
                n_messages, n_files)
            most_common_words = get_most_common_words(messages)
            nlinks = get_nlinks(messages)

        users[user] = {
            'gender': gender,
            'messages': messages,
            'n_messages': n_messages,
            'n_files': n_files,
            'ratio_files_and_messages': ratio_files_and_messages,
            'most_common_word': most_common_words,
            'nlinks': nlinks
        }

    print_info(users)
