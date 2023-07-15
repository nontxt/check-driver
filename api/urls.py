from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.create_order, name='create_order'),
    path('checks/<str:filename>', views.CheckView.as_view({'post': 'pdf', 'patch': 'printed'})),
    path('checks/', views.CheckView.as_view({'post': 'pdf_list'}), name='pdf_list'),
]
