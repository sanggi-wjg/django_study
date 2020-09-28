from django import forms

from apps.model.portfolios import Portfolios


class CreatePortfolioForm(forms.ModelForm):
    portfolio_name = forms.CharField(label = '포트폴리오 이름', required = True
                                     , widget = forms.TextInput(attrs = { 'class': 'form-control' }))
    portfolio_deposit = forms.IntegerField(label = '예수금', required = True, min_value = 10000
                                           , widget = forms.NumberInput(attrs = { 'class': 'form-control' }))

    class Meta:
        model = Portfolios
        fields = ['portfolio_name', 'portfolio_deposit']
