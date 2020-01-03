from datetime import date


class BaseProfile:
    """
    Inherited whenever a Profile is the main model on the serializer
    """

    def get_full_name(self, obj):
        """
        Use serializers.SerializerMethodField(source='get_full_name')
        """
        return f'{obj.first_name} {obj.last_name}'

    def get_age(self, obj):
        """
        Use serializers.SerializerMethodField(source='get_age')
        """
        return date.today().year - obj.date_of_birth.year \
            if obj.date_of_birth is not None else ''
