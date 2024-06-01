from rest_framework import serializers
from . import models as m

from app.serializers import AppSerializer


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
        fields = '__all__'

    def create(self, validated_data):
        cvv = validated_data.pop('cvv', None)
        expired = validated_data.pop('expired', None)
        account = validated_data.pop('account', None)
        client_id = validated_data.pop('client_id', None)
        client_secret = validated_data.pop('client_secret', None)

        transaction = m.Transaction.objects.create(**validated_data)
        return transaction

    def process_extra_fields(self, cvv, expired, account, client_id, client_secret):
        pass
