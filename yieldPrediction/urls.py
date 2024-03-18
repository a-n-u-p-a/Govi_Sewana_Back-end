<<<<<<< HEAD
from django.urls import path
from . import views

urlpatterns = [
    path('predictor/', views.predictor, name='predictor'),
]
=======
from django.urls import path
from . import views

urlpatterns = [
    path('', views.predictor, name = 'predictor'),
]
>>>>>>> 7ef29c090b6300e9d7ec70a747fd81796baea790
