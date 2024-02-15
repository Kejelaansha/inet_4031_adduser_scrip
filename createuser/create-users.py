#!/usr/bin/env python3
import os
import re
import sys

def main():
    for line in sys.stdin:
        # Use re.match to check for the presence of a '#' at the start of a line.
        # We want to skip any lines in the file that start with a hashtag.
        match = re.match(r'^#', line)

        # Strip any whitespace and split into an array.
        fields = line.strip().split(':')

        # This checks if the line starts with a '#' or does NOT have five fields.
        # If either condition is true, we skip the line.
        if match or len(fields) != 5:
            continue

        # Extracting fields from the line.
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])
        groups = fields[4].split(',')  # Splitting the group field into a list.

        # Creating a user account.
        print(f"==> Creating account for {username}...")
        cmd = f"/usr/sbin/adduser --disabled-password --gecos '{gecos}' {username}"
        os.system(cmd)  # Executing the command to add the user.

        # Setting the user's password.
        print(f"==> Setting the password for {username}...")
        cmd = f"/bin/echo -ne '{password}\n{password}' | /usr/bin/sudo /usr/bin/passwd {username}"
        os.system(cmd)

        # Assigning the user to groups.
        for group in groups:
            if group != '-':
                print(f"==> Assigning {username} to the {group} group...")
                cmd = f"/usr/sbin/adduser {username} {group}"
                os.system(cmd)

if __name__ == '__main__':
    main()

