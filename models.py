from django.db import models

# Create your models here.
from django.db import models


class Thesis(models.Model):
    thesis_no = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=500)
    abstract = models.TextField()
    author = models.ForeignKey(
        'Author',
        on_delete=models.CASCADE,
        db_column='author_id'
    )
    year = models.IntegerField()
    type = models.ForeignKey(
        'ThesisType',
        on_delete=models.CASCADE,
        db_column='type_id'
    )
    institute = models.ForeignKey(
        'Institute',
        on_delete=models.CASCADE,
        db_column='institute_id'
    )
    num_pages = models.IntegerField()
    language = models.ForeignKey(
        'Language',
        on_delete=models.CASCADE,
        db_column='language_id'
    )
    submission_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'thesis'

    def __str__(self):
        return f"{self.thesis_no} - {self.title}"
class Author(models.Model):
    author_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'author'

    def __str__(self):
        return str(self.author_id)


class ThesisType(models.Model):
    type_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'thesis_type'

    def __str__(self):
        return str(self.type_id)


class Institute(models.Model):
    institute_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'institute'

    def __str__(self):
        return str(self.institute_id)


class Language(models.Model):
    language_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'language'

    def __str__(self):
        return str(self.language_id)
