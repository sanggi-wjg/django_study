from django import forms

from apps.stock.models import Pivot


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


class FinanceInfoForm(forms.Form):
    year = forms.IntegerField(label = '년도', required = True, min_value = 1990, initial = 2020
                              , widget = forms.NumberInput(attrs = { 'class': 'form-control' }))
    total_sales = forms.IntegerField(label = '매출액', required = True
                                     , widget = forms.NumberInput(attrs = { 'class': 'form-control' }))
    business_profit = forms.IntegerField(label = '영업이익', required = True
                                         , widget = forms.NumberInput(attrs = { 'class': 'form-control' }))
