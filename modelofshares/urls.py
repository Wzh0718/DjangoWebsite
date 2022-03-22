from django.urls import path

from modelofshares import views

urlpatterns = [
    path('', views.login),
    path('login', views.login),
    path('regist', views.regist),
    path('recompose', views.recompose),
    path('index', views.index),
    # path('/index', views.index),
]
