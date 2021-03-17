from django.db import models
import os
# Create your models here.
from django.db.models import Model


class Department(models.Model):
    dep_name = models.CharField(max_length=30, blank=False, null=False)
    add_time = models.DateField(blank=False, null=False)


class Student(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    roll_number = models.CharField(max_length=20, unique=True, blank=False, null=False)
    std = models.IntegerField(default=10)
    percentage = models.DecimalField(max_digits=5, blank=False, null=False, decimal_places=2)
    state = models.CharField(max_length=50, blank=False, null=False)
    dep = models.ForeignKey(Department, on_delete=models.CASCADE)


class Artist(models.Model):
    name = models.CharField(max_length=25, null=False, blank=False)
    experience = models.IntegerField()
    language = models.CharField(max_length=20, null=False, blank=False)


class Movies(models.Model):
    movie_name = models.CharField(max_length=1000, null=False, blank=False)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    artist = models.ManyToManyField(Artist)


class FirstYearStudent(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    choices_var = [('male', 'Male'), ('female', 'FeMale'), ('others', 'Others')]
    gender = models.CharField(max_length=6, choices=choices_var, blank=False, default=None)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    xii_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    admission_date = models.DateField()


class Location(models.Model):
    state = models.CharField(max_length=75, blank=False)

    def __str__(self):
        return self.state

    def delete(self, using=None, keep_parents=False):
        # Get the list of employee belongs to this location
        emp_list = self.employee_set.all()
        for emp in emp_list:
            emp.delete()
        super().delete(using=None, keep_parents=False)


class Employee(models.Model):
    name = models.CharField(max_length=50, blank=False)
    ch = [
        ('male', 'Male'), ('female', 'FeMale'), ('others', 'Others')
    ]
    gender = models.CharField(max_length=6, choices=ch, blank=False, default=None)
    package = models.IntegerField(blank=True, help_text='in LPA')
    address = models.TextField(blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True)
    photo = models.FileField(upload_to='photos', blank=True, default='no_photo.jpg',
                             help_text="Supported format: jpeg/gif/png; max-size:50kb")

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.photo.name != 'no_photo.jpg':
            if os.path.isfile(self.photo.path):
                os.remove(self.photo.path)
        super(Employee, self).delete(*args, **kwargs)