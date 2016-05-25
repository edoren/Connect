from .MessageSerializer import MessageSerializer

"""
Class to handle the server messages

"""

__all__ = ["Message"]


class Message:

    def __init__(self, msgtype, content=None):
        self.type = msgtype
        self.content = content

    def __str__(self):
        return str({"type": self.type, "content": self.content})

    def Encode(msg, Serializer):
        if not isinstance(msg, Message):
            raise TypeError("argument must be an instance of Message")
        if not issubclass(Serializer, MessageSerializer):
            raise TypeError("argument must be subclass of "
                            "MessageSerializer")

        if msg.content is None:
            obj = {"type": msg.type}
        else:
            obj = {"type": msg.type, "content": msg.content}

        result = Serializer.Encode(obj)

        if isinstance(result, (bytes, bytearray)):
            return result
        else:
            return None

    def Decode(data, Serializer):
        if not issubclass(Serializer, MessageSerializer):
            raise TypeError("argument must be subclass of "
                            "MessageSerializer")

        result = Serializer.Decode(data)

        if isinstance(result, dict):
            type_data = result.get("type")
            content_data = result.get("content")
            if type_data is not None:
                return Message(type_data, content_data)

        return None
