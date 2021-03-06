# Generated by Django 3.2 on 2021-04-08 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20210408_2046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='The name of your attribute.', max_length=255, verbose_name='label')),
                ('min_value', models.PositiveIntegerField(default=1)),
                ('max_value', models.PositiveIntegerField(default=5)),
                ('upgrade_multiplier', models.PositiveIntegerField(default=5)),
                ('notes', models.TextField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='DerivedValues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modifier', models.PositiveIntegerField(default=0)),
                ('attribute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='games.attribute')),
            ],
        ),
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(help_text='How you refer to your game.', max_length=255, verbose_name='name'),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='The name of your skill.', max_length=255, verbose_name='label')),
                ('min_value', models.PositiveIntegerField(default=1)),
                ('max_value', models.PositiveIntegerField(default=14)),
                ('notes', models.TextField(blank=True, max_length=500)),
                ('can_be_expert_skill', models.BooleanField(default=False, help_text='Lil6 allows for a concept of "Expert Skills" but not all Open D6 games use this. In addition some Lil6 Skills cannot be taken as an Expert Skill.')),
                ('parent_attribute', models.ForeignKey(blank=True, help_text='The attribute this skill inherits a starting value form. Leave blank to have it as a standalone skill.', null=True, on_delete=django.db.models.deletion.CASCADE, to='games.attribute')),
            ],
        ),
        migrations.CreateModel(
            name='GameSkills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.game')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.skill')),
            ],
        ),
        migrations.CreateModel(
            name='GameDerivedValues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('derived_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.derivedvalues')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.game')),
            ],
        ),
        migrations.CreateModel(
            name='GameAttributes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.attribute')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.game')),
            ],
        ),
        migrations.AddField(
            model_name='derivedvalues',
            name='skill',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='games.skill'),
        ),
        migrations.AddField(
            model_name='game',
            name='attributes',
            field=models.ManyToManyField(through='games.GameAttributes', to='games.Attribute'),
        ),
        migrations.AddField(
            model_name='game',
            name='derived_values',
            field=models.ManyToManyField(through='games.GameDerivedValues', to='games.DerivedValues'),
        ),
        migrations.AddField(
            model_name='game',
            name='skills',
            field=models.ManyToManyField(through='games.GameSkills', to='games.Skill'),
        ),
    ]
