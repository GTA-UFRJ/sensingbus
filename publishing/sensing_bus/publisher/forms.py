import datetime
from django import forms


SENSORS = (('TEMPERATURE', u"Temperature"), ('HUMIDITY', u"Humidity"),
           ('LIGHT', u"Light"), ('RAIN', u"Rain"))

class VisualizeForm(forms.Form):
    bus_name = forms.CharField(label=u"Bus identifier", initial=u"A00000", max_length=10)
    start_time = forms.DateTimeField(label=u"Start time", initial=datetime.date.today, 
                                     widget=forms.Textarea(attrs={'type': 'date'}))
    end_time = forms.DateTimeField(label=u"End time", initial=datetime.date.today,
                                    widget=forms.Textarea(attrs={'type': 'date'}))
    sensor_name = forms.ChoiceField(widget=forms.RadioSelect(attrs={'type': 'radio'}),
                                    choices=SENSORS)
    min_lat = forms.DecimalField(label=u"Minimum Latitude", initial=0.0,
                                  min_value=(-90), max_value=90,
                                  max_digits=9, decimal_places=6)
    max_lat = forms.DecimalField(label=u"Maximum Latitude", initial=0.0,
                                  min_value=(-90), max_value=90,
                                  max_digits=9, decimal_places=6)
    min_lng = forms.DecimalField(label=u"Minimum Longitude", initial=0.0,
                                  min_value=(-180), max_value=180,
                                  max_digits=9, decimal_places=6)
    max_lng = forms.DecimalField(label=u"Maximum Longitude", initial=0.0,
                                  min_value=(-180), max_value=180,
                                  max_digits=9, decimal_places=6)