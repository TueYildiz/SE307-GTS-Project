from django.db import models


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
   
    name = models.CharField(max_length=255, verbose_name="Yazar Adı Soyadı")

    class Meta:
        db_table = 'author'
       

    def __str__(self):
        return self.name  



class ThesisType(models.Model):
    type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Tez Türü")

    class Meta:
        db_table = 'thesis_type'

    def __str__(self):
        return self.name


class Institute(models.Model):
    institute_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Üniversite/Enstitü Adı")

    class Meta:
        db_table = 'institute'

    def __str__(self):
        return self.name



class Language(models.Model):
    language_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Dil")

    class Meta:
        db_table = 'language'

    def __str__(self):
        return self.name



class Thesis(models.Model):
    thesis_no = models.IntegerField(primary_key=True, verbose_name="Tez Numarası")
    title = models.CharField(max_length=500, verbose_name="Başlık")
    abstract = models.TextField(verbose_name="Özet")
    year = models.IntegerField(verbose_name="Yıl")
    num_pages = models.IntegerField(verbose_name="Sayfa Sayısı")
    submission_date = models.DateField(verbose_name="Teslim Tarihi")

    
    author = models.ForeignKey(Author, on_delete=models.CASCADE, db_column='author_id', verbose_name="Yazar")
    type = models.ForeignKey(ThesisType, on_delete=models.CASCADE, db_column='type_id', verbose_name="Tez Türü")
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, db_column='institute_id', verbose_name="Üniversite")
    language = models.ForeignKey(Language, on_delete=models.CASCADE, db_column='language_id', verbose_name="Dil")

    class Meta:
        db_table = 'thesis'

    def __str__(self):
        return f"{self.thesis_no} - {self.title}"