from classes.email_reader import EmailReader
from classes.email_sender import EmailSender
from dateutil.parser import parse
from classes.setup import Setup
import re

commands = {
    "-scan": {
        "desc": "Scans your inbox for emails from a specific person.",
        "args": "Email"
    },
    "-sendEmail": {
        "desc": "Sends an email to a specific person.",
        "args": "Email-Content"
    },
    "-reply": {
        "desc": "Replies to an email.",
        "args": "UID, Content"
    },
    "-showEmail": {
        "desc": "Shows email with given UID.",
        "args": "UID"
    },
    "-printCredentials": {
        "desc": "Prints your email and password for you to see.",
        "args": "None"
    },
    "-changeEmail": {
        "desc": "Changes email for if you typed it incorrectly.",
        "args": "Email"
    },
    "-changePassword": {
        "desc": "Changes password for if you typed it incorrectly.",
        "args": "Password"
    },
    "-clear": {
        "desc": "Clears the terminal.",
        "args": "None"
    }
}

def print_cmds():
    """Prints commands neatly in the terminal"""
    key_width = len(max(commands.keys(), key=len)) + 4
    desc_width = len(max([val['desc'] for val in commands.values()], key=len)) + 4
    args_width = len(max([val['args'] for val in commands.values()], key=len)) + 4

    print(f"{'Command':<{key_width}}{'Description':<{desc_width}}{'Arguments':<{args_width}}")
    print('-' * (key_width + desc_width + args_width))
        
    for command_name in commands:
        print(f"{command_name:<{key_width}}{commands[command_name]['desc']:<{desc_width}}{commands[command_name]['args']:<{args_width}}")

a = Setup()

lines = []
with open('login-info.txt') as file:
    lines = file.readlines()
    
user = {
    'email': lines[0].strip(),
    'password': lines[1].strip()
}

reader = EmailReader(user)
sender = EmailSender(user)

while True:
    print_cmds()
    command = input("Command Line: ").strip().lower()
    a.clear()
    print_cmds()

    if command == "-scan":
        while True:
            target = input("Who do you want to search for? ")
            a.clear()
            is_valid = reader.verify(target)
            if not is_valid: continue
            break
        print("Fetching emails...")
        found = reader.find_email_from(target)
        if not found:
            print(f"Could not find emails from {target} within the last 24 hours.")
    elif command == "-sendemail":
        new_email = sender.create_email()
        while True:
            free_to_go = True
            global recipient
            recipients = input("Enter recipients (Seperate by space): ").strip().split()
            for recipient in recipients:
                is_valid = reader.verify(recipient)
                if not is_valid:
                    free_to_go = False
                    break
            if free_to_go:
                break

        while True:
            free_to_go = True
            global recipients_cc
            recipients_cc = input("Enter CC recipients (Press enter if none): ").strip().split()
            for recipient in recipients_cc:
                is_valid = reader.verify(recipient)
                if not is_valid:
                    free_to_go = False
                    break
            if free_to_go:
                break
        
        while True:
            free_to_go = True
            global recipients_bcc
            recipients_bcc = input("Enter BCC recipients (Press enter if none): ").strip().split()
            for recipient in recipients_bcc:
                is_valid = reader.verify(recipient)
                if not is_valid:
                    free_to_go = False
                    break
            if free_to_go:
                break

        subject = input("Enter a subject: ")
        print("Enter content (type 'END' on a new line to finish):")
        lines = []
        while True:
            line = input()
            if line.strip() == 'END':
                break  # Stop the loop if the user types 'END'
            lines.append(line)
        
        # Join the lines into a single string with line breaks
        content = '\n'.join(lines)


        new_email.add_recipient(recipients, "to")
        new_email.add_recipient(recipients_cc, "cc")
        new_email.add_recipient(recipients_bcc, "bcc")

        new_email.add_subject(subject=subject)
        new_email.add_content(content=content)

        sender.send_email(new_email)

    elif command == "-reply":
        email_uid = input("Enter the UID of the email you want to reply to: ")
        a.clear()
        original_email = reader.get_email_by_uid(email_uid)

        if original_email is None:
            print("Could not find the email.")
            continue

        reply_email = sender.create_email()

        original_sender = original_email.get('From')
        string_pool = original_sender.split()
        for string in string_pool:
            if "<" in string and ">" in string:
                original_sender = re.sub(r'[<>]', '', string)
        reply_email.add_recipient([original_sender], type="to")

        if original_email.get('Cc'):
            original_cc = original_email.get('Cc').split(',')
            for cc_address in original_cc:
                reply_email.add_recipient(cc_address.strip(), type="cc")

        reply_subject = "Re: " + original_email.get('Subject', '')
        reply_email.add_subject(reply_subject)

        print("Enter content (type 'END' on a new line to finish):")
        lines = []
        while True:
            line = input()
            if line.strip() == 'END':
                break  # Stop the loop if the user types 'END'
            lines.append(line)

        user_reply_content = '\n'.join(lines)

        original_body = ""
        if original_email.is_multipart():
            for part in original_email.walk():
                if part.get_content_type() == 'text/plain' and not part.is_multipart():
                    original_body = part.get_payload(decode=True).decode('utf-8')
                    break
        else:
            original_body = original_email.get_payload(decode=True).decode('utf-8')

        original_date = original_email.get('Date', '')
        parsed_date = parse(original_date)
        formatted_date = parsed_date.strftime('%a, %b %d, %Y at %I:%M %p')

        quoted_content = f"\n\nOn {formatted_date} <{original_sender}> wrote:\n{original_body}"
        indented_original_body = '\n'.join(['    ' + line for line in original_body.split('\n')])
        quoted_content = f"\n\nOn {formatted_date}, {original_sender} wrote:\n{indented_original_body}"
        full_reply_content = user_reply_content + quoted_content

        reply_email.add_content(full_reply_content)

        try:
            sender.send_email(reply_email)
            print("Reply sent!")
        except Exception as e:
            print(f"An error occurred: {e}")
    elif command == "-showemail":
        email_uid = input("Enter the UID of the email you want to reply to: ")
        a.clear()

        original_emai1l = reader.get_email_by_uid(email_uid)
        print(original_emai1l)
    elif command == "-printcredentials":
        with open('login-info.txt', 'r') as file:
            lines = file.readlines()
            
        a.clear()
        print(f"Email: {lines[0]}")
        print(f"Password: {lines[1]}")
    elif command == "-changeemail":
        while True:
            new_email = input("Enter your new email: ")
            is_valid = reader.verify(new_email)
            if is_valid:
                break
            with open('login-info.txt', 'r+') as file:
                lines = file.readlines()
                lines[0] = new_email
                file.writelines(lines)
        a.clear()
    elif command == "-changepassword":
        while True:
            new_password = input("Enter your new password: ")
            is_valid = reader.verify(new_email)
            if is_valid:
                break
            with open('login-info.txt', 'r+') as file:
                lines = file.readlines()
                lines[0] = new_password
                file.writelines(lines)
    elif command == "-clear":
        a.clear()