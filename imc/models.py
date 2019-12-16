from django.db import models
from django.contrib.auth.models import User

class WeightHistory(models.Model):

    weight = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Imc(models.Model):

    PESO_MUITO_ABAIXO = 'PP'
    PESO_ABAIXO = 'P'
    PESO_NORMAL = 'M'
    PESO_ACIMA = 'G'
    OBESIDADE_I = 'GG'
    OBESIDADE_II = 'XG'
    OBESIDADE_III = 'XGG'

    CLASSIFICACAO = (
        (PESO_MUITO_ABAIXO, 'Muito abaixo do peso'),
        (PESO_ABAIXO, 'Abaixo do peso'),
        (PESO_NORMAL, 'Peso normal'),
        (PESO_ACIMA, 'Obesidade'),
        (OBESIDADE_I, 'Acima do peso'),
        (OBESIDADE_II, 'Obesidade II (severa)'),
        (OBESIDADE_III, 'Obesidade III (mórbida)'),
    )

    current_height = models.DecimalField(max_digits=4, decimal_places=2)
    current_weight = models.DecimalField(max_digits=5, decimal_places=2)
    classificacao = models.CharField(
        max_length=25,
        choices=CLASSIFICACAO,
        default=PESO_NORMAL
    )
    imc = models.DecimalField(max_digits=4, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def switch_imc(self):
        if self.imc < 17:
            self.classificacao = self.PESO_MUITO_ABAIXO
        elif self.imc >= 17 and self.imc <= 18.49:
            self.classificacao = self.PESO_ABAIXO
        elif self.imc >= 18.50 and self.imc <= 24.99:
            self.classificacao = self.PESO_NORMAL
        elif self.imc >= 25 and self.imc <= 29.99:
            self.classificacao = self.PESO_ACIMA
        elif self.imc >= 30 and self.imc <= 34.99:
            self.classificacao = self.OBESIDADE_I
        elif self.imc >= 35 and self.imc <= 39.99:
            self.classificacao = self.OBESIDADE_II
        else:
            self.classificacao = self.OBESIDADE_III


    def save(self, *args, **kwargs):
        self.imc = self.current_weight / (self.current_height ** 2)
        self.set_imc_classification()
        super(Imc, self).save(*args, **kwargs)
