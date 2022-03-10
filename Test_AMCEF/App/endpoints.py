from django.urls import path

from . import views

urlpatterns = [
    path('', views.addPost),
    path('<int:id>',views.apiHandler)

]