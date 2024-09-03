from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Plantilla(models.Model):
    nombre=models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Renglon(models.Model):
    plantilla=models.ForeignKey(
        Plantilla,
        on_delete=models.CASCADE
    )
    descripcion=models.CharField(max_length=25)
    dia=models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(31)]
    )
    monto = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0.00
    )
    activo=models.BooleanField(default=True)    

class Registro(models.Model):
    descripcion = models.CharField(max_length=25)
    monto = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0.00
    )
    fecha = models.DateField(verbose_name = "Fecha Vencimiento")
    pagado=models.BooleanField(default=False)
    plantilla=models.ForeignKey(
        Plantilla, models.DO_NOTHING, default=1
    )

