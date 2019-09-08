from main.libs.firebase import messages_ref
import hashlib


def get_conversation_hash(sender_email=None, receiver_email=None):
    if sender_email < receiver_email:
        sender_email, receiver_email = receiver_email, sender_email
    return hashlib.md5((sender_email + receiver_email).encode()).hexdigest()


def create_user_message(sender_email=None, receiver_email=None, text=None):
    try:
        conversations = messages_ref.get()
        messaged_before = False
        conversation_hash = get_conversation_hash(sender_email=sender_email, receiver_email=receiver_email)
        if not conversations:
            messages_ref.push({'conversation_hash': conversation_hash})
            conversations = messages_ref.get()

        print(conversations)
        for key, val in conversations.items():
            if val['conversation_hash'] == conversation_hash:
                messaged_before = True
                messages_ref.child(key).child(val['conversation_hash']).push({'text': text, 'email': sender_email})

        if not messaged_before:
            chat_node = messages_ref.push({'conversation_hash': conversation_hash})
            chat_node.push({'text': text, 'email': sender_email})
    except Exception:
        raise Exception('There is an error creating user message')


def get_user_messages(sender_email=None, receiver_email=None):
    try:
        conversations = messages_ref.get()
        conversation_hash = get_conversation_hash(sender_email=sender_email, receiver_email=receiver_email)
        messages = []
        for key, val in conversations.items():
            if val['conversation_hash'] == conversation_hash:
                messages = messages_ref.child(key).child(conversation_hash).get()
                messages = [value for key, value in messages.items()]

        return messages
    except Exception:
        raise Exception('There is an error getting user messages')
