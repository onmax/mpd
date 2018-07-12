import os.path
import sys

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
        metadata_chat.main(content)
        #users.main(content)

    else:
        print("You must enter a file path as an argument")
        sys.exit()
