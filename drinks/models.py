from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        db_table = "categories"

class Size(models.Model):
    name_kr     = models.CharField(max_length=32, null=True)
    name_en     = models.CharField(max_length=32, null=True)
    milliliter  = models.DecimalField(max_digits=4, decimal_places=3)
    fluid_ounce = models.DecimalField(max_digits=4, decimal_places=3)

    class Meta:
        db_table = "sizes"

class Allergen(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = "allergens"

class Nutrition(models.Model):
    calorie       = models.DecimalField(max_digits=5, decimal_places=3)
    saturated_fat = models.DecimalField(max_digits=5, decimal_places=3)
    protein       = models.DecimalField(max_digits=5, decimal_places=3)
    sodium        = models.DecimalField(max_digits=5, decimal_places=3)
    sugar         = models.DecimalField(max_digits=5, decimal_places=3)
    caffeine      = models.DecimalField(max_digits=5, decimal_places=3)

    class Meta:
        db_table = "nutritions"

class Drink(models.Model):
    name_kr   = models.CharField(max_length=128)
    name_en   = models.CharField(max_length=128)
    category  = models.ForeignKey("Category", on_delete=models.CASCADE)
    size      = models.ForeignKey("Size", on_delete=models.CASCADE)
    nutrition = models.OneToOneField("Nutrition", on_delete=models.CASCADE)
    allergens = models.ManyToManyField("Allergen")

    class Meta:
        db_table = "drinks"

class Description(models.Model):
    content = models.TextField()
    drink   = models.ForeignKey("Drink", on_delete=models.CASCADE)

    class Meta:
        db_table = "descriptions"

class Image(models.Model):
    url   = models.URLField(max_length=400)
    drink = models.ForeignKey("Drink", on_delete=models.CASCADE)

    class Meta:
        db_table = "images"