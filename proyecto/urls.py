from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from proyecto.views import tienda, agregar_producto, eliminar_producto, restar_producto, limpiar_carrito
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    
    path("home/",views.home, name="home" ),
    path("moca/", views.moca, name="moca" ),
    path("login/", views.login_t, name="login_t"),
    path('logout/', auth_views.LogoutView.as_view(next_page='login_t'), name='logout'),  # Usa auth_views.LogoutView para manejar el cierre de sesión
    path("beneficio/", views.beneficio, name="beneficio"),
    path("expreso/", views.expreso, name="expreso"),
    path("capuchino/", views.capuchino, name="capuchino"),
    path("carrito/", views.carrito, name="carrito"),
    path('Tienda/', tienda, name="tienda"),
    path('agregar/<int:producto_id>/', agregar_producto, name="Add"),
    path('eliminar/<int:producto_id>/', eliminar_producto, name="Del"),
    path('restar/<int:producto_id>/', restar_producto, name="Sub"),
    path('limpiar/', limpiar_carrito, name="CLS"),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('factura/', views.generar_factura, name='factura'),
    path('registro/', views.registrar_cliente, name='registro_cliente'),
    path('', views.login_t, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
    
    
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
