from django import forms

class CountryForm(forms.Form):
    CONTINENTS = [
        ('Africa', 'Africa'), ('Europe', 'Europe'), ('Asia', 'Asia'),
        ('Americas', 'Americas'), ('Oceania', 'Oceania')
    ]
    continent = forms.ChoiceField(choices=CONTINENTS, label='Select Continent')
    country = forms.CharField(label='Enter Country Name', max_length=100)
