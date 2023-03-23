from django.core.management.base import CommandError, BaseCommand
from ...models import Product, Category
import factory
from django.utils.text import slugify
import random
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile



class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Faker('word')
    description = factory.Faker('sentence')
    slug = factory.lazy_attribute(lambda obj: slugify(obj.title))


def generate_random_image():
    color = tuple(random.randint(0, 255) for _ in range(3))

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('sentence',nb_words=3)
    description = factory.Faker('sentence')
    slug = factory.lazy_attribute(lambda obj: slugify(obj.name))
    price = factory.Faker('pyfloat',min_value=777.0,max_value=99999.0)
    discount_price = factory.Faker('pyfloat',min_value=100.0,max_value=500.0)    
    brand = factory.Faker('word')

class Command(BaseCommand):
    help = 'Populate the database with fake data.'

    def handle(self, *args, **options):
        # Create 10 categories
        # categories = CategoryFactory.create_batch(5)
        categories = Category.objects.all()

        for category in categories:
            ProductFactory.create_batch(1000, category=category,image = factory.django.ImageField(color= tuple(random.randint(0, 255) for _ in range(3)) , width=200,height=200))

        self.stdout.write(self.style.SUCCESS('Data populated successfully.'))