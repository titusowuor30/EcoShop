from PIL import Image
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.db import models
from io import BytesIO

from apps.vendor.models import Vendor

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='products', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    additional_info = models.TextField(max_length=255, default=description)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/')
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, default='primary')

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title

    @property
    def getImageURL(self):
        if self.image.url and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return None

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.makethumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x180.jpg'

    def makethumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail
