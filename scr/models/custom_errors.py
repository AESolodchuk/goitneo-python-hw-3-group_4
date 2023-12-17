class PhoneContainsAlphaSymbols(KeyError):
    pass


class BirthdayFormat(KeyError):
    pass


class PhoneContainsTenSymbols(KeyError):
    pass


class WrongDataFormat(ValueError, KeyError):
    pass


class NewPhoneWasNotProvided(ValueError, KeyError):
    pass


class PhoneWasNotFound(KeyError):
    pass


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BirthdayFormat:
            return "Please be sure that provided format is applicable,\nformat for birthday adding: 'name' 'birthday'"
        except PhoneWasNotFound:
            return "We cannot find this phone number, please try it again"
        except NewPhoneWasNotProvided:
            return "Please be sure that provided format is applicable,\nformat for phone changing: 'name' 'old phone number' 'new phone number'"
        except WrongDataFormat:
            return "Please be sure that provided format is applicable,\nallowed data format: DD.MM.YYYY"
        except PhoneContainsTenSymbols:
            return "Phone must contains strictly 10 numbers, please try it again."
        except PhoneContainsAlphaSymbols:
            return "Phone cannot contain letters, please try it again."
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Sorry, we couldn't find the contact. Please check the name and try again."
        except IndexError:
            return "Contact name cannot be empty, please and try again."

    return inner
