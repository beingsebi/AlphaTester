from django.db import models
from django.urls import reverse

class Strategy(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name + " by " + self.user.username
    
    def get_absolute_url(self):
        return reverse("backtester:detail", kwargs={"pk": self.pk})