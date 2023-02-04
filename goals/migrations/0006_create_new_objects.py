from django.db import migrations, transaction
from django.utils import timezone


def create_objects(apps, schema_editor):
    user_model = apps.get_model('core', 'User')
    board_model = apps.get_model('goals', 'Board')
    board_participant_model = apps.get_model('goals', 'BoardParticipant')
    goal_category_model = apps.get_model('goals', 'GoalCategory')

    time_now = timezone.now()

    with transaction.atomic():
        for user in user_model.objects.all():
            new_board = board_model.objects.create(
                title='Мои цели',
                created=time_now,
                updated=time_now
            )
            board_participant_model.objects.create(
                user=user,
                board=new_board,
                role=1,
                created=time_now,
                updated=time_now
            )
            goal_category_model.objects.filter(user=user).update(board=new_board)


class Migration(migrations.Migration):
    dependencies = [
        ('goals', '0005_board_alter_goal_category_alter_goalcomment_user_and_more'),
    ]

    operations = [
        migrations.RunPython(create_objects)
    ]
