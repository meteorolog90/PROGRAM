from io import BytesIO
from base64 import b64encode
import csv

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from .carpatclim import *
from .forms import CronFormYearly, CronFormMonthly, CronFormDaily, CronFormCord
# Create your views here.


def home(request):
    if request.method == "POST":
        form = CronFormYearly(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            year = data.get('year')
            inter = data.get('inter')
            country = data.get('country')
            date_path = '/%s/%s/%s'%(inter,country,year) 
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
            date_path = '/%s/%s/%s'%(inter,country,year) 
            return redirect (date_path)
            
    else:
        form = CronFormYearly()
        active_yearly = True
    return render(request, 'carpatclimapp/home.html', {'form': form, 'active_yearly': active_yearly})


def monthly(request):
    if request.method == "POST":
        form = CronFormMonthly(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            year = data.get('year')
            month = data.get('month')
            inter = data.get ('inter')
            country = data.get('country')
            date_path = '/%s/%s/%s/%s' % (inter,country,year,month)
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
            year = data.get('year')
            month = data.get('month')
            day = data.get('day')
            inter = data.get ('inter')
            country = data.get('country')
            date_path = '/%s/%s/%s/%s/%s' % (inter,country,year, month, day)
            return redirect(date_path)
    else:
        form = CronFormDaily()
        active_daily = True
    return render(request, 'carpatclimapp/home.html', {'form': form, 'active_daily': active_daily})

def cordinates(request):
    if request.method == "POST":
        form = CronFormCord(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            lat = data.get('lat')
            lon = data.get('lon')
            cord = '/%s/%s/'%(lat,lon)
            # broj = data.get('broj')
            # adresa = '/%s'%(broj)
            return redirect(cord)
    else:
        form = CronFormCord()
        active_cordinates = True
    return render(request, 'carpatclimapp/cordinates.html', {'form': form, 'active_cordinates': active_cordinates})

def carpatclim_y_figure(request,inter,country, year):
    """View with year map image"""

    map = create_map(year, inter,country, month=None, day=None)
    buffer = BytesIO()
    canvas = FigureCanvas(map)
    canvas.print_png(buffer)

    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    response['Content-Length'] = str(len(response.content))
    return response


def carpatclim_m_figure(request,inter,country, year, month):
    """year/month map image"""

    map = create_map(year, inter,country, month, day=None)
    buffer = BytesIO()
    canvas = FigureCanvas(map)
    canvas.print_png(buffer)

    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    # I recommend to add Content-Length for Django
    response['Content-Length'] = str(len(response.content))
    return response


def carpatclim_d_figure(request,inter,country, year, month, day):
    """year/month/day map image"""

    map = create_map(year, inter,country, month, day)
    buffer = BytesIO()
    canvas = FigureCanvas(map)
    canvas.print_png(buffer)

    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    # I recommend to add Content-Length for Django
    response['Content-Length'] = str(len(response.content))
    return response

def carpatclim_point(request,lat,lon):


#def carpatclim_point(request,broj):

    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    # writer = csv.writer(response)
    # writer.writerow(['broj'])
    #writer.writero#w(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    lat = float(lat)
    lon = float(lon)
    #broj = int(broj)
    point = cordinates_point(lat,lon)
    #point = cordinates_point(broj)
    args = {'point':point, 'lat':lat, 'lon':lon}
    #args = {'point':point}#, 'number':number}
      
    #return render(request, 'carpatclimapp/cordinates.html',args)
    return render(request, 'carpatclimapp/cordout.html',args)
    
    

def carpatclim_y(request,inter,country, year):
    """year/month embeded in page"""
    
    date_path = '%s/%s/%s' %(inter,country,year)

    return render(request, 'carpatclimapp/simple.html', {'date_path': date_path})


def carpatclim_m(request,inter,country, year, month):
    """View with year/month embeded in page"""
    
    date_path = '%s/%s/%s/%s' % (inter,country, year, month)

    return render(request, 'carpatclimapp/simple.html', {'date_path': date_path})


def carpatclim_d(request,inter,country, year, month, day):
    """View with year/month/day embeded in page"""
    
    date_path = '%s/%s/%s/%s/%s' % (inter,country, year, month, day)

    return render(request, 'carpatclimapp/simple.html', {'date_path': date_path})

