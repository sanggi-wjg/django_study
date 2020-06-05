from django import forms

from .models import Pivot


class PivotForm(forms.ModelForm):
    prev_closing_price = forms.IntegerField(label = '전일 종가', required = True, min_value = 1
                                            , widget = forms.NumberInput(attrs = { 'class': 'form-control' }))
    prev_high_price = forms.IntegerField(label = '전일 고가(↑)', required = True, min_value = 1
                                         , widget = forms.NumberInput(attrs = { 'class': 'form-control' }))
    prev_low_price = forms.IntegerField(label = '전일 저가(↓)', required = True, min_value = 1
                                        , widget = forms.NumberInput(attrs = { 'class': 'form-control' }))

    class Meta:
        model = Pivot
        fields = ['prev_closing_price', 'prev_high_price', 'prev_low_price']
