from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Q

from .constants import MAX_LENGTH

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=MAX_LENGTH, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="Слаг")
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name="Текст публикации")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор"
    )
    image = models.ImageField(
        upload_to="posts/", null=True, blank=True, verbose_name="Изображение"
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Сообщество",
    )

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"

        default_related_name = "posts"

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name="Публикация"
    )
    text = models.TextField(verbose_name="Комментарий")
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        default_related_name = "comments"

    def __str__(self):
        return self.author


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор",
    )

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

        constraints = [
            models.UniqueConstraint(
                fields=("user", "following"), name="unique_user_following"
            ),
            models.CheckConstraint(
                check=~Q(user=F("following")), name="check_self_follow"
            ),
        ]

        def __str__(self):
            return self.user
