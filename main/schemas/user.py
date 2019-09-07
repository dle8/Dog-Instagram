from marshmallow import fields, validate
from main.schemas.base import BaseSchema


class AuthSchema(BaseSchema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))


class ConfirmationCodeSchema(BaseSchema):
    confirmation_code = fields.Integer(required=True)
    email = fields.Email(required=True)
