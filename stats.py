import re


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


def most_common(messages):
    words = []
    for x in messages:
        for y in x.split(' '):
            words.append(y)
    if len(words) == 0:
        return ''
    else:
        return max(set(words), key=words.count)


def print_info(users):
    print('\n')
    print('Number of messages:')
    for user in users:
        print('\t' + user + ': ' + str(users[user]['n_messages']) +
              ". Most common message: " + users[user]['most_common_word'])

    print('\n')
    print('Number of files sent:')
    for user in users:
        print('\t' + user + ': ' + str(users[user]['n_files']) +
              '. Ratio: ' +
              str(round(users[user]['ratio_files_and_messages'], 2)) + " %")

    print('\n')


def main(content):
    users = get_users(content)
    for user in users:
        users[user]['messages'] = get_messages(content, user)
        users[user]['n_messages'] = len(users[user]['messages'])
        users[user]['n_files'] = get_nfiles(users[user]['messages'])
        if users[user]['n_messages'] != 0:
            users[user]['ratio_files_and_messages'] = users[user]['n_files'] * \
                100 / users[user]['n_messages']
        else:
            users[user]['ratio_files_and_messages'] = 0
        users[user]['most_common_word'] = most_common(users[user]['messages'])

    print_info(users)
