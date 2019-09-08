from marshmallow import fields, validate, validates
from main.schemas.base import BaseSchema
from main.libs.neverbounce.email_verification import validate_email


class AuthSchema(BaseSchema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))

    @validates('email')
    def validate_email(self, email):
        if email:
            validate_email(email)


class ConfirmationCodeSchema(BaseSchema):
    confirmation_code = fields.Integer(required=True)
    email = fields.Email(required=True)

    @validates('email')
    def validate_email(self, email):
        if email:
            validate_email(email)

