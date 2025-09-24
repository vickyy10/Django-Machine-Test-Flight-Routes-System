from django import forms
from .models import Airport, Route
from core.constants import DIRECTION_CHOICES



class AirportForm(forms.ModelForm):
    class Meta:
        model = Airport
        fields = ['code', 'name', 'city', 'country']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '3'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'code': 'Airport Code (IATA)',
            'name': 'Airport Name',
            'city': 'City',
            'country': 'Country',
        }



class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['from_airport', 'to_airport', 'position', 'duration', 'direction']
        widgets = {
            'from_airport': forms.Select(attrs={'class': 'form-control'}),
            'to_airport': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'direction': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'from_airport': 'From Airport',
            'to_airport': 'To Airport',
            'position': 'Position',
            'duration': 'Duration (minutes)',
            'direction': 'Direction',
        }



class AirportRouteForm(forms.Form):
    from_airport_code = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        label="From Airport",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    to_airport_code = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        label="To Airport",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    position = forms.IntegerField(
        min_value=1,
        label="Position",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    )
    duration = forms.IntegerField(
        min_value=1,
        label="Duration (minutes)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    )

    def clean(self):
        cleaned_data = super().clean()
        from_airport = cleaned_data.get('from_airport_code')
        to_airport = cleaned_data.get('to_airport_code')

        if from_airport and to_airport:
            if from_airport == to_airport:
                raise forms.ValidationError("From airport and To airport cannot be the same.")
            
            if Route.objects.filter(from_airport=from_airport, to_airport=to_airport).exists():
                raise forms.ValidationError("A route between these airports already exists.")

        return cleaned_data



class SearchNthNodeForm(forms.Form):
    start_airport = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        label="Starting Airport",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    n = forms.IntegerField(
        min_value=1,
        label="Nth Position",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    )
    direction = forms.ChoiceField(
        choices=DIRECTION_CHOICES,
        label="Direction",
        widget=forms.Select(attrs={'class': 'form-control'})
    )



class ShortestRouteForm(forms.Form):
    from_airport = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        label="From Airport",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    to_airport = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        label="To Airport",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        from_airport = cleaned_data.get('from_airport')
        to_airport = cleaned_data.get('to_airport')

        if from_airport and to_airport and from_airport == to_airport:
            raise forms.ValidationError("From airport and To airport cannot be the same.")

        return cleaned_data