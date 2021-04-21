# Generated by Django 3.1.7 on 2021-04-19 22:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
  

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210416_2225'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('time_minutes', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('links', models.CharField(blank=True, max_length=255)),
                ('ingrediants', models.ManyToManyField(to='core.Ingredient')),
                ('tag', models.ManyToManyField(to='core.Tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
