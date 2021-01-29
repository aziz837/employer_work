from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=80 )
    parend_id = models.IntegerField( null=True, blank=False)
    last_time = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.title

class Region(models.Model):
    title = models.CharField(max_length=80 )
    parend_id = models.IntegerField( null=True, blank=False)

    def __str__(self):
        return self.title

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    tg_id = models.BigIntegerField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    type_work = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.first_name
class UserCategory(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField
    location = models.CharField(max_length=100)
    district = models.ForeignKey(Region, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now=True, blank=True)

