from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

     path(
        'add-farm/',
        views.add_farm,
        name='add_farm'
    ),

    path(
    'farm/<int:farm_id>/',
    views.farm_details,
    name='farm_details'
    ),

path(
    'farm/<int:farm_id>/add-expense/',
    views.add_expense,
    name='add_expense'
),

path(
    'farm/<int:farm_id>/profit-loss/',
    views.profit_loss,
    name='profit_loss'
),
path(
    'farm/<int:farm_id>/add-harvest/',
    views.add_harvest,
    name='add_harvest'
),
path(
    'harvest/<int:harvest_id>/edit/',
    views.edit_harvest,
    name='edit_harvest'
),
path(
    'farm/<int:farm_id>/harvest-details/',
    views.harvest_details,
    name='harvest_details'
),
path(
    'my-farms/',
    views.my_farms,
    name='my_farms'
),
path(
    'settings/',
    views.settings_page,
    name='settings_page'
),
]