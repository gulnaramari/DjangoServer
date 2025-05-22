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
            raise ValidationError(f'Уберите некорректные слова!')


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
                   ]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
                'class': 'form-control',  # Добавление CSS-класса для стилизации поля
                'placeholder': 'Введите название продукта'
            })
        self.fields['description'].widget.attrs.update({
                'class': 'form-control',  # Добавление CSS-класса для стилизации поля
                'placeholder': 'Введите описание'
            })
        self.fields["published_status"].widget.attrs.update(
            {
                "class": "form-check-input",
            }
        )

        self.fields['image'].widget.attrs.update({
                'class': 'form-control',  # Добавление CSS-класса для стилизации поля
                'accept': 'image/*'
            })
        self.fields['category'].widget.attrs.update({
                'class': 'form-control'  # Добавление CSS-класса для стилизации поля
            })
        self.fields['purchase_price'].widget.attrs.update({
                'class': 'form-control',  # Добавление CSS-класса для стилизации поля
                'placeholder': 'Введите цену'
            })

    def clean(self):
        cleaned_data = super().clean()
        product_name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        validate_no_forbidden_words(product_name)
        validate_no_forbidden_words(description)

    def clean_price(self):
        price = self.cleaned_data.get['purchase_price']
        if price < 0:
            raise ValidationError('Цена не должна быть отрицательной')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            validate_image(image)
        return image
