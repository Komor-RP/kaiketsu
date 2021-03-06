from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date


class User(AbstractUser):
    first_name = models.CharField(max_length=50, null=True)
    USERNAME_FIELD = 'username'

    def get_days(self):
        grouped_days = [goal.days.all() for goal in self.goals.all()]
        days = [day for goals in grouped_days for day in goals]
        return days


class DateStamp(models.Model):
    created_at = models.DateField(auto_now_add=True, null=True)

    class Meta:
        abstract = True


class Goal(DateStamp):
    resolution = models.TextField(null=True)
    reason = models.TextField(null=True)

    DURATION_CHOICES = (
        (timedelta(days=10), '10 Days'),
        (timedelta(days=30), '30 Days'),
        (timedelta(days=60), '60 Days'),
        (timedelta(days=90), '90 Days'),
    )
    duration = models.DurationField(choices=DURATION_CHOICES, null=True)

    TYPE_CHOICES = (
        ('HEALTH', 'HEALTH'),
        ('PROFESSIONAL', 'PROFESSIONAL'),
        ('PERSONAL', 'PERSONAL'),
    )
    category = models.CharField(choices=TYPE_CHOICES, null=True, max_length=20)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='goals'
        )
    active = models.BooleanField(default=True, editable=True)

    def get_days(self):
        return self.days.all().order_by('created_at')

    def log_day_as_false(self):
        today = date.today()
        has_day = self.days.filter(created_at=today)
        if not has_day:
            GoalDay.objects.create(
                goal_met=False,
                goal=self,
                created_at=today)


class GoalDay(DateStamp):
    goal_met = models.BooleanField(default=False)
    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name='days'
        )

    class Meta:
        unique_together = ('created_at', 'goal')

    def save(self, *args, **kwargs):
        super(GoalDay, self).save(*args, **kwargs)
        if self.goal.duration.days == len(self.goal.days.all()):
            self.goal.active = False
            self.goal.save()


class TimePie(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_free_hours_per_week(self):
        sum_of_sections = sum(
            [timepie.hours for timepie in self.sections.all()]
            )
        return (24 - sum_of_sections) * 7


class TimeSection(models.Model):
    title = models.CharField(max_length=255)
    timepie = models.ForeignKey(
        TimePie,
        on_delete=models.CASCADE,
        null=True,
        related_name='sections'
        )
    hours = models.DecimalField(decimal_places=1, max_digits=3)

    def __str__(self):
        return self.title

    def clean(self):
        sum_of_sections = sum(
            [timepie.hours for timepie in self.timepie.sections.all()]
            )
        if self.pk is None:
            if self.hours + sum_of_sections > 24:
                raise ValidationError(
                    _('Time sections can not add up over 24.'))
        else:
            if sum_of_sections > 24:
                raise ValidationError(
                    _('Time sections can not add up over 24.'))
