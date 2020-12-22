from django.db import models

# Create your models here.


class Student(models.Model):
    first_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Имя')

    last_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Фамилия')

    middle_name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name='Отчество',
        default='')

    birthday = models.DateField(
        blank=False,
        verbose_name='Дата рождения',
        null=True)

    photo = models.ImageField(
        blank=True,
        verbose_name='Фото',
        null=True)

    ticket = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Билет')

    notes = models.TextField(
        blank=True,
        verbose_name='Примечания')

    student_group = models.ForeignKey(
        'Group',
        verbose_name='Группа',
        blank=False,
        null=True,
        on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['-id']

    def __str__(self):
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()


class Group(models.Model):
    title = models.CharField(
        max_length=256,
        verbose_name='Название')

    leader = models.OneToOneField(
        'Student',
        verbose_name='Староста',
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

    notes = models.TextField(
        blank=True,
        verbose_name='Примечания')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['-id']

    def __str__(self):
        if self.leader:
            return '%s (%s %s)' % (self.title, self.leader.last_name, self.leader.first_name)
        else:
            return '%s' % (self.title,)
