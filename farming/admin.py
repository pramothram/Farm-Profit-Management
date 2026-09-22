from django.contrib import admin
from .models import Farm, Expense, Harvest


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = (
        'crop_name',
        'land_size',
        'land_unit',
        'planting_date',
        'expected_harvest_date',
        'user',
    )


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'purpose',
        'category',
        'amount',
        'farm',
    )

    list_filter = (
        'category',
        'date',
    )


@admin.register(Harvest)
class HarvestAdmin(admin.ModelAdmin):
    list_display = (
        'farm',
        'date',
        'quantity',
        'unit',
        'selling_price',
    )