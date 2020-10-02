from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    favorite_food = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.email
#user get by id
#user update by id
#user.disconnect (cookies)
#user.connect (cookies)