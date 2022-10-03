import re
import shelve
from datetime import date
from pathlib import Path

from dateutil.parser import parse as date_parse, ParserError
from dateutil.relativedelta import relativedelta


class Field:
    def __init__(self, value=None):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

    def __eq__(self, other) -> bool:
        return type(self) == type(other) and self.__value == other.__value


class Name(Field):
    def __init__(self, name: str):
        super().__init__(name)
        self.is_required = True

    @Field.value.setter
    def value(self, name: str):
        if not name:
            raise ValueError("A contact name cannot be empty.")
        super(Name, type(self)).value.fset(self, self.sanitize_name(name))

    @staticmethod
    def sanitize_name(name: str) -> str:
        return name.lower().title()

    def __str__(self):
        return self.value


class Email(Field):
    def __init__(self, email: str):
        super().__init__(email)
        self.is_required = False

    @Field.value.setter
    def value(self, email: str):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.fullmatch(regex, email):
            super(Email, type(self)).value.fset(self, email)
        else:
            raise ValueError(f"Entered email '{email}' is incorrect.")

    def __str__(self):
        return self.value


class Address(Field):
    def __init__(self, address: str):
        super().__init__(address)
        self.is_required = False

    @Field.value.setter
    def value(self, address: str):
        super(Address, type(self)).value.fset(self, address)

    def __str__(self):
        return self.value


class Phone(Field):
    def __init__(self, phone: str):
        super().__init__(phone)
        self.is_required = False

    @Field.value.setter
    def value(self, new_phone: str):
        if not new_phone:
            raise ValueError("A phone number cannot be empty.")
        super(Phone, type(self)).value.fset(self, self.sanitize_phone(new_phone))

    @staticmethod
    def sanitize_phone(phone: str) -> str:
        tel_code = {9: "380", 10: "38"}
        snz_phone = "".join([ch for ch in phone if ch.isdecimal()])
        if len(snz_phone) not in (9, 10, 12):
            raise ValueError(f"Entered phone '{phone}' is incorrect.")
        return tel_code.get(len(snz_phone), "") + snz_phone

    def __str__(self):
        pn = self.value
        return f"+{pn[:3]}({pn[3:5]}){pn[5:8]}-{pn[8:10]}-{pn[10:]}"


class Birthday(Field):
    def __init__(self, birthday: str):
        super().__init__(birthday)
        self.is_required = False

    @Field.value.setter
    def value(self, birthday: str):
        if not birthday:
            raise ValueError("A birthday cannot be empty.")

        try:
            birth_date = date_parse(birthday, dayfirst=True, yearfirst=False).date()
        except ParserError:
            raise ValueError("Unknown date string format. Use date format: 'dd.mm.Y'")

        if birth_date > date.today():
            raise ValueError(f"Entered birthday '{birthday}' is incorrect.")

        super(Birthday, type(self)).value.fset(self, birth_date)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y") if self.value else ""


class Record:
    def __init__(self, cnt_name: Name, phone: Phone = None):
        self.cnt_name = cnt_name
        self.phones = [phone] if phone else []
        self.email = None
        self.address = None
        self.birthday = None

    @property
    def phone_list(self) -> str:
        return ', '.join([str(phone) for phone in self.phones])

    @property
    def days_to_birthday(self) -> int:
        if self.birthday:
            today = date.today()
            date_birth = date(today.year, self.birthday.value.month, self.birthday.value.day)

            if date_birth >= today:
                delta_days = (date_birth - today).days
            else:
                delta_days = ((date_birth + relativedelta(years=1)) - today).days

            return delta_days

    def match_search_str(self, search_str: str):
        if self.cnt_name.value.lower().find(search_str) != -1:
            return True
        for phone in self.phones:
            if phone.value.find(search_str) != -1:
                return True
        return False

    @property
    def fields_info(self) -> {}:
        return {"cnt_name": {"caption": "Name", "class": Name, "is_list": False, "is_required": True},
                "phones": {"caption": "Phones", "class": Phone, "is_list": True, "is_required": False},
                "email": {"caption": "Email", "class": Email, "is_list": False, "is_required": False},
                "address": {"caption": "Address", "class": Address, "is_list": False, "is_required": False},
                "birthday": {"caption": "Birthday", "class": Birthday, "is_list": False, "is_required": False}}

    @property
    def values(self) -> []:
        return [self.cnt_name.value,
                self.phone_list if self.phones else "",
                self.email.value if self.email else "",
                self.address.value if self.address else "",
                str(self.birthday) if self.birthday else ""]

    def __str__(self):
        tmp_list = [f"Name: {self.cnt_name.value}"]
        if self.phones:
            tmp_list.append(f"phones: {self.phone_list}")
        if self.birthday:
            tmp_list.append(f"birthday: {str(self.birthday)}")
            tmp_list.append(f"days to birthday: {self.days_to_birthday}")

        return "; ".join(tmp_list)


