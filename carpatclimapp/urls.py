from django.urls import path
from django.conf.urls import url
from . import views, views_test


urlpatterns = [
    path('', views.home, name='home'),
    path('yearly/', views.yearly, name='yearly'),
    path('monthly/', views.monthly, name='monthly'),
    path('daily/', views.daily, name='daily'),    
    path('<int:year>/<int:month>/<int:day>/figure.png', views.carpatclim_d_figure, name='carpatclim_d_figure'),
    path('<int:year>/<int:month>/figure.png', views.carpatclim_m_figure, name='carpatclim_m_figure'),
    path('<int:year>/figure.png', views.carpatclim_y_figure, name='carpatclim_y_figure'),
    path('<int:year>/<int:month>/<int:day>/', views.carpatclim_d, name='carpatclim_d'),
    path('<int:year>/<int:month>/', views.carpatclim_m, name='carpatclim_m'),
    path('<int:year>/', views.carpatclim_y, name='carpatclim_y'),
    path('cordinates/', views.cordinates, name='cordinates'),
    path('<lat>/<lon>/', views.carpatclim_point, name='carpatclim_point'),
    # test view examples
    path('test/', views_test.test, name='test'),
    path('test/simple/', views_test.simple, name='simple'),
    path('test/mplimage.png', views_test.mplimage, name='mplimage'),
    path('test/sine.png', views_test.show_sine, name='show_sine'),
]
