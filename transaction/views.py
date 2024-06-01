import requests
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, permissions, views, response as r
from . import models as m, serializers as s, filters as f


class TransactionListAPIView(generics.ListAPIView):
    queryset = m.Transaction.objects.all()
    serializer_class = s.TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = f.TransactionFilter

    # def get_queryset(self):
    #     # if self.request.user.is_superuser:
    #     return self.queryset

        # return self.queryset.filter(app=self.request.user.apps)


class TransactionCreateAPIView(generics.CreateAPIView):
    serializer_class = s.TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransactionDataGetAPIView(generics.CreateAPIView):
    serializer_class = s.TransactionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        super().post(request, args, kwargs)


class TransactionSendAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = s.TransactionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        external_url = 'http://localhost:8080/transactions/'
        try:
            external_response = requests.post(
                external_url,
                json=serializer.validated_data,
            )
            external_response.raise_for_status()

            return r.Response(external_response.json(), status=external_response.status_code)
        except requests.exceptions.RequestException as e:
            return r.Response({'detail': str(e)}, status=status.HTTP_502_BAD_GATEWAY)


class TransactionChangeAPIView(generics.RetrieveUpdateAPIView):
    queryset = m.Transaction.objects.all()
    serializer_class = s.TransactionCreateSerializer
