from django import forms
from .models import Profile, Transaction


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone']


class TransactionForm(forms.ModelForm):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)

    class Meta:
        model = Transaction
        fields = ['amount']