from django.db import models

# Create your models here.


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
