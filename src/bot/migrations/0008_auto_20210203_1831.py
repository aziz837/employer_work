# Generated by Django 3.1.5 on 2021-02-03 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0007_auto_20210129_1208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='region',
            name='parend_id',
        ),
        migrations.AddField(
            model_name='order',
            name='Region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bot.region'),
        ),
        migrations.AddField(
            model_name='order',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='cat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bot.category'),
        ),
        migrations.AlterField(
            model_name='user',
            name='tg_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bot.region')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bot.district'),
        ),
        migrations.CreateModel(
            name='UserRegion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bot.district')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.region')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.user')),
            ],
            options={
                'unique_together': {('user', 'region', 'district')},
            },
        ),
    ]