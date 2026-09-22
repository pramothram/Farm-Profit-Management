from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from .models import Farm, Expense, Harvest
from django.db.models import Sum
from .forms import FarmForm, ExpenseForm, HarvestForm
from decimal import Decimal
from django.contrib.auth import authenticate, login, logout

def register_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                'Account created successfully!'
            )

            return redirect('dashboard')

    else:
        form = RegisterForm()

    return render(
        request,
        'farming/register.html',
        {'form': form}
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(
        request,
        'farming/login.html'
    )


def logout_view(request):

    logout(request)

    return redirect('login')


@login_required(login_url='login')
def dashboard(request):

    # Get only this farmer's farms
    farms = Farm.objects.filter(
        user=request.user
    ).order_by('-created_at')

    # Get only this farmer's expenses
    expenses = Expense.objects.filter(
        farm__user=request.user
    )

    # Get only this farmer's harvests
    harvests = Harvest.objects.filter(
        farm__user=request.user
    )

    # Total expenses
    total_expenses = expenses.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')

    # Total income
    total_income = Decimal('0')

    for harvest in harvests:
        total_income += (
            harvest.quantity * harvest.selling_price
        )

    # Profit / Loss
    profit = Decimal('0')
    loss = Decimal('0')

    if total_income > total_expenses:
        profit = total_income - total_expenses

    elif total_expenses > total_income:
        loss = total_expenses - total_income

    context = {
        'farms': farms,
        'expenses': expenses,
        'harvests': harvests,

        'total_farms': farms.count(),

        'total_expenses': total_expenses,
        'total_income': total_income,

        'profit': profit,
        'loss': loss,
    }

    return render(
        request,
        'farming/dashboard.html',
        context
    )

@login_required(login_url='login')
def add_farm(request):

    if request.method == 'POST':

        form = FarmForm(request.POST)

        if form.is_valid():

            farm = form.save(commit=False)

            # Connect farm to logged-in farmer
            farm.user = request.user

            farm.save()

            messages.success(
                request,
                'Farm added successfully!'
            )

            return redirect('dashboard')

    else:

        form = FarmForm()

    return render(
        request,
        'farming/add_farm.html',
        {
            'form': form
        }
    )
@login_required(login_url='login')
def add_expense(request, farm_id):

    farm = get_object_or_404(
        Farm,
        id=farm_id,
        user=request.user
    )

    if request.method == 'POST':

        form = ExpenseForm(request.POST)

        if form.is_valid():

            expense = form.save(commit=False)

            expense.farm = farm

            expense.save()

            messages.success(
                request,
                'Expense added successfully!'
            )

            return redirect(
                'farm_details',
                farm_id=farm.id
            )

    else:

        form = ExpenseForm()

    return render(
        request,
        'farming/add_expense.html',
        {
            'form': form,
            'farm': farm
        }
    )

@login_required(login_url='login')
def farm_details(request, farm_id):

    farm = get_object_or_404(
        Farm,
        id=farm_id,
        user=request.user
    )

    expenses = farm.expenses.all().order_by('-date')

    total_expenses = sum(
        expense.amount for expense in expenses
    )

    return render(
        request,
        'farming/farm_details.html',
        {
            'farm': farm,
            'expenses': expenses,
            'total_expenses': total_expenses,
        }
    )

@login_required(login_url='login')
def profit_loss(request, farm_id):

    farm = get_object_or_404(
        Farm,
        id=farm_id,
        user=request.user
    )

    expenses = farm.expenses.all()

    harvests = farm.harvests.all()

    # Calculate total expenses
    total_expenses = sum(
        (expense.amount for expense in expenses),
        Decimal('0')
    )

    # Calculate total income
    total_income = sum(
        (
            harvest.quantity * harvest.selling_price
            for harvest in harvests
        ),
        Decimal('0')
    )

    # Calculate profit or loss
    profit_loss_amount = total_income - total_expenses

    # Decide whether profit or loss
    if profit_loss_amount > 0:
        result = 'Profit'
    elif profit_loss_amount < 0:
        result = 'Loss'
    else:
        result = 'Break Even'

    return render(
        request,
        'farming/profit_loss.html',
        {
            'farm': farm,
            'total_expenses': total_expenses,
            'total_income': total_income,
            'profit_loss_amount': abs(profit_loss_amount),
            'result': result,
            'expenses': expenses,
            'harvests': harvests,
        }
    )
@login_required(login_url='login')
def add_harvest(request, farm_id):
    farm = get_object_or_404(
        Farm,
        id=farm_id,
        user=request.user
    )

    # Allow only ONE harvest for each farm
    if farm.harvests.exists():
        messages.warning(
            request,
            'Harvest data already exists. You can edit the existing harvest.'
        )
        return redirect(
            'profit_loss',
            farm_id=farm.id
        )

    if request.method == 'POST':
        form = HarvestForm(request.POST)

        if form.is_valid():
            harvest = form.save(commit=False)
            harvest.farm = farm
            harvest.save()

            messages.success(
                request,
                'Harvest income added successfully!'
            )

            return redirect(
                'profit_loss',
                farm_id=farm.id
            )

    else:
        form = HarvestForm()

    return render(
        request,
        'farming/add_harvest.html',
        {
            'form': form,
            'farm': farm
        }
    )
@login_required(login_url='login')
def edit_harvest(request, harvest_id):
    harvest = get_object_or_404(
        Harvest,
        id=harvest_id,
        farm__user=request.user
    )

    if request.method == 'POST':
        form = HarvestForm(request.POST, instance=harvest)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Harvest updated successfully!'
            )
            return redirect(
                'profit_loss',
                farm_id=harvest.farm.id
            )
    else:
        form = HarvestForm(instance=harvest)

    return render(
        request,
        'farming/edit_harvest.html',
        {
            'form': form,
            'harvest': harvest,
            'farm': harvest.farm,
        }
    )
@login_required(login_url='login')
def harvest_details(request, farm_id):

    farm = get_object_or_404(
        Farm,
        id=farm_id,
        user=request.user
    )

    harvest = farm.harvests.first()

    total_income = Decimal('0')

    if harvest:
        total_income = (
            harvest.quantity * harvest.selling_price
        )

    return render(
        request,
        'farming/harvest_details.html',
        {
            'farm': farm,
            'harvest': harvest,
            'total_income': total_income,
        }
    )
@login_required(login_url='login')
def my_farms(request):
    farms = Farm.objects.filter(user=request.user).order_by('-id')

    return render(
        request,
        'farming/my_farms.html',
        {
            'farms': farms
        }
    )
@login_required(login_url='login')
def settings_page(request):

    if request.method == 'POST':
        language = request.POST.get('language')

        if language in ['en', 'ta', 'hi']:
            request.session['language'] = language

        messages.success(
            request,
            'Language preference saved successfully!'
        )

        return redirect('settings_page')

    current_language = request.session.get('language', 'en')

    return render(
        request,
        'farming/settings.html',
        {
            'current_language': current_language
        }
    )