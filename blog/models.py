from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
from time import time
from PIL import Image
from resizeimage import resizeimage

# Create your models here.
def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + "-" + str(int(time()))

class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = 'published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    body = models.TextField(blank=True, db_index=True)
    publish = models.DateTimeField(default=timezone.now)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    image = models.ImageField(upload_to='img/', blank=True)
    objects = models.Manager()#Менеджер по умолчанию
    published = PublishManager()#Наш новый менеджер
    comment = models.TextField(max_length=150, blank=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    categories = models.ForeignKey('Category', on_delete=models.SET_NULL, related_name='posts', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})


    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

        if self.image:
            width = self.image.width
            height = self.image.height
            filepath = self.image.path

            if width > 690:
                img = Image.open(filepath)

                img = resizeimage.resize_cover(img, [690, int((height / width) * 690)] )
                img.save(filepath, img.format)


    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('category_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('category_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('category_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Comment(models.Model):

    class Meta:
        db_table = 'comments'
        ordering = ('-pub_date',)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    content = models.TextField('Comments')
    pub_date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    moderate = models.BooleanField(default=True)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.author.get_full_name, self.post)

