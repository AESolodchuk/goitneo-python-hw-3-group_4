from .custom_errors import WrongDataFormat, PhoneWasNotFound
from collections import UserDict, defaultdict
from datetime import datetime, timedelta
import calendar


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Birthday:
    def __init__(self, birthday):
        date_format = "%d.%m.%Y"
        try:
            self.value = datetime.strptime(birthday, date_format).date()
        except ValueError:
            raise WrongDataFormat


class Phone(Field):
    pass


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday

    def check_phone_exist(self, phone):
        phone_record = [record for record in self.phones if record.value == phone]
        if len(phone_record) > 0:
            return phone_record
        else:
            raise PhoneWasNotFound

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return True

    def find_phone(self, phone):
        for phone in self.check_phone_exist(phone):
            return phone

    def show_birthday(self):
        if self.birthday:
            return self.birthday.value
        return "not provided"

    def edit_phone(self, phone_to_replace, new_phone):
        to_edit = self.remove_phone(phone_to_replace)
        for i in range(to_edit):
            self.add_phone(new_phone)

    def remove_phone(self, phone):
        to_remove = self.check_phone_exist(phone)
        for phone in to_remove:
            self.phones.remove(phone)
        return len(to_remove)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict, Record):
    def add_record(self, record=Record):
        self.data[record.name.value] = record

    def find(self, name):
        try:
            return self.data[name]
        except:
            return False

    def get_birthdays_per_week(self):
        def next_monday(birthday_this_year, delta_days):
            for i in range(7 - delta_days):
                if (birthday_this_year + timedelta(days=i)).weekday() == 0:
                    return True
                else:
                    i += 1

        def append_users_birthday(birthday_weekday, name):
            users_birthday[birthday_weekday].append(name)

        weekend_days = [5, 6]
        users_birthday = defaultdict(list)
        users_birthday = {0: [], 1: [], 2: [], 3: [], 4: []}
        today_date = datetime.today().date()

        for key, value in self.data.items():
            name = key
            if value.birthday is None:
                continue
            else:
                birthday = value.birthday.value
                birthday_this_year = (
                    birthday.replace(year=today_date.year + 1)
                    if birthday.replace(year=today_date.year) < today_date
                    else birthday.replace(year=today_date.year)
                )
                delta_days = (birthday_this_year - today_date).days
                if delta_days < 7:
                    if birthday_this_year.weekday() in weekend_days and next_monday(
                        birthday_this_year, delta_days
                    ):
                        append_users_birthday(0, name)
                    elif birthday_this_year.weekday() not in weekend_days:
                        append_users_birthday(birthday_this_year.weekday(), name)

        for key, value in users_birthday.items():
            if value:
                return (f"{calendar.day_name[key]:<9}: {", ".join(value):<}")
            else:
                return "No scheduled birthdays for the upcoming week"

    def delete(self, name):
        self.data.pop(name)
