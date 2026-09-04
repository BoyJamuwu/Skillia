from django.db import models


class Teacher(models.Model):
    full_name = models.CharField(max_length=200)
    headline = models.CharField(max_length=200, blank=True)
    specialty = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    photo_url = models.URLField(max_length=500, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    years_experience = models.PositiveIntegerField(default=0)
    email = models.EmailField(blank=True)
    linkedin_url = models.URLField(max_length=500, blank=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name

    @property
    def initials(self):
        """Iniciales para el avatar de respaldo cuando no hay foto cargada."""
        parts = self.full_name.split()
        return "".join(part[0] for part in parts[:2]).upper()
