from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_instructor_to_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='instructor',
        ),
    ]
