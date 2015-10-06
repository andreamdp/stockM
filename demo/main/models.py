# -*- encoding: utf-8 -*-
from django.db import models
from datetime import date
class Proveedor(models.Model):
	codigo =models.CharField('Código',max_length=32, unique=True)
	nombre=models.CharField(max_length=200)
	telefono=models.CharField(max_length=200, null=True, blank= True)
	direccion= models.CharField(max_length=200, null=True, blank= True)
	mail=models.CharField(max_length=50,null=True, blank= True)

class Producto(models.Model):
    codigo = models.CharField('Código',max_length=32, unique=True)
    nombre = models.CharField(max_length=64)
    precioCosto = models.FloatField( 'Costo',null=True, blank=True)
    precioVta = models.FloatField('Precio de Venta',null=True, blank=True)
    qty = models.PositiveIntegerField(default=0)
    proveedor= models.ForeignKey('Proveedor')
    def update_qty(self, qty):
        """ creates a movement with the diff """
        mov, _ = Movimiento.objects.get_or_create(producto=self, dia=date.today())
        mov.qty += qty - self.qty
        mov.save()
        self.qty = qty
        self.save()

    def qty_on(self, day):
        """ returns qty on specific day """
        return self.qty - sum(
            Movimiento.objects.filter(producto=self, day__range=(dia,
                date.today())).values_list('qty', flat=True))
class Movimiento(models.Model):
    producto = models.ForeignKey(Producto)
    dia = models.DateField(default=date.today())
    qty = models.IntegerField(default=0)

    class Meta:
        unique_together = ('producto', 'dia')
