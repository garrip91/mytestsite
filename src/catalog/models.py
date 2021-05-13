from django.db import models

from django.urls import reverse

import uuid


# Create your models here:
class MyModelName(models.Model):
    """
    Типичный класс, определяющий модель, производный от класса Model.
    """
    
    # Поля:
    my_field_name = models.CharField(max_length=20, help_text="Введите документацию поля", verbose_name = "Название")
    ...
    
    # Метаданные:
    class Meta:
        verbose_name_plural = "Названия"
        ordering = ["-my_field_name"]
        
    # Методы:
    def get_absolute_url(self):
        """
        Возвращает URL-адрес для доступа к конкретному экземпляру MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.id)])
        
    def __str__(self):
        """
        Строка для представления объекта MyModelName (на сайте администратора и т. Д.)
        """
        return self.my_field_name
        
        
class Genre(models.Model):
    """
    Модель, представляющая жанр книги (например, научная фантастика, научно-популярная литература).
    """
    name = models.CharField(max_length=200, help_text="Укажите жанр книги (например, научная фантастика, французская поэзия и т. Д.)", verbose_name="Жанр")
    
    class Meta:
        verbose_name_plural = "Жанры"
    
    def __str__(self):
        """
        Строка для представления объекта модели (на сайте администратора и т. Д.)
        """
        return self.name
        
        
class Book(models.Model):
    """
    Модель, представляющая книгу (но не конкретный экземпляр книги).
    """
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Используется внешний ключ, потому что у книги может быть только один автор, но у авторов может быть несколько книг.
    # Автор как строка, а не объект, потому что он еще не был объявлен в файле.
    summary = models.TextField(max_length=1000, help_text="Введите краткое описание книги", verbose_name="Описание")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр для этой книги", verbose_name="Жанр")
    # ManyToManyField используется, потому что жанр может содержать много книг. Книги могут охватывать многие жанры.
    # Класс жанра уже определен, поэтому мы можем указать объект выше.
    
    class Meta:
        verbose_name_plural = "Книги"
        ordering = ['title']
    
    def __str__(self):
        """
        Строка для представления объекта модели.
        """
        return self.title
        
    def get_absolute_url(self):
        """
        Возвращает URL-адрес для доступа к конкретному экземпляру книги.
        """
        return reverse('book-detail', args=[str(self.id)])
        
    def display_genre(self):
        """
        Создаёт строку для жанра. Это необходимо для отображения жанра в админке.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description = 'Genre'
        
        
class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный идентификатор этой конкретной книги во всей библиотеке")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200, verbose_name="Отпечаток")
    due_back = models.DateField(null=True, blank=True, verbose_name="Дата возврата")
    
    LOAN_STATUS = (
        ('m', 'Обслуживание'),
        ('o', 'Взаймы'),
        ('a', 'Имеется в наличии'),
        ('r', 'Обратный'),
    )
    
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Доступность книги', verbose_name="Статус")
    
    class Meta:
        verbose_name_plural = "экземпляры книг"
        ordering = ["due_back"]
        
    def __str__(self):
        """
        Строка для представления объекта модели
        """
        return '{0} ({1})'.format (self.id, self.book.title)
        
        
class Author(models.Model):
    """
    Модель, представляющая автора.
    """
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    date_of_death = models.DateField('Died', null=True, blank=True)
    
    def get_absolute_url(self):
        """
        Возвращает URL-адрес для доступа к конкретному экземпляру автора.
        """
        return reverse('author-detail', args=[str(self.id)])
        
    class Meta:
        verbose_name_plural = "Авторы"
        ordering = ['last_name']
        
    def __str__(self):
        """
        Строка для представления объекта модели.
        """
        return '{0} ({1})'.format (self.last_name, self.first_name)
        