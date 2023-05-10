from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from django.core.files import File
from PIL import Image
from io import BytesIO  

class Category(models.Model):
    name = models.CharField(max_length=255)
    plural_name = models.CharField(max_length=255)
    slug = models.SlugField()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # для доступа к ссылке
        return f'/{self.slug}/'

class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    plural_name = models.CharField(max_length=255)
    slug=models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    plural_name = models.CharField(max_length=255)
    slug=models.SlugField(blank=True,null=True)

    def __str__(self):
        return self.name

class Comments(models.Model):
    user = models.ForeignKey(User, related_name='user_comment', on_delete=models.CASCADE)

    heading = models.CharField(max_length=100)
    score = models.IntegerField(default = 1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at',]

    def __str__(self):
        return self.heading


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    slug = models.SlugField()       
    # subcategory = models.CharField(max_length=255, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)

    # manufacturer = models.CharField(max_length=255, null=True, blank=True)
    #                               значит что поле необязятельно

    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)
    sales = models.IntegerField(default=0)


    comments = models.ManyToManyField(Comments, related_name='comment', blank=True)
    type = models.CharField(max_length=255)
    processor = models.CharField(max_length=255)
    videocart = models.CharField(max_length=255)
    hdd = models.CharField(max_length=255)
    ram = models.CharField(max_length=255)

    class Meta:
        ordering = ('-date_added', )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            # в таком формате передаем фото
            return 'http://127.0.0.1:8000' + self.image.url
        else:
            return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else: 
            if self.image:  
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    
    def make_thumbnail(self, image, size=(200,133)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=100)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

class Shop(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(default='none')
    
    def __str__(self):
        return self.name