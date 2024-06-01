from rest_framework import generics, status, permissions, response as r
from . import models as m, serializers as s


class AppListAPIView(generics.ListAPIView):
    queryset = m.App.objects.all()
    serializer_class = s.AppWithCredentialsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset

        return self.queryset.filter(owner=self.request.user.id)


class AppCreateAPIView(generics.CreateAPIView):
    serializer_class = s.AppSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = self.request.data
        data['owner'] = self.request.user

        super().create(request, args, kwargs)


class AppAnalyticsAPIView(generics.ListAPIView):
    queryset = m.App.objects.all()
    serializer_class = s.AppAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset

        return self.queryset.filter(owner=self.request.user.id)


class AppAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = m.App.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        if self.request.user.is_superuser:
            return self.queryset

        return self.queryset.filter(owner=self.request.user.id)
