from django.contrib import admin

from .models import MyModelName, Genre, Book, BookInstance, Author


# Определите класс администратора:
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


# Зарегистрируйте классы администратора для Book с помощью декоратора
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


# Зарегистрируйте классы администратора для BookInstance с помощью декоратора:
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

    
# Register your models here:
admin.site.register(MyModelName)
admin.site.register(Genre)
# admin.site.register(Book)
# admin.site.register(BookInstance)
# Зарегистрируйте класс администратора со связанной моделью:
admin.site.register(Author, AuthorAdmin)
