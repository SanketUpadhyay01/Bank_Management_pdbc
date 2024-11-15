import re
from constants.constants import MIN_PASSWORD_LENGTH

class UserValidation:
    """
    Validates user input fields such as email, phone, and password.
    """

    def validate_email(self, email: str) -> bool:
        """
        Checks if email contains '@' and ends with '.com' to be valid.
        """
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))

    def validate_phone(self, phone: str) -> bool:
        """
        Ensures phone number is 10 digits and contains only numbers.
        """
        return phone.isdigit() and len(phone) == 10

    def validate_password(self, password: str) -> bool:
        """
        Ensures password meets minimum length requirement and includes at least
        one uppercase letter, one lowercase letter, one digit, and one special character.
        """
        if len(password) < MIN_PASSWORD_LENGTH:
            return False
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$'
        return bool(re.match(pattern, password))

    def validate_age(self, age: int) -> bool:
        """
        Ensures the age is a positive integer.
        """
        return age > 0

    def validate_name(self, name: str) -> bool:
        """
        Ensures name only contains alphabetic characters and spaces.
        """
        return bool(re.match(r'^[A-Za-z\s]+$', name))
