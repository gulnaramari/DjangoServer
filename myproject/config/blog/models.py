from django.db import models

from django.utils import timezone


class Post(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
        help_text="Введите заголовок",
    )
    content = models.TextField(
        verbose_name="Содержимое",
        help_text="Введите содержимое",
    )
    image = models.ImageField(
        upload_to="images/",
        blank=True,
        null=True,
        verbose_name="Фотография",
        help_text="Загрузите фотографию",
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        help_text="Введите дату создания",
        default=timezone.now
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано"
    )
    views = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество просмотров"
    )

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["views"]

    def __str__(self):
        return self.title
