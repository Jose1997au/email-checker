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
        found = False
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        date_str = yesterday.strftime("%d-%b-%Y")

        try:
            # Search for emails since yesterday
            _, data = self.imap.uid('search', None, '(SINCE {date})'.format(date=date_str))

            # Keep uid_list as a list of bytes
            uid_list = data[0].split()
            uid_list.reverse()  # if you want the latest emails first

            for email_uid in uid_list:

                str_email_uid = email_uid.decode('utf-8')

                result, email_data = self.imap.uid('fetch', str_email_uid, '(RFC822)')
                if result != 'OK':
                    print(f"Error fetching email with UID: {str_email_uid}")
                    continue

                raw_email = email_data[0][1]
                message = email.message_from_bytes(raw_email)

                if email_from.lower() in message.get('From').lower():
                    found = True
                    print("Message found.")
                    print(f"UID: {str_email_uid}")
                    print(f"From: {message.get('From')}")
                    print(f"To: {message.get('To')}")
                    print(f"BCC: {message.get('BCC')}")
                    print(f"Date: {message.get('Date')}")
                    print(f"Subject: {message.get('Subject')}")
                    print("Content: ")
                    for part in message.walk():
                        if part.get_content_type() == "text/plain":
                            print(part.get_payload(decode=True).decode('utf-8'))  
                    break 
        except imaplib.IMAP4.error as e:
            print('An error occurred: ', e)
            
        return found

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
            _, email_data = self.imap.uid('fetch', email_uid, '(RFC822)')
            raw_email = email_data[0][1]
            message = email.message_from_bytes(raw_email)
            return message
        except imaplib.IMAP4.error as e:
            print('An error occurred: ', e)
            return None
