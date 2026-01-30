from django.urls import path 
from .views import views95_full_bridge_phase_shift

urlpatterns = [
   path('full_bridge_phase_shift/', views95_full_bridge_phase_shift.full_bridge_phase_shift_converter, name = 'full_bridge_phase_shift'),
]

