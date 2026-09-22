from django.db import models
from django.contrib.auth.models import User


class Farm(models.Model):
    LAND_UNITS = [
        ('acre', 'Acre'),
        ('cent', 'Cent'),
        ('hectare', 'Hectare'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    crop_name = models.CharField(max_length=100)

    land_size = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    land_unit = models.CharField(
        max_length=20,
        choices=LAND_UNITS,
        default='acre'
    )

    planting_date = models.DateField()

    expected_harvest_date = models.DateField(
        null=True,
        blank=True
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.crop_name} - {self.land_size} {self.land_unit}"


class Expense(models.Model):

    CATEGORY_CHOICES = [
        ('seeds', 'Seeds'),
        ('fertilizer', 'Fertilizer'),
        ('pesticide', 'Pesticide'),
        ('labour', 'Labour'),
        ('machinery', 'Machinery'),
        ('irrigation', 'Irrigation'),
        ('transport', 'Transport'),
        ('other', 'Other'),
    ]

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name='expenses'
    )

    date = models.DateField()

    purpose = models.CharField(
        max_length=255
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.date} - {self.purpose} - ₹{self.amount}"


class Harvest(models.Model):

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name='harvests'
    )

    date = models.DateField()

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    unit = models.CharField(
        max_length=20,
        default='kg'
    )

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    notes = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.farm} - {self.quantity} {self.unit}"