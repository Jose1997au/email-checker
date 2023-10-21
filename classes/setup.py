import os

class Setup():
    def __init__(self):
        lines = []
        with open('login-info.txt', 'r') as file:
            lines = file.readlines()

        if len(lines) == 0:
            self.main()

    def clear(self):
        if os.name == 'nt':
            os.system('cls')

    def save_info(self, email, password):
        with open('login-info.txt', 'r+') as file:
            lines = file.readlines()
            lines.append(f"{email}\n")
            lines.append(f"{password}\n")

            file.writelines(lines)

    def main(self):
        while True:
            global email
            email = input("Enter email: ").strip()
            self.clear()

            if not "@" in email:
                print("Invalid email. Missing ('@')")
                continue

            if not "gmail" in email:
                print("Invalid email. Must be ('gmail')")
                continue

            if not ".com" in email:
                print("Invalid email. Missing ('.com')")
                continue

            if not "@gmail.com" in email:
                strings = email.split("@")
                print(f"Invalid email. Must be @gmail.com, not '{strings[1]}'")
                continue

            break

        while True:
            global password_old
            password_old = input("Enter password: ").strip()
            self.clear()
            password_new = input("Confirm password: ").strip()
            self.clear()

            if password_old == password_new:
                break
            else:
                print("Passwords do not match.")

        self.save_info(email, password_old)

a = Setup()