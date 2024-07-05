class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

    def agregar(self, producto):
        producto_id = str(producto.id)
        if producto_id not in self.carrito:
            self.carrito[producto_id] = {
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "precio": float(producto.precio),  # Convertir Decimal a float
                "acumulado": float(producto.precio),  # Convertir Decimal a float
                "cantidad": 1,
            }
        else:
            self.carrito[producto_id]["cantidad"] += 1
            self.carrito[producto_id]["acumulado"] += float(producto.precio)  # Convertir Decimal a float

        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            self.carrito[producto_id]["cantidad"] -= 1
            self.carrito[producto_id]["acumulado"] -= float(producto.precio)
            if self.carrito[producto_id]["cantidad"] <= 0:
                del self.carrito[producto_id]

        self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True