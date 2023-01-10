'''
pip install phonenumbers
'''
import phonenumbers
from phonenumbers import geocoder, carrier, timezone


number = "YOUR_PHONE_NUMBER_WITH_COUNTRY_CODE : +CountrycodePhonenumber"

ch_number = phonenumbers.parse(number, "CH")
carrier_name = phonenumbers.parse(number, "RO")
gb_number = phonenumbers.parse(number, "GB")

print(geocoder.description_for_number(ch_number, "en"))
print(carrier.name_for_number(carrier_name, "en"))
print(timezone.time_zones_for_number(gb_number))