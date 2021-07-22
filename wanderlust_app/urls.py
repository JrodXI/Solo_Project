from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('dashboard', views.dashboard),
    path('process_message', views.post_message),
    path('add_comment/<int:id>', views.post_comment),
    path('like/<int:id>', views.add_like),
    path('delete/<int:id>', views.delete_comment),
    path('edit/<int:id>', views.edit),
    path('trips/new', views.new),
    path('trips/create', views.create),
    path('trips/<int:id>', views.show),
    path('trips/edit/<int:id>', views.edit),
    path('trips/<int:id>/update', views.update),
    path('trips/<int:id>/join', views.join),
    path('trips/<int:id>/delete', views.delete),
    path('trips/<int:id>/cancel', views.cancel),
    path('logout', views.logout),
]