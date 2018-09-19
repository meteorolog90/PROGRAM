import io
import random
import datetime

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from matplotlib import pylab


from django.http import HttpResponse
from django.shortcuts import render

def test(request):
    """Test page"""
    
    return render(request, 'carpatclimapp/test.html')


def simple(request):
    """
    Matplot image view simple example

    From tutorial:
    https://scipy-cookbook.readthedocs.io/items/Matplotlib_Django.html
    """

    fig = Figure()
    ax = fig.add_subplot(111)
    x = []
    y = []
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now += delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)

    buffer = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buffer)

    response = HttpResponse(buffer.getvalue(), content_type='image/png')

    # I recommend to add Content-Length for Django
    response['Content-Length'] = str(len(response.content))

    return response


def mplimage(request):
    """
    Matplot image view simple example 2

    At the moment, matplotlib's writing functions require the seek ducktype
    to use the response at a file.
    https://stackoverflow.com/questions/49542459/error-in-django-when-using-matplotlib-examples
    """

    fig = Figure()
    buffer = io.BytesIO()

    ax = fig.add_subplot(111)
    x = np.arange(-2,1.5,.01)
    y = np.sin(np.exp(2*x))
    ax.plot(x, y)

    canvas = FigureCanvas(fig)

    # Store image in a string buffer
    canvas.print_png(buffer)

    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    # I recommend to add Content-Length for Django
    response['Content-Length'] = str(len(response.content))

    # if required clear the figure for reuse
    fig.clear()

    return response


def show_sine(request):
    """
    Sine graph

    URL: https://www.eriksmistad.no/making-charts-and-outputing-them-as-images-to-the-browser-in-django/
    https://matplotlib.org/examples/pylab_examples/pythonic_matplotlib.html
    """

    fig = Figure()
    buffer = io.BytesIO()
    ax = fig.add_subplot(111)
    
    # Construct the graph
    t = np.arange(0.0, 2.0, 0.01)
    s = np.sin(2*np.pi*t)

    ax.plot(t, s, linewidth=1.0)
    ax.set_xlabel('time (s)')
    ax.set_ylabel('voltage (mV)')
    ax.set_title('Sine signal')
    ax.grid(True)
    ax.plot(t, s)
 
    canvas = FigureCanvas(fig)

    # Store image in a string buffer
    canvas.print_png(buffer)
    
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    # I recommend to add Content-Length for Django
    response['Content-Length'] = str(len(response.content))

    # if required clear the figure for reuse
    fig.clear()

    # Send buffer in a http response the the browser with the mime type image/png set
    return response
