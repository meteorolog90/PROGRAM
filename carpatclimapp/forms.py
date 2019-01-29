from django import forms

class DataFormYearlyPrec(forms.Form):

	MY_VARIABLE = (
		
		("temperature", "temperature"),
		("precipitation", "precipitation"),    
	)

	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	var = forms.ChoiceField(choices=MY_VARIABLE,label="Variable")

class DataFormMonthly(forms.Form):

	MY_VARIABLE = (
		
		("temperature", "temperature"),
		("precipitation", "precipitation"),    
	)

	var = forms.ChoiceField(choices=MY_VARIABLE,label="Variable")
	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)


class DataFormDaily(forms.Form):

	MY_VARIABLE = (
		
		("temperature", "temperature"),
		("precipitation", "precipitation"),    
	)

	var = forms.ChoiceField(choices=MY_VARIABLE,label="Variable")	
	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
	day = forms.ChoiceField(choices=[(x, x) for x in range(1, 32)], initial=1)




class CronFormYearly(forms.Form):
	"""
	Date drop down form
	
	https://stackoverflow.com/questions/8859504/django-form-dropdown-list-of-numbers
	"""

	MY_CHOICES = (
		
		("linear", "linear"),
		("barnes", "barnes"),
		("cressman", "cressman"),
		
	)


	MY_VARIABLE = (
		
		("temperature", "temperature"),
		("precipitation", "precipitation"),    
	)


	var = forms.ChoiceField(choices=MY_VARIABLE,label="Variable")	
	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	inter = forms.ChoiceField( choices = MY_CHOICES,label="Interpolation", initial='', widget=forms.Select(), required=True )
	
class CronFormYearlyPrec(forms.Form):

	MY_CHOICES1 = (

		("barnes", "barnes"),
		("krigin", "krigin"),
	)

	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	inter = forms.ChoiceField( choices = MY_CHOICES1,label="Interpolation", initial='', widget=forms.Select(), required=True )


class CronFormMonthly(forms.Form):
	"""
	Date drop down form
	
	https://stackoverflow.com/questions/8859504/django-form-dropdown-list-of-numbers
	"""

	MY_CHOICES = (

		("linear", "linear"),
		("barnes", "barnes"),
		("cressman", "cressman"),
		
	)



	MY_VARIABLE = (
		
		("temperature", "temperature"),
		("precipitation", "precipitation"),    
	)

	var = forms.ChoiceField(choices=MY_VARIABLE,label="Variable")	
	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
	inter = forms.ChoiceField( choices = MY_CHOICES,label="Interpolation", initial='', widget=forms.Select(), required=True )
	

class CronFormMonthlyPrec(forms.Form):

	MY_CHOICES1 = (

		("barnes", "barnes"),
		("krigin", "krigin"),
	)

	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
	inter = forms.ChoiceField( choices = MY_CHOICES1,label="Interpolation", initial='', widget=forms.Select(), required=True )


class CronFormDaily(forms.Form):
	"""
	Date drop down form
	
	https://stackoverflow.com/questions/8859504/django-form-dropdown-list-of-numbers
	"""
	MY_CHOICES = (
		
		("linear", "linear"),
		("barnes", "barnes"),
		("cressman", "cressman"),
		
	)

	
	MY_VARIABLE = (
		
		("temperature", "temperature"),
		("precipitation", "precipitation"),    
	)

	var = forms.ChoiceField(choices=MY_VARIABLE,label="Variable")
	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
	# TODO: add check for number of days in specific month
	day = forms.ChoiceField(choices=[(x, x) for x in range(1, 32)], initial=1)
	inter = forms.ChoiceField( choices = MY_CHOICES,label="Interpolation", initial='', widget=forms.Select(), required=True )


class CronFormDailyPrec(forms.Form):

	MY_CHOICES1 = (

		("barnes", "barnes"),
		("krigin", "krigin"),
	)

	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
	day = forms.ChoiceField(choices=[(x, x) for x in range(1, 32)], initial=1)
	inter = forms.ChoiceField( choices = MY_CHOICES1,label="Interpolation", initial='', widget=forms.Select(), required=True )
	
class CronFormCord(forms.Form):

	lat = forms.DecimalField(label="Lat", initial=44.0)
	lon = forms.DecimalField(label="Lon",initial=19.0)

	


class PeriodYearlyForm(forms.Form):


	MY_CHOICES = (
		
		("linear", "linear"),
		("barnes", "barnes"),
		("cressman", "cressman"),
		
	)

	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	year1 = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	lon = forms.DecimalField(label="Lon",initial=19.0)
	lat = forms.DecimalField(label="Lat", initial=44.0)
	#inter = forms.ChoiceField( choices = MY_CHOICES,label="Interpolation", initial='', widget=forms.Select(), required=True )


class PeriodMonthlyForm(forms.Form):


	MY_CHOICES = (
		
		("linear", "linear"),
		("barnes", "barnes"),
		("cressman", "cressman"),
		
	)

	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
	year1 = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month1 = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
	lon = forms.DecimalField(label="Lon",initial=19.0)
	lat = forms.DecimalField(label="Lat", initial=44.0)
	inter = forms.ChoiceField( choices = MY_CHOICES,label="Interpolation", initial='', widget=forms.Select(), required=True )

class PeriodDailyForm(forms.Form):


	MY_CHOICES = (
		
		("linear", "linear"),
		("barnes", "barnes"),
		("cressman", "cressman"),
		
	)

	year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
	day = forms.ChoiceField(choices=[(x, x) for x in range(1, 32)], initial=1)
	year1 = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2011)], initial=1961)
	month1 = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], initial=1)
	day1 = forms.ChoiceField(choices=[(x, x) for x in range(1, 32)], initial=1)
	lat = forms.DecimalField(label="Lat", initial=44.0)
	lon = forms.DecimalField(label="Lon",initial=19.0)
	inter = forms.ChoiceField( choices = MY_CHOICES,label="Interpolation", initial='', widget=forms.Select(), required=True )
