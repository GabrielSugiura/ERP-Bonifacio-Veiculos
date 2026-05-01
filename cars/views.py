# cars/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Car, Sale, VehicleDocument, VehicleDocumentImage, AppConfiguration
from .forms import (
    CarForm,
    SaleForm,
    VehicleDocumentForm,
    AccessPasswordCreateForm,
    CredentialsUnlockForm,
    ItauCredentialsForm,
    ChangeAccessPasswordForm,
)

def car_update(request, pk):
    car = get_object_or_404(Car, pk=pk)

    form = CarForm(request.POST or None, request.FILES or None, instance=car)

    if form.is_valid():
        form.save()
        return redirect('cars_list')

    return render(request, 'cars/car_form.html', {
        'form': form,
        'editing': True,
        'car': car,
    })


def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if request.method == 'POST':
        car.delete()
        return redirect('cars_list')

    return render(request, 'cars/car_delete.html', {
        'car': car,
    })

def dashboard(request):
    
    carros = Car.objects.all()

    context = {
        'carros_venda': carros.count(),
        'carros_vendidos': 0,
        'total_investido': 0,
        'lucro_total': 0,
        'carros': carros[:5]
    }

    return render(request, 'cars/dashboard.html', context)

def cars_list(request):
    cars = Car.objects.all()
    return render(request, 'cars/cars_list.html', {'cars': cars})


def car_create(request):
    form = CarForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('cars_list')

    return render(request, 'cars/car_form.html', {'form': form})

def sold_cars_list(request):
    query = request.GET.get('q', '')

    sales = Sale.objects.select_related('car').all().order_by('-created_at')

    if query:
        sales = sales.filter(
            car__brand__icontains=query
        ) | sales.filter(
            car__model__icontains=query
        ) | sales.filter(
            car__plate__icontains=query
        )

    total_sales = sales.count()
    total_value = sales.aggregate(Sum('sale_price'))['sale_price__sum'] or 0
    total_profit = sales.aggregate(Sum('profit'))['profit__sum'] or 0

    context = {
        'sales': sales,
        'total_sales': total_sales,
        'total_value': total_value,
        'total_profit': total_profit,
        'query': query,
    }

    return render(request, 'cars/sold_cars.html', context)


def sale_create(request):
    form = SaleForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('sold_cars_list')

    return render(request, 'cars/sale_form.html', {'form': form})



def documentation_list(request):
    car_id = request.GET.get('car')

    cars = Car.objects.all().order_by('brand', 'model')
    documents = VehicleDocument.objects.select_related('car').prefetch_related('images').all().order_by('-created_at')

    if car_id:
        documents = documents.filter(car_id=car_id)

    context = {
        'cars': cars,
        'documents': documents,
        'selected_car': car_id,
    }

    return render(request, 'cars/documentation.html', context)


def document_create(request):
    form = VehicleDocumentForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        document = form.save()

        for image in request.FILES.getlist('images'):
            VehicleDocumentImage.objects.create(
                document=document,
                image=image
            )

        return redirect('documentation_list')

    return render(request, 'cars/document_form.html', {'form': form})

def inventory_view(request):
    cars = Car.objects.all().order_by('-id')

    cars_in_stock = cars.filter(status='estoque')
    cars_for_sale = cars.filter(status='estoque')

    total_inventory = cars.count()
    total_investment = cars.aggregate(Sum('purchase_price'))['purchase_price__sum'] or 0
    estimated_value = cars.aggregate(Sum('fipe_current_price'))['fipe_current_price__sum'] or 0

    estimated_margin = estimated_value - total_investment

    if total_investment > 0:
        margin_percentage = (estimated_margin / total_investment) * 100
    else:
        margin_percentage = 0

    context = {
        'cars': cars,
        'cars_in_stock': cars_in_stock,
        'cars_for_sale': cars_for_sale,
        'total_inventory': total_inventory,
        'total_investment': total_investment,
        'estimated_value': estimated_value,
        'estimated_margin': estimated_margin,
        'margin_percentage': margin_percentage,
    }

    return render(request, 'cars/inventory.html', context)

def settings_view(request):
    config = AppConfiguration.load()

    active_tab = request.GET.get('tab', 'credentials')
    unlocked = request.session.get('itau_credentials_unlocked', False)

    access_form = AccessPasswordCreateForm()
    unlock_form = CredentialsUnlockForm()
    credentials_form = ItauCredentialsForm()
    change_password_form = ChangeAccessPasswordForm()

    message = ''
    error = ''

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create_access_password':
            access_form = AccessPasswordCreateForm(request.POST)

            if access_form.is_valid():
                config.set_access_password(access_form.cleaned_data['new_password'])
                config.save()

                request.session['itau_credentials_unlocked'] = True
                return redirect('/configuracoes/?tab=credentials')

        elif action == 'unlock_credentials':
            unlock_form = CredentialsUnlockForm(request.POST)

            if unlock_form.is_valid():
                password = unlock_form.cleaned_data['access_password']

                if config.check_access_password(password):
                    request.session['itau_credentials_unlocked'] = True
                    return redirect('/configuracoes/?tab=credentials')

                error = 'Senha incorreta.'

        elif action == 'save_itau_credentials':
            credentials_form = ItauCredentialsForm(request.POST)

            if credentials_form.is_valid():
                config.set_itau_credentials(
                    credentials_form.cleaned_data['itau_email'],
                    credentials_form.cleaned_data['itau_password']
                )
                config.save()

                request.session['itau_credentials_unlocked'] = True
                return redirect('/configuracoes/?tab=credentials')

        elif action == 'lock_credentials':
            request.session['itau_credentials_unlocked'] = False
            return redirect('/configuracoes/?tab=credentials')

        elif action == 'change_access_password':
            active_tab = 'security'
            change_password_form = ChangeAccessPasswordForm(request.POST)

            if change_password_form.is_valid():
                current_password = change_password_form.cleaned_data['current_password']
                new_password = change_password_form.cleaned_data['new_password']

                if config.has_access_password() and not config.check_access_password(current_password):
                    error = 'Senha atual incorreta.'
                else:
                    config.set_access_password(new_password)
                    config.save()

                    request.session['itau_credentials_unlocked'] = False
                    message = 'Senha alterada com sucesso.'

    decrypted_email = ''
    decrypted_password = ''

    if unlocked and config.has_itau_credentials():
        try:
            decrypted_email = config.get_itau_email()
            decrypted_password = config.get_itau_password()
        except Exception:
            error = 'Não foi possível descriptografar as credenciais. Verifique a chave de criptografia.'

    context = {
        'active_tab': active_tab,
        'config': config,
        'unlocked': unlocked,
        'has_password': config.has_access_password(),
        'has_credentials': config.has_itau_credentials(),

        'access_form': access_form,
        'unlock_form': unlock_form,
        'credentials_form': credentials_form,
        'change_password_form': change_password_form,

        'decrypted_email': decrypted_email,
        'decrypted_password': decrypted_password,

        'message': message,
        'error': error,
    }

    return render(request, 'cars/settings.html', context)
