from django.core.exceptions import ValidationError
import re
import phonenumbers
from django.utils.deconstruct import deconstructible


def validate_f_name(value):
    """Validate Full Name"""
    num = 0
    for char in value.split(' '):
        num+=1

    if num >= 2:
        for i in value.split(' '):
            if i.isdigit():
                raise ValidationError("Toʻliq ism kiriting.(raqamlarsiz)")
    else:
        raise ValidationError("Ism va familiyani o'z ichiga olgan to'liq ismni kiriting")


@deconstructible
class PhoneValidator:
    requires_context = False

    @staticmethod
    def clean(value):
        return re.sub('[^0-9+]+', '', value)

    @staticmethod
    def validate(value):
        try:
            z = phonenumbers.parse(value)  # 998944009080
            if not phonenumbers.is_valid_number(z):
                return False
        except:
            return False

        if len(value) != 13 or not value.startswith("+998"):
            return False

        return True

    def __call__(self, value):
        if not PhoneValidator.validate(value):
            raise ValidationError("Kiritilgan qiymat telefon raqami emas.")

