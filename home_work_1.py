from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
		pass

class Phone(Field):
    def __init__(self, value):
         if not self.validate(value):
              raise ValueError('Phone number must contain exactly 10 digits.')
         super().__init__(value)

    @staticmethod
    def validate(value):
         return value.isdigit() and len(value) == 10

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
    
    def edit_phone(self, new_phone, old_phone):
        phone_obj = self.find_phone(old_phone)
        if not phone_obj:
            raise ValueError (f"Phone {old_phone} not found.")
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
        
    def __str__(self):
        result = []
        for record in self.data.values():
            result.append(str(record))
        return "\n".join(result) if result else "No contacts found."


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command"
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    name, phone = args
    name = name.lower()
    contacts[name] = phone
    return 'Contact added.'

@input_error
def change_contact(args, contacts):
    name, phone = args
    name = name.lower()
    if name in contacts:
        contacts[name] = phone
        return 'Contact updated.'
    else:
        return 'Contacts not found.'

@input_error
def show_phone(args, contacts):
    name = args[0].lower()
    if name in contacts:
        return contacts[name]
    else:
        return 'Contacts not found.'

def show_all(contacts):
    if not contacts:
        return 'No contacts found.'
    result = []
    for name, phone in contacts.items():
        result.append(f'{name}: {phone}')
    return '\n'.join(result)

def main():
    contacts = {}
    print("Welcome to assistant bot!")
    while True:
        user_input = input('Enter a command: ')
        if not user_input:
            print('Enter a valid command.')
            continue

        try:
            command, *args = parse_input(user_input)
        except ValueError:
            print('Enter a valid command.')
            continue

        if command in ['close', 'exit']:
            print('Good bay!')
            break
        elif command == 'hello':
            print('How can i halp you?')
        elif command == 'add':
            print(add_contact(args, contacts))
        elif command == 'change':
            print(change_contact(args, contacts))
        elif command == 'phone':
            print(show_phone(args, contacts))
        elif command == 'all':
            print(show_all(contacts))
        else:
            print('Invalid command.')

if __name__ == "__main__":
    main()
