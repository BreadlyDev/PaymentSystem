import requests
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, permissions, response as r
from rest_framework.response import Response

from . import models as m, serializers as s, filters as f


class TransactionListAPIView(generics.ListAPIView):
    queryset = m.Transaction.objects.all()
    serializer_class = s.TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = f.TransactionFilter

    def get_queryset(self):
        user_apps = self.request.user.apps.all()
        return m.Transaction.objects.filter(app__in=user_apps)


class TransactionCreateAPIView(generics.CreateAPIView):
    serializer_class = s.TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        super().post()


class TransactionDataGetAPIView(generics.CreateAPIView):
    serializer_class = s.TransactionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        super().post(request, args, kwargs)


class TransactionSendAPIView(generics.CreateAPIView):
    serializer_class = s.TransactionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = s.TransactionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        external_url = 'http://localhost:8080/transactions/'
        payload = {
            'from_card': m.App.objects.get(id=data['app'].id).account,
            'to_card_number': data['account'],
            'amount': str(data['full_sum']),
        }

        try:
            print(f"Sending payload to external service: {payload}")
            external_response = requests.post(external_url, json=payload)
            external_response.raise_for_status()
            return Response(external_response.json(), status=external_response.status_code)
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            return Response({'detail': str(e)}, status=status.HTTP_502_BAD_GATEWAY)


class TransactionChangeAPIView(generics.RetrieveUpdateAPIView):
    queryset = m.Transaction.objects.all()
    serializer_class = s.TransactionCreateSerializer
