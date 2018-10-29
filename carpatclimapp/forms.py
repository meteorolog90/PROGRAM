from django import forms


class CronFormYearly(forms.Form):
    """
    Date drop down form
    
    https://stackoverflow.com/questions/8859504/django-form-dropdown-list-of-numbers
    """
    year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)


class CronFormMonthly(forms.Form):
    """
    Date drop down form
    
    https://stackoverflow.com/questions/8859504/django-form-dropdown-list-of-numbers
    """
    year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
    month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)


class CronFormDaily(forms.Form):
    """
    Date drop down form
    
    https://stackoverflow.com/questions/8859504/django-form-dropdown-list-of-numbers
    """
    year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
    month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
    # TODO: add check for number of days in specific month
    day = forms.ChoiceField(choices=[(x, x) for x in range(1, 32)], initial=1)



class CronFormCord(forms.Form):
    

#     # def seq(start, stop, step=1):

#     #     n = int(round((stop - start)/float(step)))
#     #     if n > 1:
#     #         return([start + step*i for i in range(n+1)])
#     #     elif n == 1:
#     #         return([start])
#     #     else:
#     #         return([])
#     """
#     Date drop down form
    
#     https://stackoverflow.com/questions/8859504/django-form-dropdown-list-of-numbers

#     """
    

    #lat = forms.ChoiceField(choices=[(x, x) for x in range(44,51)], initial=44.0)
    #lon = forms.ChoiceField(choices=[(x,x) for x in range(17,28)], initial=17.0)
#     # max_number = forms.ChoiceField(widget = forms.Select(), 
#     #              choices = ([('17.1','17.2'), ('2','2'),('3','3'), ]), initial='3', required = True,)
#     # lat = forms.ChoiceField(choices=[(x, x) for x in seq(44.0,50.0,0.1)], initial=44.0)
#     # lon = forms.ChoiceField(choices=[(x,x) for x in seq(17.0, 27.0, 0.1)], initial=17.0)




   

#     lon_choices = ((19.0,19.0),(19.1,19.1),
#     (19.2,19.2), (19,19)
#     )
#     lat_choices = ((49.9,49.9),
#     (50.0,50.0),(50,50)
#     ) 
    lat = forms.DecimalField(label="Lat")
    lon = forms.DecimalField(label="Lon")
