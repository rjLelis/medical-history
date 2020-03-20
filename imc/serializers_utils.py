from datetime import date


class BaseProfile:
    """
    Inherited whenever a Profile is the main model on the serializer
    """

    def get_full_name(self, obj):
        """
        Returns the full name of a Profile
        use full_name = serializers.SerializerMethodField()
        """
        return f'{obj.first_name} {obj.last_name}'

    def get_age(self, obj):
        """
        Returns the age of a Profile
        use age = SerializerMethodField(source='get_age')
        """
        return date.today().year - obj.date_of_birth.year \
            if obj.date_of_birth is not None else ''
