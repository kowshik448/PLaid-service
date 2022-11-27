# Generated by Django 4.1.3 on 2022-11-26 16:28

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('plaid_account_id', models.CharField(max_length=200, null=True, unique=True)),
                ('balances', models.JSONField(null=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('account_type', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('account_owner', models.CharField(max_length=200, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('authorized_date', models.CharField(max_length=200, null=True)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 11, 26, 21, 58, 55, 629968))),
                ('name', models.CharField(max_length=200, null=True)),
                ('payment_meta', models.JSONField(null=True)),
                ('payment_channel', models.CharField(max_length=200, null=True)),
                ('pending', models.BooleanField(null=True)),
                ('pending_transaction_id', models.CharField(max_length=200, null=True)),
                ('transaction_id', models.CharField(max_length=200, null=True, unique=True)),
                ('transaction_type', models.CharField(max_length=200, null=True)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='plaidApp.account')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlaidItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=200, unique=True)),
                ('item_id', models.CharField(max_length=200, unique=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='item',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='plaidApp.plaiditem'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
