from django import forms

class WeatherForm(forms.Form):
	cidade = forms.CharField(max_length=50)	