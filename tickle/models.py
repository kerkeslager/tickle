from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

class QQ:
    def __xor__(self, other):
        return (self & (~other)) | ((~self) & other)

Q.__bases__ += (QQ, )

BOULDER_DIFFICULTY_CHOICES = (
    ('v0', 'v0'),
    ('v1', 'v1'),
    ('v2', 'v2'),
    ('v3', 'v3'),
    ('v4', 'v4'),
    ('v5', 'v5'),
    ('v6', 'v6'),
    ('v7', 'v7'),
    ('v8', 'v8'),
    ('v9', 'v9'),
    ('v10', 'v10'),
    ('v11', 'v11'),
    ('v12', 'v12'),
    ('v13', 'v13'),
    ('v14', 'v14'),
    ('v15', 'v15'),
    ('v16', 'v16'),
)

class Area(models.Model):
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=64)
    notes = models.TextField(blank=True)

    def __str__(self):
        if self.parent is None:
            return self.name

        return '{} > {}'.format(self.parent, self.name)

class Boulder(models.Model):
    area = models.ForeignKey('Area', on_delete=models.PROTECT)
    name = models.CharField(max_length=64)
    difficulty = models.CharField(
        choices=BOULDER_DIFFICULTY_CHOICES,
        max_length=8,
    )
    mountainproject = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.difficulty)

PITCH_DIFFICULTY_CHOICES = (
    ('3', '3'),
    ('4', '4'),
    ('5.0', '5.0'),
    ('5.1', '5.1'),
    ('5.2', '5.2'),
    ('5.3', '5.3'),
    ('5.4', '5.4'),
    ('5.5', '5.5'),
    ('5.6', '5.6'),
    ('5.7', '5.7'),
    ('5.7+', '5.7+'),
    ('5.8', '5.8'),
    ('5.8+', '5.8+'),
    ('5.9', '5.9'),
    ('5.9+', '5.9+'),
    ('5.10a', '5.10a'),
    ('5.10b', '5.10b'),
    ('5.10c', '5.10c'),
    ('5.10d', '5.10d'),
    ('5.11a', '5.11a'),
    ('5.11b', '5.11b'),
    ('5.11c', '5.11c'),
    ('5.11d', '5.11d'),
    ('5.12a', '5.12a'),
    ('5.12b', '5.12b'),
    ('5.12c', '5.12c'),
    ('5.12d', '5.12d'),
    ('5.13a', '5.13a'),
    ('5.13b', '5.13b'),
    ('5.13c', '5.13c'),
    ('5.13d', '5.13d'),
    ('5.14a', '5.14a'),
    ('5.14b', '5.14b'),
    ('5.14c', '5.14c'),
    ('5.14d', '5.14d'),
    ('5.15a', '5.15a'),
    ('5.15b', '5.15b'),
    ('5.15c', '5.15c'),
    ('5.15d', '5.15d'),
)

class Pitch(models.Model):
    order = models.PositiveSmallIntegerField()
    route = models.ForeignKey(
        'Route',
        on_delete=models.CASCADE,
        related_name='pitches',
    )
    difficulty = models.CharField(
        choices=PITCH_DIFFICULTY_CHOICES,
        max_length=8,
    )
    name = models.CharField(blank=True, max_length=32)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return 'P{} ({})'.format(self.order, self.difficulty)

PROTECTION_STYLE_CHOICES = (
    ('sport', 'Sport'),
    ('toprope', 'Top Rope'),
    ('trad', 'Trad'),
)

class Route(models.Model):
    area = models.ForeignKey('Area', on_delete=models.PROTECT)
    name = models.CharField(max_length=64)
    protection_style = models.CharField(max_length=8, choices=PROTECTION_STYLE_CHOICES)
    mountainproject = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    # TODO Write test for this
    @property
    def difficulty(self):
        return self.pitches.order_by('-difficulty').first().difficulty

    def __str__(self):
        return '{} ({})'.format(self.name, self.difficulty)

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
    date = models.DateField()
    notes = models.TextField(blank=True)
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

        ordering = ('date',)

STYLE_CHOICES = (
    ('onsight', 'On Sight'),
    ('flash', 'Flash'),
    ('project', 'Project'),
    ('other', 'Other'),
)

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    protection = models.CharField(max_length=8, choices=PROTECTION_CHOICES)
    boulder = models.ForeignKey('Boulder', null=True, on_delete=models.PROTECT, related_name='todos')
    route = models.ForeignKey('Route', null=True, on_delete=models.PROTECT, related_name='todos')
    style = models.CharField(max_length=8, choices=STYLE_CHOICES)

    class Meta:
        constraints = (
            models.CheckConstraint(
                check=(Q(boulder__isnull=True) ^ Q(route__isnull=True)),
                name='todo_boulder_xor_route',
            ),
        )

        ordering = ('route__name',)

    def __str__(self):
        if self.boulder:
            climb = self.boulder
        elif self.route:
            climb = self.route
        else:
            raise Exception()

        return '{} {}'.format(self.style, climb)
