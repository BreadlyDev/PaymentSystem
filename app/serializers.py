from django.db.models import Sum
from rest_framework import serializers
from . import models as m

from user.serializers import UserSerializer


class AppSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    is_active = serializers.ReadOnlyField()

    class Meta:
        model = m.App
        fields = '__all__'


class AppCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.AppCredentials
        fields = '__all__'


class AppWithCredentialsSerializer(serializers.ModelSerializer):
    credentials = AppCredentialsSerializer(read_only=True)

    class Meta:
        model = m.App
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        credentials = instance.credentials
        representation['credentials'] = AppCredentialsSerializer(credentials).data
        return representation


class AppAnalyticsSerializer(serializers.ModelSerializer):
    income = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()

    class Meta:
        model = m.App
        fields = ['id', 'title', 'income', 'owner', 'account', 'is_active', 'created_at', 'updated_at', 'transactions']

    def get_transactions(self, obj):
        return obj.transactions.count()

    def get_income(self, obj):
        income = obj.transactions.aggregate(total_income=Sum('full_sum'))['total_income']
        return income or 0
