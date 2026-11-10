from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Transaction
from .forms import ProfileForm, TransactionForm
from django.db.models import Sum

def home(request):
    users = Profile.objects.annotate(total=Sum('transactions__amount', default=0))
    return render(request, 'main/home.html', {'users': users})

def create_user(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm()

    return render(request, 'main/create_user.html', {'form': form})

def transaction(request, user_id):
    profile = get_object_or_404(Profile, id=user_id)
    old_transactions = Transaction.objects.filter(user=profile)

    if request.method == 'POST':
        form = TransactionForm(request.POST)

        if form.is_valid():
            tn = form.save(commit=False)
            tn.user = profile
            if 'owe' in request.POST:
                tn.amount = -tn.amount
            tn.save()
            return redirect('transaction', user_id=profile.id)
    else:
        form = TransactionForm()

    total = old_transactions.aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'main/transitions.html', {
        'form': form,
        'transitions': old_transactions,
        'profile': profile,
        'total': total,
    })
