import secrets
import uuid

from django.db import models

from user.models import User


class App(models.Model):
    title = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apps')
    account = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'business_apps'
        verbose_name = 'Приложение'
        verbose_name_plural = 'Приложения'

    def create_credentials(self):
        client_id = str(uuid.uuid4())
        client_secret = secrets.token_urlsafe(50)

        credentials = AppCredentials.objects.create(
            app=self,
            client_id=client_id,
            client_secret=client_secret
        )

        return credentials

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.credentials:
            self.create_credentials()
        super().save()
    
    def __str__(self):
        return f'Приложение {self.title} пользователя {self.owner}'


class AppCredentials(models.Model):
    client_id = models.CharField(max_length=200)
    client_secret = models.CharField(max_length=500)
    app = models.OneToOneField(App, on_delete=models.CASCADE, related_name='credentials')

    class Meta:
        db_table = 'apps'
        verbose_name = 'Реквизит приложения'
        verbose_name_plural = 'Реквизиты приложения'

    def __str__(self):
        return f'Реквизиты приложения {self.app.title}'
