import phonenumbers
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_phone_number(phone,country_code):
    try:
        phone_number = phonenumbers.parse(phone,country_code)
        if not phonenumbers.is_valid_number(phone_number):
            raise ValidationError(_('Invalid phone number'))

        if  phonenumbers.region_code_for_country_code(phone_number):
            raise ValidationError(_('Invalid country code'))
        
        if phonenumbers.length(phone_number) < 10:
            raise ValidationError(_('Phone number should be at least 10 digits long'))
        
        
        if phonenumbers.length(phone_number) > 12:
            raise ValidationError(_('Phone number should not be more than 12 digits long'))
        
    except phonenumbers.NumberParseException:
        raise ValidationError(_('Enter a valid phone number'))


