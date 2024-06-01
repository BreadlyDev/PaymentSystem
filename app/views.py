from rest_framework import generics, status, permissions, response as r
from rest_framework.exceptions import NotFound

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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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
    serializer_class = s.AppSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()

        if self.request.user.is_superuser:
            return super().get_object()

        try:
            app = queryset.get(pk=self.kwargs['pk'], owner=self.request.user)
        except m.App.DoesNotExist:
            raise NotFound('App not found or you do not have permission to access it')

        return app
