from .MessageSerializer import MessageSerializer

"""
Class to handle the server messages

"""

__all__ = ["Message"]


class Message:

    def __init__(self, msgtype, contents=None):
        self.type = msgtype
        self.contents = contents

    def __str__(self):
        return str({"type": self.type, "contents": self.contents})

    def Encode(msg, serializer):
        if not isinstance(msg, Message):
            raise TypeError("argument must be an instance of Message")
        if not issubclass(serializer, MessageSerializer):
            raise TypeError("argument must be subclass of "
                            "MessageSerializer")
        obj = {"type": msg.type, "contents": msg.contents}
        return serializer.Encode(obj)

    def Decode(data, serializer):
        if not issubclass(serializer, MessageSerializer):
            raise TypeError("argument must be subclass of "
                            "MessageSerializer")
        result = serializer.Decode(data)
        if "type" in result and "contents" in result:
            return Message(result["type"], result["contents"])
        else:
            # decode error
            pass
