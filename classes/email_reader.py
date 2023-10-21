import imaplib
import email
import datetime

class EmailReader():
    def __init__(self, user) -> None:
        try:
            self.imap_server = "imap.gmail.com"

            self.imap = imaplib.IMAP4_SSL(self.imap_server)
            self.imap.login(user['email'], user['password'])

            self.imap.select("Inbox")
        except imaplib.IMAP4.error as e:
            print("Error: ", e)

    def find_email_from(self, email_from):
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        date_str = yesterday.strftime("%d-%b-%Y")

        try:
            # Search for emails since yesterday
            _, data = self.imap.search(None, '(SINCE {date})'.format(date=date_str))

            msgnums = list(map(int, data[0].split()))
            msgnums.reverse()

            for msgnum in msgnums:
                result, data = self.imap.fetch(str(msgnum), "(RFC822)")  # the message number must be converted to string
                if result != 'OK':
                    print(f"Error fetching message {msgnum}")
                    continue

                message = email.message_from_bytes(data[0][1])  # parse the email

                print(f"UID: {msgnum}")
                if email_from.lower() in message.get('From').lower():
                    print("Message found.")
                    print(f"UID: {msgnum}")  # msgnum is an integer, no need to decode
                    print(f"Message Number: {msgnum}")
                    print(f"From: {message.get('From')}")
                    print(f"To: {message.get('To')}")
                    print(f"BCC: {message.get('BCC')}")
                    print(f"Date: {message.get('Date')}")
                    print(f"Subject: {message.get('Subject')}")
                    print("Content: ")
                    for part in message.walk():
                        if part.get_content_type() == "text/plain":
                            print(part.get_payload(decode=True).decode('utf-8'))  # decode the byte content to string
                    break  # stop after finding the first (latest) email from the specified sender
        except imaplib.IMAP4.error as e:
            print('An error occurred: ', e)
            
    def verify(self, email):
        while True:

            if not "@" in email:
                print("Invalid email. Missing ('@')")
                return False

            if not ".com" and not ".org" in email:
                print("Invalid email. Missing ('.com') or ('.org')")
                return False
            
            return True
        
    def get_email_by_uid(self, email_uid):
        try:
            print(email_uid)
            email_uid = str(int(email_uid) + 1)
            print(email_uid)
            _, email_data = self.imap.uid('fetch', email_uid, '(RFC822)')
            raw_email = email_data[0][1]
            message = email.message_from_bytes(raw_email)
            return message
        except imaplib.IMAP4.error as e:
            print('An error occurred: ', e)
            return None
