from django.db import models


class University(models.Model):
    university_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Üniversite Adı")

    class Meta:
        db_table = 'university'
        verbose_name_plural = "Universities"

    def __str__(self):
        return self.name


class Institute(models.Model):
    institute_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Enstitü Adı")
   
    university = models.ForeignKey(University, on_delete=models.CASCADE, db_column='university_id', verbose_name="Bağlı Olduğu Üniversite")

    class Meta:
        db_table = 'institute'

    def __str__(self):
        return f"{self.name} ({self.university.name})"

# --- MEVCUT: Yazar Modeli ---
class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Yazar Adı Soyadı")

    class Meta:
        db_table = 'author'

    def __str__(self):
        return self.name  


class Supervisor(models.Model):
    supervisor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Danışman Adı Soyadı")

    class Meta:
        db_table = 'supervisor'

    def __str__(self):
        return self.name


class ThesisType(models.Model):
    type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Tez Türü")

    class Meta:
        db_table = 'thesis_type'

    def __str__(self):
        return self.name


class Language(models.Model):
    language_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Dil")

    class Meta:
        db_table = 'language'

    def __str__(self):
        return self.name

class SubjectTopic(models.Model):
    topic_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Konu Başlığı")

    class Meta:
        db_table = 'subject_topic'

    def __str__(self):
        return self.name


class Keyword(models.Model):
    keyword_id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=100, verbose_name="Anahtar Kelime")

    class Meta:
        db_table = 'keyword'

    def __str__(self):
        return self.word


class Thesis(models.Model):
    thesis_no = models.IntegerField(primary_key=True, verbose_name="Tez Numarası")
    title = models.CharField(max_length=500, verbose_name="Başlık")
    abstract = models.TextField(verbose_name="Özet")
    year = models.IntegerField(verbose_name="Yıl")
    num_pages = models.IntegerField(verbose_name="Sayfa Sayısı")
    submission_date = models.DateField(verbose_name="Teslim Tarihi")

    
    author = models.ForeignKey(Author, on_delete=models.CASCADE, db_column='author_id', verbose_name="Yazar")
    type = models.ForeignKey(ThesisType, on_delete=models.CASCADE, db_column='type_id', verbose_name="Tez Türü")
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, db_column='institute_id', verbose_name="Enstitü")
    language = models.ForeignKey(Language, on_delete=models.CASCADE, db_column='language_id', verbose_name="Dil")
    
    
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, related_name='supervised_theses', verbose_name="Danışman")
    co_supervisor = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, null=True, blank=True, related_name='co_supervised_theses', verbose_name="Eş Danışman")
    
    topics = models.ManyToManyField(SubjectTopic, verbose_name="Konu Başlıkları")
    keywords = models.ManyToManyField(Keyword, blank=True, verbose_name="Anahtar Kelimeler")

    class Meta:
        db_table = 'thesis'
        verbose_name_plural = "Theses"

    def __str__(self):
        return f"{self.thesis_no} - {self.title}"
