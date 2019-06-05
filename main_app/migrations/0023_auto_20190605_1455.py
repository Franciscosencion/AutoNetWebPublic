# Generated by Django 2.1 on 2019-06-05 18:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0022_auto_20190604_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicedetail',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='createdby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='devicedetail',
            name='last_modify',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='devicedetail',
            name='modified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modifiedby', to=settings.AUTH_USER_MODEL),
        ),
    ]
