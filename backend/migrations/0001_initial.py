# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaceSpaceUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('birthday', models.DateField()),
                ('is_male', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'facespaceusers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_link', models.URLField()),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ads',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bid_time', models.DateTimeField()),
                ('bid_price', models.DecimalField(max_digits=9, decimal_places=2)),
                ('holds', models.ForeignKey(related_name='holding_ad_slots', to='backend.Ad')),
            ],
            options={
                'db_table': 'adslots',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
            ],
            options={
                'db_table': 'comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'entities',
                'verbose_name_plural': 'Entities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('since', models.DateField()),
                ('from_friend', models.ForeignKey(related_name='from_friend', to=settings.AUTH_USER_MODEL)),
                ('to_friend', models.ForeignKey(related_name='to_friend', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'friendships',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('parent', models.ForeignKey(related_name='children', to='backend.Interest', null=True)),
            ],
            options={
                'db_table': 'interests',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_positive', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'likes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('entity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='backend.Entity')),
                ('caption', models.TextField()),
                ('file_name', models.CharField(max_length=75)),
            ],
            options={
                'db_table': 'photos',
            },
            bases=('backend.entity',),
        ),
        migrations.CreateModel(
            name='Romance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('romance_type', models.CharField(default=b'Dating', max_length=10, choices=[(b'Dating', b'Dating'), (b'Engaged', b'Engaged'), (b'Married', b'Married')])),
                ('since', models.DateField()),
                ('until', models.DateField(null=True, blank=True)),
                ('from_partner', models.ForeignKey(related_name='from_partner', to=settings.AUTH_USER_MODEL)),
                ('to_partner', models.ForeignKey(related_name='to_partner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'romances',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('entity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='backend.Entity')),
                ('text', models.TextField()),
            ],
            options={
                'db_table': 'statuses',
            },
            bases=('backend.entity',),
        ),
        migrations.AlterUniqueTogether(
            name='romance',
            unique_together=set([('from_partner', 'to_partner', 'since')]),
        ),
        migrations.AddField(
            model_name='like',
            name='entity',
            field=models.ForeignKey(to='backend.Entity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=set([('user', 'entity')]),
        ),
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together=set([('from_friend', 'to_friend')]),
        ),
        migrations.AddField(
            model_name='entity',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='entity',
            field=models.ForeignKey(to='backend.Entity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='adslot',
            name='interest',
            field=models.OneToOneField(to='backend.Interest'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='adslot',
            name='will_hold',
            field=models.ForeignKey(related_name='will_hold_ad_slots', to='backend.Ad', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facespaceuser',
            name='friends',
            field=models.ManyToManyField(related_name='friend', through='backend.Friendship', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facespaceuser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facespaceuser',
            name='interests',
            field=models.ManyToManyField(to='backend.Interest', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facespaceuser',
            name='profile_picture',
            field=models.ForeignKey(blank=True, to='backend.Photo', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facespaceuser',
            name='relationship_with',
            field=models.ManyToManyField(related_name='relationship', through='backend.Romance', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facespaceuser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
    ]
