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
        return json.dumps(obj).encode("UTF-8")

    def Decode(data):
        return json.loads(data.decode("UTF-8"))
