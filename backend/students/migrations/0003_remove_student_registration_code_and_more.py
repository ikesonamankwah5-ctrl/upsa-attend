from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_student_registration_code_student_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='registration_code',
            new_name='registration_code_hash',
        ),
        migrations.AlterField(
            model_name='student',
            name='registration_code_hash',
            field=models.CharField(
                max_length=128,
                unique=True,
                null=True,
                blank=True
            ),
        ),
    ]