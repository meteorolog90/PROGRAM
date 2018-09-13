from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('<int:year>/<int:month>/<int:day>/figure.png', views.carpatclim_d_figure, name='carpatclim_d_figure'),
    path('<int:year>/<int:month>/figure.png', views.carpatclim_m_figure, name='carpatclim_m_figure'),
    path('<int:year>/figure.png', views.carpatclim_y_figure, name='carpatclim_y_figure'),
    path('<int:year>/<int:month>/<int:day>/', views.carpatclim_d, name='carpatclim_d'),
    path('<int:year>/<int:month>/', views.carpatclim_m, name='carpatclim_m'),
    path('<int:year>/', views.carpatclim_y, name='carpatclim_y'),
    # test view examples
]
