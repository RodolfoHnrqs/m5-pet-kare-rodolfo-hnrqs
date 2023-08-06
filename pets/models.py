from django.db import models

class SexChoices(models.TextChoices):
    Female = "Female"
    Male = "Male"
    DEFAULT = "Not Informed"

class Pet(models.Model):
    name = models.CharField(max_length=50, null=False)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(max_length=20, choices=SexChoices.choices, default=SexChoices.DEFAULT)
    group = models.ForeignKey("groups.Group", on_delete=models.PROTECT, related_name="pets")
    traits = models.ManyToManyField("traits.Trait", related_name="pets")

    def __repr__(self):
        return f"<[{self.id}] - ({self.name})>"