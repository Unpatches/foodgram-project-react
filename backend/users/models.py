from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=254,
        verbose_name='Имя пользователя',
        help_text='Введите имя пользователя',
        unique=True
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Адрес электронной почты',
        help_text='Введите email',
        unique=True
    )
    first_name = models.CharField(
        max_length=254,
        verbose_name='Имя',
        help_text='Введите имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=254,
        verbose_name='Фамилия',
        help_text='Введите фамилию',
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
        help_text="Пользователь"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор",
        help_text="Создатель постов"
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'],
            name='unique_following'
        )]
