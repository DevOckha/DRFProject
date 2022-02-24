from socket import send_fds
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Comment


@receiver(post_save, sender=User)
def do_somethin_when_user_created(sender, instance, created, **kwargs):
    """Kullanıcı oluşturulduğunda bir şeyler yapın"""
    if created == True and instance.is_active == True:
        pass