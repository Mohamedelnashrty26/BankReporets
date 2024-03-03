from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
# from .views import UserAPIView, ObtainTokenAPIView, CreateUserAPIView
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    # Swagger documentation endpoints
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('register/', views.UserRegistrationAPIView.as_view(), name='user-register'),
    path('login/', views.UserLoginAPIView.as_view(), name='user-login'),
    path('update/', views.UserUpdateAPIView.as_view(), name='user-update'),
    path('delete/', views.UserDeleteAPIView.as_view(), name='user-delete'),
 
    # API endpoints
    # path('api/users/', UserAPIView.as_view(), name='user-list'),
    # path('api/users/<int:pk>/', UserAPIView.as_view(), name='user-detail'),
    # path('api/token/', ObtainTokenAPIView.as_view(), name='token'),
    # path('api/register/', CreateUserAPIView.as_view(), name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
