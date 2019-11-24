# Generated by Django 2.2.6 on 2019-11-18 07:59

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='allUserFavorite',
            fields=[
                ('allUserFavorite_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('headline', models.CharField(max_length=250)),
                ('summary', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('cluster_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('cluster_headline', models.CharField(blank=True, max_length=250, null=True)),
                ('cluster_summary', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewsSummary',
            fields=[
                ('news_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('headline', models.CharField(max_length=250)),
                ('summary', models.TextField(blank=True, null=True)),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('pub_date', models.DateTimeField(blank=True, null=True, verbose_name='Date Published')),
                ('sum_date', models.DateTimeField(auto_now_add=True, verbose_name='Date Summarized')),
                ('category', models.CharField(max_length=20)),
                ('cluster_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='newsArticles.Cluster')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=40, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('rating_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('score', models.IntegerField(default=0)),
                ('news_summary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsArticles.NewsSummary')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsArticles.User')),
            ],
        ),
        migrations.CreateModel(
            name='Recommend',
            fields=[
                ('recommend_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('cluster_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsArticles.Cluster')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsArticles.User')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('favorite_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('allUserFav_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsArticles.allUserFavorite')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsArticles.User')),
            ],
        ),
    ]