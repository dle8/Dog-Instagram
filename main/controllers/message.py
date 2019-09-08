from flask import jsonify
from main import app, errors
from main.utils import parse_args_with, jwt_required
from main.schemas.message import MessageSchema
from main.libs.firebase.message import create_user_message, get_user_messages


@app.route('/messages', methods=['POST'])
@jwt_required()
@parse_args_with(MessageSchema())
def create_message(args, **kwargs):
    create_user_message(
        sender_email=kwargs['sub'],
        receiver_email=args.get('receiver_email'),
        text=args.get('text')
    )
    return jsonify({'message': 'Message sent.'})


@app.route('/messages/<string:receiver_email>', methods=['GET'])
@jwt_required()
def get_messages(**kwargs):
    messages = get_user_messages(sender_email=kwargs['sub'], receiver_email=kwargs['receiver_email'])
    return jsonify(messages)
