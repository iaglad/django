# Generated by Django 2.2.17 on 2020-12-22 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_student_student_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['-id'], 'verbose_name': 'Группа', 'verbose_name_plural': 'Группы'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['-id'], 'verbose_name': 'Студент', 'verbose_name_plural': 'Студенты'},
        ),
    ]
