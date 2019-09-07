from marshmallow import Schema, EXCLUDE, pre_load, validates
from main.libs.neverbounce.email_verification import validate_email


class BaseSchema(Schema):
    @pre_load()
    def strip_data(self, data, **kwargs):
        for key in data:
            if isinstance(data[key], str):
                data[key] = data[key].strip()
        return data

    @validates('email')
    def validate_email(self, email):
        if email:
            validate_email(email)

    class Meta:
        unknown = EXCLUDE
