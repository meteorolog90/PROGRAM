from io import BytesIO
from base64 import b64encode

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from .carpatclim import *
from .forms import CronForm
# Create your views here.


def home(request):
    if request.method == "POST":
        form = CronForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            year = data.get('year')
            # month = data.get('month')
            # day = data.get('day')
            # return redirect('%s/%s/%s/figure.png' % (year, month, day))
            # return redirect('%s/figure.png' % (year))
            date_path = year
            # return render(request, 'carpatclimapp/simple.html', {'date_path': date_path})
            return redirect('/carpatclim/%s/' % (date_path))
    else:
        form = CronForm()
    return render(request, 'carpatclimapp/home.html', {'form': form})


def carpatclim_y_figure(request, year):
    """View with year map image"""

    map = create_map(year, month=None, day=None)
    buffer = BytesIO()
    canvas = FigureCanvas(map)
    canvas.print_png(buffer)

    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    response['Content-Length'] = str(len(response.content))
    return response


def carpatclim_m_figure(request, year, month):
    """year/month map image"""

    map = create_map(year, month, day=None)
    buffer = BytesIO()
    canvas = FigureCanvas(map)
    canvas.print_png(buffer)

    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    # I recommend to add Content-Length for Django
    response['Content-Length'] = str(len(response.content))
    return response


def carpatclim_d_figure(request, year, month, day):
    """year/month/day map image"""

    map = create_map(year, month, day)
    buffer = BytesIO()
    canvas = FigureCanvas(map)
    canvas.print_png(buffer)

    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    # I recommend to add Content-Length for Django
    response['Content-Length'] = str(len(response.content))
    return response


def carpatclim_y(request, year):
    """year/month embeded in page"""
    
    date_path = year

    return render(request, 'carpatclimapp/simple.html', {'date_path': date_path})


def carpatclim_m(request, year, month):
    """View with year/month embeded in page"""
    
    date_path = '%s/%s' % (year, month)

    return render(request, 'carpatclimapp/simple.html', {'date_path': date_path})


def carpatclim_d(request, year, month, day):
    """View with year/month/day embeded in page"""
    
    date_path = '%s/%s/%s' % (year, month, day)

    return render(request, 'carpatclimapp/simple.html', {'date_path': date_path})

