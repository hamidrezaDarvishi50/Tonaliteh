import django_filters
from .models import Art

class ArtFilter(django_filters.FilterSet):

    class Meta:
        model = Art
        fields = [
            "artist",
            "category",
        ]