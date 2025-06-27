from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pages = models.IntegerField()
    published_date = models.DateField()

    def __str__(self):
        return (f"""{{'
                f"title" : "{self.title}",
                f"author" : "{self.author}",
                f"pages" : "{self.pages}",
                f"published_date" : "{self.published_date}",
                }}""")

class Chore(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    due_date = models.DateField()
    done = models.BooleanField()

    def __str__(self):
        return (f"""{{'
                f"title" : "{self.title}",
                f"description" : "{self.description}",
                f"due_date" : "{self.due_date}",
                f"done" : "{self.done}",
                }}""")





# Create your models here.
