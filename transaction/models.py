import uuid

from django.db import models
from app.models import App


class Transaction(models.Model):
    STATUS = (
        ('Размещен', 'Размещен'),
        ('Отменен', 'Отменен'),
        ('В обработке', 'В обработке'),
        ('Исполнен', 'Исполнен'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='transactions')
    title = models.CharField(max_length=150)
    full_sum = models.FloatField()
    status = models.CharField(max_length=150, choices=STATUS, default=STATUS[0][1])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return f'Транзакция {self.title}'
