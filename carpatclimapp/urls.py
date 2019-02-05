from django.urls import path
from django.conf.urls import url
from . import views, views_test


urlpatterns = [

	path('', views.home, name='home'),
	path('yearly/', views.yearly, name='yearly'),
	path('monthly/', views.monthly, name='monthly'),
	path('daily/', views.daily, name='daily'),
	path('yearly_period/', views.yearly_period, name='yearly_period'),
	path('monthly_period/', views.monthly_period, name='monthly_period'),
	path('daily_period/', views.daily_period, name='daily_period'),
	path('<var>/<inter>/<int:year>/<int:month>/<int:day>/figure.png', views.carpatclim_d_figure, name='carpatclim_d_figure'),
	path('<var>/<inter>/<int:year>/<int:month>/figure.png', views.carpatclim_m_figure, name='carpatclim_m_figure'),
	path('<var>/<inter>/<int:year>/figure.png', views.carpatclim_y_figure, name='carpatclim_y_figure'),
	path('<var>/<inter>/<int:year>/<int:month>/<int:day>/', views.carpatclim_d, name='carpatclim_d'),
	path('<var>/<inter>/<int:year>/<int:month>/', views.carpatclim_m, name='carpatclim_m'),
	path('<var>/<inter>/<int:year>/', views.carpatclim_y, name='carpatclim_y'),
	path('<var>/<year>/<year1>/<lon>/<lat>/<inter>/', views.period_year_prec, name = 'period_year_prec'),
	path('<var>/<year>/<month>/<year1>/<month1>/<lon>/<lat>/<inter>/', views.period_month_prec, name = 'period_month_prec'),
	path('<var>/<year>/<month>/<day><year1>/<month1>/<day1><lon>/<lat>/<inter>/', views.period_daily_temp, name = 'period_daily_temp'),
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
