import os.path
import sys

import print_data

import users
import metadata_chat

# Returns the content of the file path


def get_content(file_path):
    if not os.path.isfile(file_path):
        print("The file doesn't exists")
        sys.exit()
    else:
        f = open(file_path, 'r', encoding="utf8")
        content = f.readlines()
        f.close()
        return content


if __name__ == '__main__':

    # Check if the user has entered a file_path to the image
    if(len(sys.argv) > 1):
        if(sys.argv[1] == '--help' or sys.argv[1] == '-h'):
            print(
                '\nMPD Help: You must enter a file path as an argument like\n\t$> main.py chat.txt\n')
            sys.exit()

        content = get_content(sys.argv[1])
        metadata = metadata_chat.main(content)
        users = users.main(content, metadata)

        if('--get-list-word' in sys.argv):
            f = open('./chats/words.txt', 'w', encoding='utf8')
            for user in users:
                f.write(user + '\n')
                f.write(
                    str(users[user]['most_common_word']).strip('[]') + '\n')
            f.close()

        # print_data.print_metadata(metadata)
        # print_data.print_info_table(users)

    else:
        print("You must enter a file path as an argument")
        sys.exit()
