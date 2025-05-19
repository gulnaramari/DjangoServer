import os
from django import forms
from .models import Product
from django.core.exceptions import ValidationError

# Список запрещённых слов
FORBIDDEN_WORDS = {"казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"}


def validate_no_forbidden_words(value):
    lower_value = value.lower()
    for word in FORBIDDEN_WORDS:
        if word in lower_value:
            raise ValidationError(f'Уберите спам!')


def validate_image(image):
    # Проверяем размер (5MB = 5 * 1024 * 1024 байт)
    max_size = 5 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError("Размер изображения не должен превышать 5MB.")

    # Проверяем формат (только JPEG и PNG)
    valid_extensions = {'.jpg', '.jpeg', '.png'}
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError("Допустимые форматы изображений: JPEG, PNG.")

class ProductModeratorForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "published_status",
        ]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name',
                  'description',
                  'published_status',
                  'image',
                  'category',
                  'purchase_price',
                  'created_at',
                  'updated_at', ]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
                'class': 'form-control',  # Добавление CSS-класса для стилизации поля
                'placeholder': 'Введите название продукта'  # Текст подсказки внутри поля
            })
        self.fields['description'].widget.attrs.update({
                'class': 'form-control',  # Добавление CSS-класса для стилизации поля
                'placeholder': 'Введите описание'  # Текст подсказки внутри поля
            })
        self.fields["published_status"].widget.attrs.update(
            {
                "class": "form-check-input",
            }
        )

        self.fields['image'].widget.attrs.update({
                'class': 'form-control',  # Добавление CSS-класса для стилизации поля
                'accept': 'image/*'  # Разрешаем только изображения
            })
        self.fields['category'].widget.attrs.update({
                'class': 'form-control'  # Добавление CSS-класса для стилизации поля
            })
        self.fields['purchase_price'].widget.attrs.update({
                'class': 'form-control',  # Добавление CSS-класса для стилизации поля
                'placeholder': 'Введите цену'  # Текст подсказки внутри поля
            })
        self.fields['created_at'].widget.attrs.update({
                'class': 'form-control',  # Добавление CSS-класса для стилизации поля
                'type': 'date'  # Указание типа поля как даты
            })
        self.fields['updated_at'].widget.attrs.update({
                'class': 'form-control',  # Добавление CSS-класса для стилизации поля
                'type': 'date'  # Указание типа поля как даты
            })

    def clean_name(self):
        name = self.cleaned_data.get("name")
        for word in FORBIDDEN_WORDS:
            if word in name.lower():
                raise ValidationError('Вы используете запретное слово в названии продукта: "{}"'.format(word))

    def clean_description(self):
        description = self.cleaned_data.get("description")
        for word in FORBIDDEN_WORDS:
            if word in description.lower():
                raise ValidationError('Вы используете запретное слово в описании продукта: "{}"'.format(word))
        return description

    def clean_price(self):
        price = self.cleaned_data.get("purchase_price")
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        return price

