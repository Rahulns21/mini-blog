from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('myblog:home')

    name = models.CharField(max_length=50)

class UserProfile(models.Model):
    class Meta:
        verbose_name_plural = 'User Profiles'

    def __str__(self) -> str:
        return self.user.username

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(upload_to='images/profile/', blank=True, null=True)
    website_link = models.URLField(null=True, blank=True)
    instagram_link = models.URLField(null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)

class Post(models.Model):
    class Meta:
        verbose_name_plural ='Posts'

    def __str__(self) -> str:
        return self.title + ' | ' + self.author.username
    
    def get_absolute_url(self):
        return reverse('myblog:article-detail', args={str(self.id)})
    
    def total_likes(self):
        return self.likes.count()

    title = models.CharField(max_length=255)
    header_image = models.ImageField(blank=True, null=True, upload_to='images/')
    title_tag = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, 
                                null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    snippet = models.CharField(max_length=200)
    body = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_post', blank=True, null=True)

class Comment(models.Model):
    class Meta:
        verbose_name_plural = 'Comments'

    def __str__(self) -> str:
        return f"{self.name.username} - {self.post} - {self.body}"
    
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)