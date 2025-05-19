from django.core.management.base import BaseCommand

from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'Add products to the database'

    def handle(self, *args, **options):
        category, _ = Category.objects.get_or_create(category_name="Крупа", description="Рассыпчатые зерна")


        products = [
            {'product_name': "Гречка", 'description': "Коричневого цвета", 'category': category, 'price': 100},
            {'product_name': "Рис", 'description': "В основном белого цвета", 'category': category, 'price': 100},
        ]

        for product in products:
            products, created = Product.objects.get_or_create(**product)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Успешное создание продукта: {products.product_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Продукт {products.product_name} уже существует'))
