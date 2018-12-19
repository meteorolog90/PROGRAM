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


    MY_COUNTRY = (
        
        ("Serbia", "Serbia"),
        ("Romania", "Romania"),
        ("Carpathian area", "Carpathian area"),
        
    )

    year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
    inter = forms.ChoiceField( choices = MY_CHOICES,label="Interpolation", initial='', widget=forms.Select(), required=True )
    country = forms.ChoiceField(choices = MY_COUNTRY,label="Region", initial='Carpathian area', widget=forms.Select(), required=True )
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

    MY_COUNTRY = (
        
        ("Serbia", "Serbia"),
        ("Romania", "Romania"),
        ("Carpathian area", "Carpathian area"),
        
    )

    year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
    month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
    inter = forms.ChoiceField( choices = MY_CHOICES,label="Interpolation", initial='', widget=forms.Select(), required=True )
    country = forms.ChoiceField(choices = MY_COUNTRY,label="Region", initial='Carpathian area', widget=forms.Select(), required=True )


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

    MY_COUNTRY = (
        
        ("Serbia", "Serbia"),
        ("Romania", "Romania"),
        ("Carpathian area", "Carpathian area"),
        
    )

    year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
    month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
    # TODO: add check for number of days in specific month
    day = forms.ChoiceField(choices=[(x, x) for x in range(1, 32)], initial=1)
    inter = forms.ChoiceField( choices = MY_CHOICES,label="Interpolation", initial='', widget=forms.Select(), required=True )
    country = forms.ChoiceField(choices = MY_COUNTRY,label="Region", initial='Carpathian area', widget=forms.Select(), required=True )

class CronFormCord(forms.Form):

    lat = forms.DecimalField(label="Lat", initial=44.0)
    lon = forms.DecimalField(label="Lon",initial=19.0)

    # COUNTRY = (
        
    #     ("1", "Hungary"),
    #     ("2", "Serbia"),
    #     ("3", "Romania"),
    #     ("4", "Ukraine"),
    #     ("5", "Slovakia"),
    #     ("6", "Poland"),
    #     ("7", "Czech Republic"),
    #     ("8", "Croatia"),
        
    # )



    # broj = forms.ChoiceField( choices= COUNTRY,label="Select country"  )
    #broj = forms.DecimalField(label="Country", initial=1)