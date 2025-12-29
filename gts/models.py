from django.db import models

class University(models.Model):
    university_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="University Name")

    class Meta:
        db_table = 'university'
        verbose_name_plural = "Universities"

    def __str__(self):
        return self.name


class Institute(models.Model):
    institute_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Institute Name")
    university = models.ForeignKey(University, on_delete=models.CASCADE, db_column='university_id', verbose_name="Affiliated University")

    class Meta:
        db_table = 'institute'

    def __str__(self):
        return f"{self.name} ({self.university.name})"


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Author Name")

    class Meta:
        db_table = 'author'

    def __str__(self):
        return self.name  


class Supervisor(models.Model):
    supervisor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Supervisor Name")

    class Meta:
        db_table = 'supervisor'

    def __str__(self):
        return self.name


class ThesisType(models.Model):
    type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Thesis Type")

    class Meta:
        db_table = 'thesis_type'

    def __str__(self):
        return self.name


class Language(models.Model):
    language_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Language")

    class Meta:
        db_table = 'language'

    def __str__(self):
        return self.name


class SubjectTopic(models.Model):
    topic_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Topic")

    class Meta:
        db_table = 'subject_topic'

    def __str__(self):
        return self.name


class Keyword(models.Model):
    keyword_id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=100, verbose_name="Keyword")

    class Meta:
        db_table = 'keyword'

    def __str__(self):
        return self.word


class Thesis(models.Model):
    thesis_no = models.IntegerField(primary_key=True, verbose_name="Thesis No")
    title = models.CharField(max_length=500, verbose_name="Title")
    abstract = models.TextField(verbose_name="Abstract")
    year = models.IntegerField(verbose_name="Year")
    num_pages = models.IntegerField(verbose_name="Number of Pages")
    submission_date = models.DateField(verbose_name="Submission Date")

    author = models.ForeignKey(Author, on_delete=models.CASCADE, db_column='author_id', verbose_name="Author")
    type = models.ForeignKey(ThesisType, on_delete=models.CASCADE, db_column='type_id', verbose_name="Thesis Type")
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, db_column='institute_id', verbose_name="Institute")
    language = models.ForeignKey(Language, on_delete=models.CASCADE, db_column='language_id', verbose_name="Language")
    
    
    supervisor = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervised_theses', verbose_name="Supervisor")
    
    co_supervisor = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, null=True, blank=True,)


    topics = models.ManyToManyField(SubjectTopic, verbose_name="Topics", blank=True)
    keywords = models.ManyToManyField(Keyword, blank=True, verbose_name="Keywords")