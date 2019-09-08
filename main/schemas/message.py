from marshmallow import fields, validate
from main.schemas.base import BaseSchema


class MessageSchema(BaseSchema):
    receiver_email = fields.Email(required=True)
    # timestamp = fields.DateTime(required=True)
    text = fields.String()
