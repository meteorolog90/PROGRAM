from io import BytesIO
from base64 import b64encode
import csv

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from .carpatclim import *
from .forms import CronFormYearly,CronFormMonthly,CronFormDaily,CronFormCord,DataFormMonthly,DataFormDaily
from .forms import DataFormYearlyPrec,CronFormYearlyPrec,CronFormMonthlyPrec,CronFormDailyPrec
# Create your views here.


def home(request):
	if request.method == "POST":
		form = CronFormYearly(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			year = data.get('year')
			inter = data.get('inter')
			country = data.get('country')
			var = data.get ('var')
			date_path = '/%s/%s/%s/%s'%(var,inter,country,year) 
			return redirect(date_path)
	else:
		form = CronFormYearly()
		active_yearly = True
	return render(request, 'carpatclimapp/home.html', {'form': form, 'active_yearly': active_yearly})


def yearly(request):

	if request.method == "POST":
		form = CronFormYearly(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			year = data.get('year')
			inter = data.get('inter')
			country = data.get('country')
			var = data.get('var')
			
			date_path = '/%s/%s/%s/%s'%(var,inter,country,year) 

			return redirect (date_path)
			
	else:
		form = CronFormYearly()
		active_yearly = True
	return render(request, 'carpatclimapp/home.html', {'form': form, 'active_yearly': active_yearly})

# def yearlyprec(request):
# 	if request.method == "POST":
# 		form = CronFormYearlyPrec(request.POST)
# 		if form.is_valid():
# 			data = form.cleaned_data
# 			year = data.get('year')
# 			inter = data.get('inter')
# 			date_path = '/%s/%s'%(inter,year) 
# 			return redirect (date_path)
			
# 	else:
# 		form = CronFormYearlyPrec()
# 		active_yearly_prec = True
# 	return render(request, 'carpatclimapp/home.html', {'form': form, 'active_yearly_prec': active_yearly_prec})

# def monthlyprec(request):
# 	if request.method == "POST":
# 		form = CronFormMonthlyPrec(request.POST)
# 		if form.is_valid():
# 			data = form.cleaned_data
# 			year = data.get('year')
# 			month = data.get('month')
# 			inter = data.get('inter')
# 			date_path = '/%s/%s/%s'%(inter,year,month) 
# 			return redirect (date_path)
			
# 	else:
# 		form = CronFormMonthlyPrec()
# 		active_monthly_prec = True
# 	return render(request, 'carpatclimapp/home.html', {'form': form, 'active_monthly_prec': active_monthly_prec})


def monthly(request):
	if request.method == "POST":
		form = CronFormMonthly(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			var = data.get ('var')
			year = data.get('year')
			month = data.get('month')
			inter = data.get ('inter')
			country = data.get('country')
			date_path = '/%s/%s/%s/%s/%s' % (var,inter,country,year,month)
			return redirect(date_path)
	else:
		form = CronFormMonthly()
		active_monthly = True
	return render(request, 'carpatclimapp/home.html', {'form': form, 'active_monthly': active_monthly})


def daily(request):
	if request.method == "POST":
		form = CronFormDaily(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			var = data.get ('var')
			year = data.get('year')
			month = data.get('month')
			day = data.get('day')
			inter = data.get ('inter')
			country = data.get('country')
			date_path = '/%s/%s/%s/%s/%s/%s' % (var,inter,country,year, month, day)

			return redirect(date_path)
	else:

		form = CronFormDaily()
		active_daily = True

	return render(request, 'carpatclimapp/home.html', {'form': form, 'active_daily': active_daily})

# def dailyprec(request):
# 	if request.method == "POST":
# 		form = CronFormDailyPrec(request.POST)
# 		if form.is_valid():
# 			data = form.cleaned_data
# 			year = data.get('year')
# 			month = data.get('month')
# 			day = data.get('day')
# 			inter = data.get ('inter')
# 			date_path = '/%s/%s/%s/%s' % (inter,year, month, day)

# 			return redirect(date_path)
# 	else:

# 		form = CronFormDailyPrec()
# 		active_daily_prec = True

# 	return render(request, 'carpatclimapp/home.html', {'form': form, 'active_daily_prec': active_daily_prec})


def cordinates(request):
	if request.method == "POST":
		form = CronFormCord(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			lat = data.get('lat')
			lon = data.get('lon')
			cord = '/%s/%s/'%(lat,lon)
			
			return redirect(cord)
	else:

		form = CronFormCord()
		active_cordinates = True

	return render(request, 'carpatclimapp/cordinates.html', {'form': form, 'active_cordinates': active_cordinates})


def dataviewsy(request):

	if request.method == "POST":
		form = DataFormYearlyPrec(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			year = data.get('year')
			var = data.get ('var')
			cord = '/%s/%s'%(var,year)
			
			if var == 'precipitation':

				point = view_data_prec(year)  
				args = {'point':point}

				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="precipitation.csv"'
				writer = csv.writer(response)
				writer.writerow([point])

				return response

			else :

				point = view_data(year)  
				args = {'point':point}

				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="temperatures.csv"'
				writer = csv.writer(response)
				writer.writerow([point])

				return response

	else:

		form = DataFormYearlyPrec()
		active_data_prec_y = True 

	return render(request, 'carpatclimapp/data.html', {'form': form, 'active_data_prec_y': active_data_prec_y})

def dataviewsm(request):

	if request.method == "POST":
		form = DataFormMonthly(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			year = data.get('year')
			month = data.get('month')
			var = data.get('var')
			cord = '%s/%s/%s'%(var,year,month)
			
			if var == 'precipitation':

				point = view_data_prec(year,month)  
				args = {'point':point}

				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="precipitation.csv"'
				writer = csv.writer(response)
				writer.writerow([point])

				return response

			else :

				point = view_data(year,month)  
				args = {'point':point}

				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="temperatures.csv"'
				writer = csv.writer(response)
				writer.writerow([point])

				return response
	else:
		
		form = DataFormMonthly()
		active_datam = True 

	return render(request, 'carpatclimapp/data.html', {'form': form, 'active_datam': active_datam})

def dataviewsd(request):

	if request.method == "POST":
		form = DataFormDaily(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			var = data.get ('var')
			year = data.get('year')
			month = data.get('month')
			day = data.get('day')
			cord = '/%s/%s/%s/%s'%(var,year,month,day)
	
			if var == 'precipitation':

				point = view_data_prec(year,month,day)  
				args = {'point':point}

				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="precipitation.csv"'
				writer = csv.writer(response)
				writer.writerow([point])

				return response

			else :

				point = view_data(year,month,day)  
				args = {'point':point}

				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="temperatures.csv"'
				writer = csv.writer(response)
				writer.writerow([point])

				return response
	else:
		form = DataFormDaily()
		active_datad = True 
	return render(request, 'carpatclimapp/data.html', {'form': form, 'active_datad': active_datad})

def carpatclim_y_figure(request,var,inter,country, year):
	"""View with year map image"""
	if var == 'temperature':

		map = create_map(year,inter,country, month=None, day=None)
		buffer = BytesIO()
		canvas = FigureCanvas(map)
		canvas.print_png(buffer)
		

		response = HttpResponse(buffer.getvalue(), content_type='image/png')
		response['Content-Length'] = str(len(response.content))
		return response

	if var == 'precipitation': 
		map1 = create_map_prec(year,inter,country, month=None, day=None)
		buffer = BytesIO()
		canvas = FigureCanvas(map1)
		canvas.print_png(buffer)
		

		response = HttpResponse(buffer.getvalue(), content_type='image/png')
		response['Content-Length'] = str(len(response.content))
		return response

# def carpatclim_y_prec_figure(request,inter,year):
# 	"""View with year map image"""
	
# 	map = create_map_prec(year, inter,month=None, day=None)
# 	buffer = BytesIO()
# 	canvas = FigureCanvas(map)
# 	canvas.print_png(buffer)
		

# 	response = HttpResponse(buffer.getvalue(), content_type='image/png')
# 	response['Content-Length'] = str(len(response.content))
# 	return response


def carpatclim_m_figure(request,var,inter,country, year, month):
	"""year/month map image"""

	if var == 'temperature':
		map = create_map(year, inter,country, month, day=None)
		buffer = BytesIO()
		canvas = FigureCanvas(map)
		canvas.print_png(buffer)

		response = HttpResponse(buffer.getvalue(), content_type='image/png')
		# I recommend to add Content-Length for Django
		response['Content-Length'] = str(len(response.content))
		return response

	if var == 'precipitation': 
		map1 = create_map_prec(year,inter,country, month, day=None)
		buffer = BytesIO()
		canvas = FigureCanvas(map1)
		canvas.print_png(buffer)
		

		response = HttpResponse(buffer.getvalue(), content_type='image/png')
		response['Content-Length'] = str(len(response.content))
		return response


# def carpatclim_m_prec_figure(request,inter,year,month):
# 	"""View with year map image"""

# 	map = create_map_prec(year, inter,month, day=None)
# 	buffer = BytesIO()
# 	canvas = FigureCanvas(map)
# 	canvas.print_png(buffer)
	

# 	response = HttpResponse(buffer.getvalue(), content_type='image/png')
# 	response['Content-Length'] = str(len(response.content))
# 	return response


def carpatclim_d_figure(request,var,inter,country, year, month, day):
	"""year/month/day map image"""
	if var == 'temperature': 
		map = create_map(year, inter,country, month, day)
		buffer = BytesIO()
		canvas = FigureCanvas(map)
		canvas.print_png(buffer)

		response = HttpResponse(buffer.getvalue(), content_type='image/png')
		# I recommend to add Content-Length for Django
		response['Content-Length'] = str(len(response.content))

		return response

	if var == 'precipitation':
		map1 = create_map_prec(year, inter,country, month, day)
		buffer = BytesIO()
		canvas = FigureCanvas(map1)
		canvas.print_png(buffer)

		response = HttpResponse(buffer.getvalue(), content_type='image/png')
		# I recommend to add Content-Length for Django
		response['Content-Length'] = str(len(response.content))

		return response

# def carpatclim_d_prec_figure(request,inter,year, month, day):
# 	"""year/month/day map image"""

# 	map = create_map_prec(year, inter, month, day)
# 	buffer = BytesIO()
# 	canvas = FigureCanvas(map)
# 	canvas.print_png(buffer)

# 	response = HttpResponse(buffer.getvalue(), content_type='image/png')
# 	# I recommend to add Content-Length for Django
# 	response['Content-Length'] = str(len(response.content))
# 	return response

def carpatclim_point(request,lat,lon):


	lat = float(lat)
	lon = float(lon)
	point = cordinates_point(lat,lon)
	
	args = {'point':point, 'lat':lat, 'lon':lon}
	
	return render(request, 'carpatclimapp/cordout.html',args)


def carpatclim_y(request,var,inter,country, year):
	"""year/month embeded in page"""
	
	date_path = '%s/%s/%s/%s' %(var,inter,country,year)

	return render(request, 'carpatclimapp/simple.html', {'date_path': date_path})

# def carpatclim_y_prec(request,inter, year):
# 	"""year/month embeded in page"""
	
# 	date_path = '%s/%s' %(inter,year)

# 	return render(request, 'carpatclimapp/simple.html', {'date_path': date_path})


def carpatclim_m(request,var,inter,country, year, month):
	"""View with year/month embeded in page"""
	
	date_path = '%s/%s/%s/%s/%s' % (var,inter,country, year, month)

	return render(request, 'carpatclimapp/simple.html', {'date_path': date_path})

# def carpatclim_m_prec(request,inter, year, month):
# 	"""View with year/month embeded in page"""
	
# 	date_path = '%s/%s/%s' % (inter,year, month)

# 	return render(request, 'carpatclimapp/simple.html', {'date_path': date_path})


def carpatclim_d(request,var,inter,country, year, month, day):
	"""View with year/month/day embeded in page"""
	
	date_path = '%s/%s/%s/%s/%s/%s' % (var,inter,country, year, month, day)

	return render(request, 'carpatclimapp/simple.html', {'date_path': date_path})

# def carpatclim_d_prec(request,inter, year, month, day):
# 	"""View with year/month/day embeded in page"""
	
# 	date_path = '%s/%s/%s/%s' % (inter,year, month, day)

# 	return render(request, 'carpatclimapp/simple.html', {'date_path': date_path})


