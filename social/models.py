from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)
    email = models.EmailField()

class Post(models.Model):
    user = models.ForeignKey(User, related_name="user_post")

    title = models.TextField()
    added = models.DateTimeField()
    text = models.TextField(max_length=24)

class Like(models.Model):
    user = models.ForeignKey(User, related_name="user_post")
    added = models.DateTimeField()