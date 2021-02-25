from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

class QQ:
    def __xor__(self, other):
        return (self & (~other)) | ((~self) & other)

Q.__bases__ += (QQ, )

class Boulder(models.Model):
    name = models.CharField(max_length=64)
    difficulty = models.ForeignKey(
        'BoulderDifficulty',
        null=True,
        on_delete=models.PROTECT,
        related_name='boulders',
    )
    mountainproject = models.URLField(null=True)

class BoulderDifficulty(models.Model):
    order = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=8)

class Pitch(models.Model):
    route = models.ForeignKey(
        'Route',
        on_delete=models.CASCADE,
        related_name='pitches',
    )
    difficulty = models.ForeignKey(
        'RouteDifficulty',
        on_delete=models.PROTECT,
        related_name='pitches',
    )

PROTECTION_STYLE_CHOICES = (
    ('sport', 'Sport'),
    ('toprope', 'Top Rope'),
    ('trad', 'Trad'),
)

class Route(models.Model):
    name = models.CharField(max_length=64)
    protection_style = models.CharField(max_length=8, choices=PROTECTION_STYLE_CHOICES)
    mountainproject = models.URLField(null=True)

    # TODO Write test for this
    @property
    def difficulty(self):
        return self.pitches.order_by('-difficulty__order').first().difficulty

class RouteDifficulty(models.Model):
    order = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=8)

ATTEMPT_RESULT_CHOICES = (
    ('send', 'Sent'),
    ('fall', 'Fall'),
)

PROTECTION_CHOICES = (
    ('none', 'None'),
    ('bolts', 'Bolts'),
    ('gear', 'Gear'),
    ('pad', 'Pad'),
    ('tr', 'Top Rope'),
)

class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField()
    boulder = models.ForeignKey('Boulder', null=True, on_delete=models.PROTECT, related_name='attempts')
    route = models.ForeignKey('Route', null=True, on_delete=models.PROTECT, related_name='attempts')
    result = models.CharField(max_length=8, choices=ATTEMPT_RESULT_CHOICES)
    prior_knowledge = models.BooleanField(default=True)
    protection_used = models.CharField(max_length=8, choices=PROTECTION_CHOICES)

    class Meta:
        constraints = (
            models.CheckConstraint(
                check=(Q(boulder__isnull=True) ^ Q(route__isnull=True)),
                name='attempt_boulder_xor_route',
            ),
        )

STYLE_CHOICES = (
    ('onsight', 'On Sight'),
    ('flash', 'Flash'),
    ('complete', 'Complete'),
    ('project', 'project'),
)

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField()
    protection = models.CharField(max_length=8, choices=PROTECTION_CHOICES)
    boulder = models.ForeignKey('Boulder', null=True, on_delete=models.PROTECT, related_name='todos')
    route = models.ForeignKey('Route', null=True, on_delete=models.PROTECT, related_name='todos')

    class Meta:
        constraints = (
            models.CheckConstraint(
                check=(Q(boulder__isnull=True) ^ Q(route__isnull=True)),
                name='todo_boulder_xor_route',
            ),
        )
