import io
import random
import datetime

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from matplotlib import pylab
from pylab import *
import PIL, PIL.Image

from django.http import HttpResponse
from django.shortcuts import render

def test(request):
    """Test page"""
    
    return render(request, 'carpatclimapp/test.html')


def simple(request):
    """
    Matplot image view example

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

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    # fig.clear()

    response = HttpResponse(content_type='image/png')

    # I recommend to add Content-Length for Django
    response['Content-Length'] = str(len(response.content))

    canvas.print_png(response)
    return response


def mplimage(request):
    """
    Matplot image view simple example 2
    
    https://stackoverflow.com/questions/45460145/how-to-render-a-matplotlib-plot-in-a-django-web-application
    """

    fig = Figure()
    canvas = FigureCanvas(fig)

    ax = fig.add_subplot(111)
    x = np.arange(-2,1.5,.01)
    y = np.sin(np.exp(2*x))
    ax.plot(x, y)

    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


def mplimage2(request):
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
    canvas.print_png(buffer)

    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    # I recommend to add Content-Length for Django
    response['Content-Length'] = str(len(response.content))

    # if required clear the figure for reuse
    fig.clear()

    return response


def showimage(request):
    """
    Sine graph

    URL: ??
    """
    # Construct the graph
    t = arange(0.0, 2.0, 0.01)
    s = sin(2*pi*t)
    plot(t, s, linewidth=1.0)
 
    xlabel('time (s)')
    ylabel('voltage (mV)')
    title('About as simple as it gets, folks')
    grid(True)
 
    # Store image in a string buffer
    buffer = io.BytesIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    pilImage = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
    pilImage.save(buffer, "PNG")
    pylab.close()
 
    # Send buffer in a http response the the browser with the mime type image/png set
    return HttpResponse(buffer.getvalue(), content_type="image/png")
