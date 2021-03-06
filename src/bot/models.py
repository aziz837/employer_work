from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=80 )
    parend_id = models.IntegerField( null=True, blank=False)
    last_time = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.title

class Region(models.Model):
    title = models.CharField(max_length=80 )
    def __str__(self):
        return self.title

class District(models.Model):
    title = models.CharField(max_length=80 )
    region = models.ForeignKey(Region, on_delete=models.CASCADE , null=True)
    def __str__(self):
        return self.title

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    tg_id = models.BigIntegerField( blank=True, null=True)
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
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    description = models.TextField(null=True)
    location = models.CharField(max_length=100)
    Region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)
    create_at = models.DateTimeField(auto_now=True, blank=True)

class UserRegion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        unique_together = [['user', 'region', 'district']]
