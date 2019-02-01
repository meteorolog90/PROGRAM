from django import forms


MY_VARIABLE = (
		
		("temperature", "temperature"),
		("precipitation", "precipitation"),    
	)

MY_CHOICES = (
		
		("linear", "linear"),
		("barnes", "barnes"),
		("cressman", "cressman"),
		
	)

MY_CHOICES1 = (

		("barnes", "barnes"),
		("krigin", "krigin"),
	)
YEARS= [x for x in range(1961,2010)]
months= [x for x in range(1,12)]


class DataFormYearlyPrec(forms.Form):

	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	var = forms.ChoiceField(choices=MY_VARIABLE,label="Variable")

class DataFormMonthly(forms.Form):

	var = forms.ChoiceField(choices=MY_VARIABLE,label="Variable")
	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)


class DataFormDaily(forms.Form):

	var = forms.ChoiceField(choices=MY_VARIABLE,label="Variable")	
	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
	day = forms.ChoiceField(choices=[(x, x) for x in range(1, 32)], initial=1)

class CronFormYearly(forms.Form):
	"""
	Date drop down form
	
	https://stackoverflow.com/questions/8859504/django-form-dropdown-list-of-numbers
	"""

	var = forms.ChoiceField(choices=MY_VARIABLE,label="Variable")	
	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	inter = forms.ChoiceField( choices = MY_CHOICES,label="Interpolation", initial='', widget=forms.Select(), required=True )
	
class CronFormYearlyPrec(forms.Form):

	

	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	inter = forms.ChoiceField( choices = MY_CHOICES1,label="Interpolation", initial='', widget=forms.Select(), required=True )


class CronFormMonthly(forms.Form):
	"""
	Date drop down form
	
	https://stackoverflow.com/questions/8859504/django-form-dropdown-list-of-numbers
	"""
	var = forms.ChoiceField(choices=MY_VARIABLE,label="Variable")	
	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
	inter = forms.ChoiceField( choices = MY_CHOICES,label="Interpolation", initial='', widget=forms.Select(), required=True )
	

class CronFormMonthlyPrec(forms.Form):

	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
	inter = forms.ChoiceField( choices = MY_CHOICES1,label="Interpolation", initial='', widget=forms.Select(), required=True )


class CronFormDaily(forms.Form):
	"""
	Date drop down form
	
	https://stackoverflow.com/questions/8859504/django-form-dropdown-list-of-numbers
	"""

	var = forms.ChoiceField(choices=MY_VARIABLE,label="Variable")
	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
	# TODO: add check for number of days in specific month
	day = forms.ChoiceField(choices=[(x, x) for x in range(1, 32)], initial=1)
	inter = forms.ChoiceField( choices = MY_CHOICES,label="Interpolation", initial='', widget=forms.Select(), required=True )


class CronFormDailyPrec(forms.Form):

	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
	day = forms.ChoiceField(choices=[(x, x) for x in range(1, 32)], initial=1)
	inter = forms.ChoiceField( choices = MY_CHOICES1,label="Interpolation", initial='', widget=forms.Select(), required=True )
	
class CronFormCord(forms.Form):

	lat = forms.DecimalField(label="Lat", initial=44.0)
	lon = forms.DecimalField(label="Lon",initial=19.0)

class PeriodYearlyForm(forms.Form):

	inter = forms.ChoiceField( choices = MY_CHOICES,label="Interpolation", initial='', widget=forms.Select(), required=True )
	var = forms.ChoiceField(choices=MY_VARIABLE,label="Variable")
	#year=forms.DateField(widget=forms.SelectDateWidget(years=YEARS,months=None))
	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	year1 = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	lon = forms.DecimalField(label="Lon",initial=19.0)
	lat = forms.DecimalField(label="Lat", initial=44.0)
	


class PeriodMonthlyForm(forms.Form):
	#field1 = forms.DateField(widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))
	#field1 = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"))
	inter = forms.ChoiceField( choices = MY_CHOICES,label="Interpolation", initial='', widget=forms.Select(), required=True )
	var = forms.ChoiceField(choices=MY_VARIABLE,label="Variable")
	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
	year1 = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month1 = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
	lon = forms.DecimalField(label="Lon",initial=19.0)
	lat = forms.DecimalField(label="Lat", initial=44.0)
	

class PeriodDailyForm(forms.Form):

	inter = forms.ChoiceField( choices = MY_CHOICES,label="Interpolation", initial='', widget=forms.Select(), required=True )
	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
	day = forms.ChoiceField(choices=[(x, x) for x in range(1, 32)], initial=1)
	year1 = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month1 = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
	day1 = forms.ChoiceField(choices=[(x, x) for x in range(1, 32)], initial=1)
	lat = forms.DecimalField(label="Lat", initial=44.0)
	lon = forms.DecimalField(label="Lon",initial=19.0)
	
