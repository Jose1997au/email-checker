from classes.email_reader import EmailReader
from classes.email_sender import EmailSender
from classes.setup import Setup

commands = {
    "-scan": {
        "desc": "Scans your inbox for emails from a specific person.",
        "args": "Email"
    },
    "-sendEmail": {
        "desc": "Sends an email to a specific person.",
        "args": "Email"
    },
    "-reply": {
        "desc": "Replies to an email.",
        "args": "Email ID"
    },
    "-showEmail": {
        "desc": "Shows email with given UID.",
        "args": "Email ID"
    },
    "-changeEmail": {
        "desc": "Changes email for if you typed it incorrectly.",
        "args": "Email"
    },
    "-changePassword": {
        "desc": "Changes password for if you typed it incorrectly.",
        "args": "Password"
    },
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
    command = input("Command Line: ")
    a.clear()
    print_cmds()
    command.lower().strip()

    if command == "-scan":
        while True:
            target = input("Who do you want to search for? ")
            a.clear()
            is_valid = reader.verify(target)
            if not is_valid: continue
            break
        print("Fetching emails...")
        reader.find_email_from(target)
    elif command == "-sendEmail":
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
        content = input("Enter content: ")

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
        reply_email.add_recipient(original_sender, type="to")

        if original_email.get('Cc'):
            original_cc = original_email.get('Cc').split(',')
            for cc_address in original_cc:
                reply_email.add_recipient(cc_address.strip(), type="cc")

        reply_subject = "Re: " + original_email.get('Subject', '')
        reply_email.add_subject(reply_subject)

        user_reply_content = input("Enter your reply: ")

        original_body = ""
        if original_email.is_multipart():
            for part in original_email.walk():
                if part.get_content_type() == 'text/plain' and not part.is_multipart():
                    original_body = part.get_payload(decode=True).decode('utf-8')
                    break
        else:
            original_body = original_email.get_payload(decode=True).decode('utf-8')

        quoted_content = f"\n\n--- Original Message ---\n{original_body}"
        full_reply_content = user_reply_content + quoted_content
        reply_email.add_content(full_reply_content)

        try:
            sender.send_email(reply_email)
            print("Reply sent!")
        except Exception as e:
            print(f"An error occurred: {e}")
    elif command == "-showEmail":
        email_uid = input("Enter the UID of the email you want to reply to: ")
        a.clear()

        original_emai1l = reader.get_email_by_uid(email_uid)
        print(original_emai1l)