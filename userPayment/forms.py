from django import forms
from project.models import Donation


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount', 'user', 'project']