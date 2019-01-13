from django.urls import path
from django.conf.urls import url
from . import views, views_test


urlpatterns = [

	path('', views.home, name='home'),
	path('yearly/', views.yearly, name='yearly'),
	#path('yearlyprec/', views.yearlyprec, name='yearlyprec'),
	path('monthly/', views.monthly, name='monthly'),
	#path('monthlyprec/', views.monthlyprec, name='monthlyprec'),
	path('daily/', views.daily, name='daily'),
	#path('dailyprec/', views.dailyprec, name='dailyprec'),    
	path('<var>/<inter>/<country>/<int:year>/<int:month>/<int:day>/figure.png', views.carpatclim_d_figure, name='carpatclim_d_figure'),
	#path('<inter>/<int:year>/<int:month>/<int:day>/figure.png', views.carpatclim_d_prec_figure, name='carpatclim_d_prec_figure'),
	path('<var>/<inter>/<country>/<int:year>/<int:month>/figure.png', views.carpatclim_m_figure, name='carpatclim_m_figure'),
	#path('<inter>/<int:year>/<int:month>/figure.png', views.carpatclim_m_prec_figure, name='carpatclim_m_prec_figure'),
	path('<var>/<inter>/<country>/<int:year>/figure.png', views.carpatclim_y_figure, name='carpatclim_y_figure'),
	#path('<inter>/<int:year>/figure.png', views.carpatclim_y_prec_figure, name='carpatclim_y_prec_figure'),
	path('<var>/<inter>/<country>/<int:year>/<int:month>/<int:day>/', views.carpatclim_d, name='carpatclim_d'),
	#path('<inter>/<int:year>/<int:month>/<int:day>/', views.carpatclim_d_prec, name='carpatclim_d_prec'),
	path('<var>/<inter>/<country>/<int:year>/<int:month>/', views.carpatclim_m, name='carpatclim_m'),
	#path('<inter>/<int:year>/<int:month>/', views.carpatclim_m_prec, name='carpatclim_m_prec'),
	path('<var>/<inter>/<country>/<int:year>/', views.carpatclim_y, name='carpatclim_y'),
	#path('<inter>/<int:year>/', views.carpatclim_y_prec, name='carpatclim_y_prec'),
	path('dataviewsy/', views.dataviewsy, name='dataviewsy'),
	path('dataviewsm/', views.dataviewsm, name='dataviewsm'),
	path('dataviewsd/', views.dataviewsd, name='dataviewsd'),
	path('cordinates/', views.cordinates, name='cordinates'),
	path('<lat>/<lon>/', views.carpatclim_point, name='carpatclim_point'),
	
	# test view examples

	path('test/', views_test.test, name='test'),
	path('test/simple/', views_test.simple, name='simple'),
	path('test/mplimage.png', views_test.mplimage, name='mplimage'),
	path('test/sine.png', views_test.show_sine, name='show_sine'),
]
