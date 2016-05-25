import json

__all__ = ["MessageSerializer", "JsonSerializer"]


class MessageSerializer:
    def Encode(obj):
        raise NotImplementedError("Encode method should be implemented "
                                  "in child members")

    def Decode(data):
        raise NotImplementedError("Decode method should be implemented "
                                  "in child members")


class JsonSerializer(MessageSerializer):
    def Encode(obj):
        try:
            return json.dumps(obj).encode("UTF-8")
        except:
            return None

    def Decode(data):
        try:
            return json.loads(data.decode("UTF-8"))
        except:
            return None
