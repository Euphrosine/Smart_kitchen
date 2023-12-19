from django.db import models

class KitchenData(models.Model):
    temperature = models.FloatField()
    gas_level = models.FloatField()
    humidity = models.FloatField()
    flame = models.BooleanField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"KitchenData - {self.datetime}"


class Lamp(models.Model):
    status = models.IntegerField(default=1)

class Fan(models.Model):
    status = models.IntegerField(default=1)

# stock management part
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Meal(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, related_name='meals')

    def __str__(self):
        return self.name