from django.urls import path

# from local apps
from .views import ManageUserView

from .views import ManageUserView


app_name = 'account'

urlpatterns = [
    # path('', views.home, name='home'),
    path('profile/', ManageUserView.as_view(), name='profile'),
]# f --- IGNORE ---