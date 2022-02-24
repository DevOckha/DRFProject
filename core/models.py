from xmlrpc.client import TRANSPORT_ERROR
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class MyUserManager(BaseUserManager):

    def create_user(self, email, username, password):

        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must be have an username')
        
        if not password:
            raise ValueError('User must have a password')

        user = self.model(
            email = self.normalize_email(email),
            username = username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self, email, username, password):
        
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password
        )

        user.is_admin = True
        user.save(using = self._db)
        return user
    

class User(AbstractBaseUser):

    email = models.EmailField(
        verbose_name= _('E-mail'),
        max_length = getattr(settings, 'USER_EMAIL_MAX_LENGTH', None),
        unique=True
    )

    username = models.CharField(
        verbose_name = _('Username'),
        max_length = getattr(settings, 'USER_USERNAME_MAX_LENGTH', None),
        unique = True,
        null = False
    )

    is_active = models.BooleanField(
        verbose_name = _('Actvie'),
        default = True
    )

    is_admin = models.BooleanField(
        verbose_name = _('Admin'),
        default = False
    )

    date_joined = models.DateTimeField(
        verbose_name = _('joined datetime'),
        auto_now_add = True,
        editable = False
    )

    object = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering  = ['-id']

    def __str__(self):
        return self.username
    

    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin


class Article(models.Model):
    
    author = models.ForeignKey(
        'User',
        related_name='articles'
    )

    title = models.CharField(
        verbose_name=_('Title'),
        max_length = getattr(settings, 'ARTICLE_TITLE_MAX_LENGTH', None)

    )

    context = models.TextField(
        verbose_name=_('Context'),
        max_length = getattr(settings, 'ARTICLE_CONTEXT_MAX_LENGTH', None)
    )

    hits = models.PositiveSmallIntegerField(
        verbose_name=_('Hits'),
        default=0
    )

    state_choices = (
        ('shown', 'Shown'),
        ('deleted', 'Deleted'),
    )

    state = models.CharField(
        verbose_name=_('State'),
        max_length=10,
        choices=state_choices,
        default='shown'
    )

    created_at = models.DateTimeField(
        verbose_name=_('Created datetime'),
        auto_now_add=True,
        editable=False
    )
    
    updated_at = models.DateTimeField(
        verbose_name=_('Updated datetime'),
        auto_now=True
    )


    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ['-id']

    def __str__(self):
        return self.title


class Comment(models.Model):

    article = models.ForeignKey(
        'Article',
        related_name='comments'
    )

    author = models.ForeignKey(
        'User',
        related_name='comments'
    )

    context = models.TextField(
        verbose_name=_('Context'),
        max_length = getattr(settings, 'COMMENT_CONTEXT_MAX_LENGTH', None)
    )

    state_choices = (
        ('shown', 'Shown'),
        ('deleted', 'Deleted'),
    )

    state = models.CharField(
        verbose_name=_('State'),
        max_length=10,
        choices=state_choices,
        default='shown'
    )

    created_at = models.DateTimeField(
        verbose_name=_('Created datetime'),
        auto_now_add=True,
        editable=False
    )

    updated_at = models.DateTimeField(
        verbose_name=_('Updated datetime'),
        auto_now=True,
    )

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['-id']
    
    def __str__(self):
        return self.id