class AddressBook:
    print_page_size = -1

    def __init__(self):
        data_path = Path(Path(Path.home(), "FreeAssistData"))
        data_path.mkdir(exist_ok=True)
        self.__data = shelve.open(str(Path(data_path, "address_book")), flag='c')

    def __del__(self):
        self.__data.close()

    def add_contact(self, name: str, phone: str = None) -> str:
        if name.lower() in self.__data:
            raise ValueError(f"A contact named '{name}' already exists.")
        self[name] = Record(Name(name), Phone(phone) if phone else None)
        return f"Contact named '{self[name].cnt_name.value}' has been added to address book."

    def del_contact(self, name: str) -> str:
        del self[name]
        return f"Contact named '{Name.sanitize_name(name)}' has been deleted from address book."

    def get_contact(self, name: str) -> Record:
        return self[name]

    def is_contact_exist(self, name: str) -> bool:
        return name.lower() in self.__data.keys()

    @staticmethod
    def get_empty_contact() -> Record:
        return Record(Name("_"))

    def set_contact(self, contact: Record) -> str:
        self[contact.cnt_name.value.lower()] = contact
        return f"Contact named '{contact.cnt_name.value}' has been saved to address book."

    def find_contacts(self, search_str: str) -> list:
        if not search_str or len(search_str) < 2:
            raise ValueError("The search string cannot be shorter than 2 characters.")

        find_contacts = []
        search_str = search_str.strip().lower()
        for contact in self.__data.values():
            if contact.match_search_str(search_str):
                find_contacts.append(contact.values)
        return find_contacts

    def birthday_list(self, days: int = 7):
        find_contacts = []
        for contact in self.__data.values():
            if contact.days_to_birthday and contact.days_to_birthday == days:
                find_contacts.append(contact.values)
        return find_contacts

    def __len__(self):
        return len(self.__data)

    def __getitem__(self, name: str) -> Record:
        result = self.__data.get(name.lower())
        if not result:
            raise ValueError(f"A contact named '{Name.sanitize_name(name)}' not found.")
        return result

    def __setitem__(self, name: str, contact: Record):
        self.__data[name.lower()] = contact

    def __delitem__(self, name: str):
        try:
            del self.__data[name.lower()]
        except KeyError:
            raise ValueError(f"A contact named '{Name.sanitize_name(name)}' not found.")

    def __iter__(self):
        self.__rec_counter = 0
        self.__len = len(self.__data)
        if not self.__len:
            raise ValueError("No contacts have been found.")
        if self.print_page_size == -1:
            self.print_page_size = self.__len
        self.__sorted_keys = (key for key in sorted(self.__data))
        return self

    def __next__(self):
        if self.__rec_counter < self.__len:
            out_list = []
            while len(out_list) < self.print_page_size and self.__rec_counter < self.__len:
                self.__rec_counter += 1
                key = next(self.__sorted_keys)
                out_list.append(self.__data[key].values)
            return out_list
        else:
            raise StopIteration
