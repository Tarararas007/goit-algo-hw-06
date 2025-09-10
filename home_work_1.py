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
    
    def edit_phone(self, old_phone, new_phone):
        if not self.find_phone(old_phone):
            raise ValueError(f"Phone {old_phone} not found.")
        self.add_phone(new_phone)

        self.remove_phone(old_phone)

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
