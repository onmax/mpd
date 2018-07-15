import re
import requests

import print_data


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


def get_gender(users):
    genders = []
    urls = []

    for i in range(len(users)):
        api_str = ''
        for j in range(10):
            index = i * 10 + j
            if index >= len(users):
                break
            api_str += 'name=' + list(users)[index] + '&'
        urls.append('https://api.genderize.io/?' + api_str)
        if index >= len(users):
            break
    for url in urls:
        json = requests.get(url=url).json()

        for r in json:
            if(r['gender'] != None):
                genders.append(r['gender'])
            else:
                genders.append('Not identified')

    return genders


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


def get_ratio(n_messages, elem):
    '''
    Return the number of elem(files or links) sent every 100 messages
    '''
    return elem * 100 / n_messages


def get_n_emojis(messages):
    n = len(re.findall(r'[\U0001f600-\U0001f650]', ''.join(messages)))
    return n


def get_longest_message(messages):
    return max(messages, key=len)


def get_most_common_words(messages):
    '''
    Creates the words list with all words from messages and then return the word that most repeat in the word list
    '''
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
    '''
    Return the average of messages sent in a day
    Note: mpd means messages per day 
    '''
    return n / days


def main(content, metadata):
    users = get_users(content)
    genders = get_gender(users)
    for i, user in enumerate(users):
        messages = get_messages(content, user)
        n_messages = len(messages)
        if(n_messages == 0):
            most_common_words = ''
            n_files = ratio_files_and_messages = n_links = ratio_links_and_messages = mpd = 0
        else:
            longest_message = get_longest_message(messages)
            len_longest_message = len(longest_message)
            n_emojis = get_n_emojis(messages)
            most_common_words = get_most_common_words(messages)
            n_files = get_nfiles(messages)
            ratio_files_and_messages = get_ratio(n_messages, n_files)
            n_links = get_nlinks(messages)
            ratio_links_and_messages = get_ratio(n_messages, n_links)
            mpd = get_mpd(n_messages, metadata['days'])

        users[user] = {
            'gender': genders[i],
            'messages': messages,
            'n_messages': n_messages,
            'longest_message': longest_message,
            'len_longest_message': len_longest_message,
            'n_emojis': n_emojis,
            'most_common_word': most_common_words,
            'n_files': n_files,
            'ratio_files_and_messages': ratio_files_and_messages,
            'n_links': n_links,
            'ratio_links_and_messages': ratio_links_and_messages,
            'mpd': mpd
        }

    print_data.print_info_table(users)
