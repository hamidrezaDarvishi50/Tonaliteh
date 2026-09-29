import django_filters
from django.db.models import Case, When, Value, CharField, F
from .models import Art, Tag

class ArtFilter(django_filters.FilterSet):

    class Meta:
        model = Art
        fields = [
            "artist",
            "category",
        ]

def annotate_shape(queryset):
    return queryset.annotate(
        shape=Case(
            When(width=F("height"), then=Value("square")),
            When(width__gt=F("height"), then=Value("horizontal")),
            When(width__lt=F("height"), then=Value("vertical")),
            output_field=CharField(),
        )
    )

# and or logic implementation
def filter_arts_by_tags(queryset, tag_ids_by_type):
    for tag_type, ids in tag_ids_by_type.items():
        if ids:
            queryset = queryset.filter(tags__type=tag_type, tags__id__in=ids)
    return queryset.distinct() #remove duplicate arts

def search_arts(query_params):
    arts = annotate_shape(Art.objects.all())

    tag_ids_by_type = {}
    for tag_type, _ in Tag.TagType.choices:
        raw = query_params.get(tag_type)
        if raw:
            tag_ids_by_type[tag_type] = [int(i) for i in raw.split(",")]
    arts = filter_arts_by_tags(arts, tag_ids_by_type)

    year = query_params.get("year")
    if year:
        arts = arts.filter(released_year=year)

    artist_id = query_params.get("artist")
    if artist_id:
        arts = arts.filter(artist_id=artist_id)

    shape = query_params.get("shape")
    if shape:
        arts = arts.filter(shape=shape)

    return arts