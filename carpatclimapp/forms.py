from django import forms


class CronFormYearly(forms.Form):
    """
    Date drop down form
    
    https://stackoverflow.com/questions/8859504/django-form-dropdown-list-of-numbers
    """

    MY_CHOICES = (
        
        ("linear", "linear"),
        ("barnes", "barnes"),
        ("cressman", "cressman"),
        ("natural_neighbor", "natural_neighbor")
    )

    year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
    inter = forms.ChoiceField( choices = MY_CHOICES,label="Interpolation", initial='', widget=forms.Select(), required=True )
    
class CronFormMonthly(forms.Form):
    """
    Date drop down form
    
    https://stackoverflow.com/questions/8859504/django-form-dropdown-list-of-numbers
    """

    MY_CHOICES = (

        ("linear", "linear"),
        ("barnes", "barnes"),
        ("cressman", "cressman"),
        ("natural_neighbor", "natural_neighbor")
    )

    year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
    month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
    inter = forms.ChoiceField( choices = MY_CHOICES,label="Interpolation", initial='', widget=forms.Select(), required=True )
    


class CronFormDaily(forms.Form):
    """
    Date drop down form
    
    https://stackoverflow.com/questions/8859504/django-form-dropdown-list-of-numbers
    """
    MY_CHOICES = (
        
        ("linear", "linear"),
        ("barnes", "barnes"),
        ("cressman", "cressman"),
        ("natural_neighbor", "natural_neighbor")
    )

    year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
    month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
    # TODO: add check for number of days in specific month
    day = forms.ChoiceField(choices=[(x, x) for x in range(1, 32)], initial=1)
    inter = forms.ChoiceField( choices = MY_CHOICES,label="Interpolation", initial='', widget=forms.Select(), required=True )
    

class CronFormCord(forms.Form):

    lat = forms.DecimalField(label="Lat", initial=44.0)
    lon = forms.DecimalField(label="Lon",initial=19.0)
