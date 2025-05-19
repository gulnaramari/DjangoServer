from django.db import models
from django.utils import timezone
from django.conf import settings


class Contacts(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Имя и Фамилия",
        help_text="Введите ваше имя и фамилию",
    )

    message = models.TextField(
        verbose_name="Сообщение",
        help_text="Введите ваше сообщение",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ["name", "message"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Название категории",
        help_text="Введите название категории",
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание категории",
        help_text="Введите описание категории",
    )
    category_updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Последняя модификация"
    )

    def __str__(self):
        return f"name: {self.name}, description: {self.description}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["name", "description"]


class Product(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
    ]

    name = models.CharField(
        max_length=150,
        verbose_name="Название продукта",
        help_text="Введите название продукта",
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание продукта",
        help_text="Введите описание продукта",
    )

    image = models.ImageField(
        upload_to="images/",
        blank=True,
        null=True,
        verbose_name="Фотография",
        help_text="Загрузите фотографию продукта",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Название категории",
        help_text="Введите название категории",
        blank=True,
        null=True,
        related_name="products",
    )

    purchase_price = models.DecimalField(
        blank=True,
        default=0.0,
        verbose_name="Цена",
        help_text="Введите цену продукта",
        decimal_places=2,
        max_digits=100
    )

    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        help_text="Введите дату создания",
        default=timezone.now
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата изменения",
        help_text="Введите дату изменения",
        default=timezone.now
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )



    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["name", "description"]
        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта'),
        ]

    def __str__(self):
        return f"""
        name: {self.name}, description: {self.description}
                """
