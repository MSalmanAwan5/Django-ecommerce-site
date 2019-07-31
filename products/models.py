from django.db import models
from django.db.models import Q
import random
# Create your models here.
from ecommerece.utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.urls import reverse

def upload_file_path(instance, filename):
    new_filename = random.randint(1, 123456789)
    # final_filename, ext = get_file_Ext(filename)
    final = "products/{new_filename}".format(new_filename=new_filename)
    print(final)
    return final


class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True)
    def search(self, query):
        lookups = (
                    Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(price__iexact=query)
                    )
        return self.filter(lookups).distinct()
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    def search(self, query):
        return self.get_queryset().search(query)


class Products(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(blank=True)
    description = models.CharField(max_length=500)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    image = models.ImageField(upload_to=upload_file_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    objects = ProductManager()
    def get_absolute_url(self):

        if self.featured:
            #return "/products/featured-detail/{slug}/".format(slug=self.slug)
            return reverse("products:featured-detail", kwargs={"slug": self.slug})
        else:
            #return "/products/detail/{slug}/".format(slug=self.slug)
            return reverse("products:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, Products)


class FormRegister(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.EmailField(max_length=20)
    password = models.CharField(max_length=10)
    ConfirmPassword = models.CharField(max_length=10)

    def __str__(self):
        return self.firstname
