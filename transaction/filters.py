import django_filters
from .models import Transaction


class TransactionFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter()
    status = django_filters.ChoiceFilter(choices=Transaction.STATUS)
    full_sum = django_filters.RangeFilter()

    class Meta:
        model = Transaction
        fields = ['created_at', 'status', 'full_sum']
