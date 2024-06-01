from rest_framework import serializers
from . import models as m


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Transaction
        fields = '__all__'


class TransactionCreateSerializer(serializers.ModelSerializer):
    cvv = serializers.CharField(max_length=3)
    expired = serializers.CharField(max_length=10)
    account = serializers.CharField(max_length=50)
    client_id = serializers.CharField(max_length=200)
    client_secret = serializers.CharField(max_length=500)

    class Meta:
        model = m.Transaction
        fields = ['id', 'app', 'title',
                  'full_sum', 'status',
                  'created_at', 'updated_at',
                  'cvv', 'expired', 'account',
                  'client_id', 'client_secret']
