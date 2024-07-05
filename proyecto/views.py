from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import Producto, Compra, Cliente
from proyecto.Carrito import Carrito
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from proyecto.forms import CustomUserChangeForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden


# Create your views here.

def home(request):
    context = {
        'username': request.user.username if request.user.is_authenticated else None
    }
    return render(request, "proyecto/index.html", context)

def moca(request):
    context={

    }
    return render(request,"proyecto/moca.html",context)

def login_t(request):

    if request.method== "POST":
        usuario= request.POST["username"]
        contrasena= request.POST["password"]
        user= authenticate(request, username= usuario, password= contrasena)
    
        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            return redirect('login_t') 
    else:

        context={ 
        }   
        return render(request,"proyecto/login.html",context)

def beneficio(request):
    context={

    }
    return render(request,"proyecto/beneficio.html",context)

def expreso(request):
    context={

    }
    return render(request,"proyecto/expreso.html",context)

def capuchino(request):
    context={

    }
    return render(request,"proyecto/capuchino.html",context)

def carrito(request):
    # Lógica de la vista carrito aquí
    return render(request, 'proyecto/carrito.html', {})  # Ejemplo de renderización de un template



def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)

    # Si el usuario decide realizar la compra desde el carrito
    if request.method == 'POST':
        try:
            with transaction.atomic():
                total_compra = Decimal('0.0')  # Inicializar el total de la compra como Decimal

                # Guardar cada producto del carrito como una compra asociada al usuario
                for item in carrito:
                    precio_unitario = Decimal(item['producto'].precio)
                    cantidad = item['cantidad']
                    total_item = precio_unitario * cantidad
                    total_compra += total_item

                    compra = Compra(
                        usuario=request.user,
                        producto=item['producto'],
                        cantidad=cantidad,
                        precio_unitario=precio_unitario,
                        total=total_item
                    )
                    compra.save()

                # Limpiar el carrito después de completar la compra
                carrito.limpiar()

        except Exception as e:
            # Manejar cualquier error que pueda ocurrir durante la transacción
            print(f"Error al realizar la compra: {e}")
            return redirect('tienda')  # Redirigir a la tienda o manejar el error según tu aplicación

        # Redirigir a la generación de factura después de completar la compra
        return redirect('generar_factura')

    return redirect('tienda')

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect("tienda")

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("tienda")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("tienda")

def tienda(request):
    productos = Producto.objects.all()
    return render(request, "proyecto/tienda.html", {'productos': productos})

def nosotros(request):
    # Aquí puedes agregar información sobre la cafetería
    informacion = {
        'nombre_cafeteria': 'Baristas',
        'descripcion': 'Matias Gonzalez - Dueño De Baristas.',
        'direccion': 'Calle Principal Grecia, Santiago, Chile',
        'telefono': '+56934567890',
        'email': 'info@cafeteriaBarista.com',
        'imagen_url': '/static/img/chico.jpg',  # Ruta de la imagen en tu proyecto
    }
    return render(request, 'proyecto/nosotros.html', informacion)

def generar_factura(request):
    # Obtener los datos del carrito desde la sesión
    carrito = request.session.get('carrito', {})
    
    # Calcular el total de la factura
    total_carrito = sum(item['acumulado'] for item in carrito.values())

    # Aquí podrías agregar más lógica para generar tu factura
    # Por ejemplo, crear un objeto de factura en la base de datos, etc.

    # Renderizar la plantilla de la factura
    return render(request, 'proyecto/factura.html', {
        'carrito': carrito,
        'total_carrito': total_carrito,
    })

def registro(request):
    if request.method == "POST":
        user_name = request.POST["nombre_user"]
        nombre = request.POST["nombre"]
        p_apellido = request.POST["pri_apellido"]
        s_apellido = request.POST["seg_apellido"]
        contrasena = request.POST["contra_user"]
        email = request.POST["email"]
        try:

            usuario = User.objects.get(username=user_name)

            mensaje = "Este nombre de usuario ya está siendo ocupado"
            context = {
                "mensaje": mensaje
            }
            return render(request, "proyecto/registro.html", context)
        except:
            user = User.objects.create_user(user_name, email, contrasena)
            user.save()
            cliente = Cliente.objects.create(
                user=user,
                nombre=nombre,
                primer_apellido=p_apellido,
                segundo_apellido=s_apellido,
                direccion=None,
                telefono=None

            )
            cliente.save()
            login(request, user)
            return redirect('home')
    else:
        return render(request, "proyecto/registro.html", {})
    
def registrar_cliente(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_user')
        nombre = request.POST.get('nombre')
        primer_apellido = request.POST.get('pri_apellido')
        segundo_apellido = request.POST.get('seg_apellido')
        correo_electronico = request.POST.get('email')
        contraseña = request.POST.get('contra_user')

        # Crear un nuevo objeto Cliente con los datos recibidos
        nuevo_cliente = Cliente(
            nombre_usuario=nombre_usuario,
            nombre=nombre,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            correo_electronico=correo_electronico,
            contraseña=contraseña
        )

        # Guardar el objeto en la base de datos
        nuevo_cliente.save()

        # Redirigir a alguna página de confirmación o a donde desees después de guardar
        return redirect('home')  # Reemplaza 'ruta_a_tu_pagina_de_confirmacion' con la URL adecuada

    return render(request, 'proyecto/registro.html')

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user, request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Tu perfil ha sido actualizado correctamente.')
            return redirect('profile')
        elif password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Actualiza la sesión si la contraseña cambió
            messages.success(request, 'Tu contraseña ha sido actualizada correctamente.')
            return redirect('profile')
        else:
            messages.error(request, 'Por favor, corrige los errores.')
    else:
        user_form = CustomUserChangeForm(instance=user)
        password_form = PasswordChangeForm(user)
    
    context = {
        'user': user,
        'user_form': user_form,
        'password_form': password_form,
    }
    return render(request, 'proyecto/profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Tu perfil ha sido actualizado correctamente.')
            return redirect('edit_profile')
        else:
            messages.error(request, 'Por favor, corrige los errores.')
    else:
        user_form = CustomUserChangeForm(instance=user)
    
    context = {
        'user_form': user_form,
    }
    return render(request, 'proyecto/edit_profile.html', context)

@login_required
def lista_compras_admin(request):
    if not request.user.is_staff:
        return HttpResponseForbidden('No tienes permiso para acceder a esta página.')
    
    compras = Compra.objects.all().order_by('-fecha_compra')
    return render(request, 'proyecto/lista_compras.html', {'compras': compras})

