from rest_framework import serializers

class BaseSerializer(serializers.Serializer):
    @property
    def props(self):
        """Return an object with validated data as instance attributes."""
        class Props:
            def __init__(self, data):
                for key, value in data.items():
                    setattr(self, key, value)

            def to_dict(self):
                return self.__dict__

        return Props(self.validated_data)
