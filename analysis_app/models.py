from django.db import models

# Models are minimal since data is loaded from CSV.
# Extend here if you want to persist user bookmarks, etc.

class SearchLog(models.Model):
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    results_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.query} ({self.timestamp})"
