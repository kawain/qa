# Generated by Django 3.1.7 on 2021-03-29 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='タイトル')),
                ('price', models.IntegerField(verbose_name='価格')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.IntegerField(choices=[(1, '★1'), (2, '★2'), (3, '★3'), (4, '★4'), (5, '★5')], verbose_name='評価点')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study1.book', verbose_name='評価対象の本')),
            ],
        ),
    ]