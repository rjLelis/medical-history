from django.db import models
from django.utils import timezone


class Profile(models.Model):
    username = models.CharField(max_length=50, unique=True)

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    date_of_birth = models.DateField(null=True)

    email = models.EmailField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'<Profile: {self.username}> {self.first_name} {self.last_name}'


class WeightHistory(models.Model):
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        Profile,
        related_name='weight_history',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user!s}\'s weight'

    def save(self, *args, **kwargs):
        super(WeightHistory, self).save(*args, **kwargs)
        Imc.objects.filter(user=self.user).update(
            current_weight=self.weight
        )


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
        default=PESO_NORMAL,
        null=True
    )

    imc = models.DecimalField(max_digits=4, decimal_places=2, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(
        Profile,
        related_name='imc',
        on_delete=models.CASCADE,
        unique=True
    )

    def _set_classificacao(self, imc):
        if imc < 17:
            self.classificacao = self.PESO_MUITO_ABAIXO
        elif 17 <= imc <= 18.49:
            self.classificacao = self.PESO_ABAIXO
        elif 18.50 <= imc <= 24.99:
            self.classificacao = self.PESO_NORMAL
        elif 25 <= imc <= 29.99:
            self.classificacao = self.PESO_ACIMA
        elif 30 <= imc <= 34.99:
            self.classificacao = self.OBESIDADE_I
        elif 35 <= imc <= 39.99:
            self.classificacao = self.OBESIDADE_II
        else:
            self.classificacao = self.OBESIDADE_III

    def save(self, *args, **kwargs):
        self.imc = self.current_weight / (self.current_height ** 2)
        self._set_classificacao(self.imc)
        super(Imc, self).save(*args, **kwargs)
        WeightHistory.objects.create(
            weight=self.current_weight,
            user=self.user
        )

    def __str__(self):
        return f'{self.user!s}\'s imc'
