from django import forms

from .models import Pivot


class PivotForm(forms.ModelForm):
    # prev_closing_price = forms.IntegerField(label = '전일 종가', required = True)
    # prev_high_price = forms.IntegerField(label = '전일 고가(↑)', required = True)
    # prev_low_price = forms.IntegerField(label = '전일 저가(↓)', required = True)

    prev_closing_price = forms.IntegerField(min_value = 1)
    prev_high_price = forms.IntegerField(min_value = 1)
    prev_low_price = forms.IntegerField(min_value = 1)

    class Meta:
        model = Pivot
        fields = ['prev_closing_price', 'prev_high_price', 'prev_low_price']
