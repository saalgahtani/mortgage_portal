from django.contrib import admin
from django.urls import path
from src_gateway import views as gateway_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Bank Login & Logout
    path('login/', gateway_views.bank_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Bank Upload Portal
    path('bank-upload/', gateway_views.bank_upload, name='bank_upload'),

    # SRC Portal and Secure Download
    path('src-portal/', gateway_views.src_portal, name='src_portal'),
    path('download/<str:bank_name>/<str:filename>/', gateway_views.secure_download, name='secure_download'),
]
