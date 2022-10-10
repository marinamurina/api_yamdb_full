import django_filters
from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')
    year = django_filters.NumberFilter(field_name='year')
    genre__slug = django_filters.CharFilter(lookup_expr='icontains')
    category__slug = django_filters.CharFilter(lookup_expr='icontains')

    class Meta():
        model = Title
        fields = (
            'name',
            'year',
            'genre',
            'category',
        )
