import re


def get_users(content):
    users = []
    regex = '\d\d:\d\d\s-\s(.*?):\s'
    for x in content:
        x = x.rstrip()
        user = re.findall(regex, x)
        if len(user) == 1:
            if not user[0] in users:
                users.append(user[0])
    return users


def get_messages(content):
    users = get_users(content)
    messages = {}
    for user in users:
        messages[user] = []
        regex = user + ': (.*)'

        for x in content:
            x = x.rstrip()
            msg = re.findall(regex, x)
            if(len(msg) != 0):
                messages[user].append(msg[0])
    return messages


def get_nmessages(content):
    messages = get_messages(content)
    for user in messages:
        print(user + ': ' + str(len(messages[user])))
