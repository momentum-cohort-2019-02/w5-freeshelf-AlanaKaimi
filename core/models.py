from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Category(models.Model):
    """Model representing a book genre."""
    
    name = models.CharField(max_length=200, help_text='Enter a Category (e.g. Python)')
    
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.set_slug()
        super().save(*args, **kwargs)

    def set_slug(self):
        # If the slug is already set, stop here
        if self.slug:
            return

        base_slug = slugify(self.name)
        slug = base_slug
        n = 0

        # while we can find a record already in the DB with the slug we're trying to use
        while Category.objects.filter(slug=slug).count():
            n += 1
            slug = base_slug + "-" + str(n)    
        self.slug = slug

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """String for representing the Model object."""
        return self.name


class Book(models.Model):
    """Model representing a book"""
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    categories = models.ManyToManyField(Category, blank=True)
    date_added = models.DateField(auto_now_add=True)

    # Worked through by comparing to Chinh's code.
    favorited_by = models.ManyToManyField(to=User, related_name='favorite_books', through='Favorite')
    
    image = models.ImageField(upload_to='books/', blank=True, null=True)

    url = models.URLField(max_length=250)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['-date_added']

    def display_category(self):
        """Create a string for the Category. This is required to display category in Admin."""
        return ', '.join(category.name for category in self.category.all()[:3])
    display_category.short_description = 'category'

# From lecture 3-12 on Slugs
    def save(self, *args, **kwargs):
        self.set_slug()
        super().save(*args, **kwargs)

    def set_slug(self):
        # If the slug is already set, stop here
        if self.slug:
            return

        base_slug = slugify(self.title)
        slug = base_slug
        n = 0
        # while we can find a record already in the DB with the slug we're trying to use
        while Book.objects.filter(slug=slug).count():
            n += 1
            slug = base_slug + "-" + str(n)        
        self.slug = slug

    def get_absolute_url(self):
        """Returns the url to access the home page."""
        return reverse('index')

    def __str__(self):
        """String for representing the Model object."""
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
