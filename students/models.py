from django.db import models

# Create your models here.


class Student(models.Model):
    first_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name="Имя"
    )

    last_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name="Фамилия"
    )

    middle_name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name="Отчество",
        default=''
    )

    birthday = models.DateField(
        blank=False,
        verbose_name="Дата рождения",
        null=True
    )

    photo = models.ImageField(
        blank=True,
        verbose_name="Фото",
        null=True
    )

    ticket = models.CharField(
        max_length=256,
        blank=False,
        verbose_name="Билет"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Примечания"
    )