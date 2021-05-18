from django.shortcuts import render

from django.http import HttpResponse

from .models import Book, BookInstance, Author, Genre

from django.views import generic


# Create your views here:
def index(request):
    """
    Функция отображения для домашней страницы сайта
    """
    # Генерация "количеств" некоторых главных объектов:
    num_books = Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Доступные книги (статус = 'a'):
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count() # Метод 'all()' применён по умолчанию
    num_genres = Genre.objects.count()
    
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context:
    return render(request, 'index.html', context={
                                            'num_books': num_books,
                                            'num_instances': num_instances,
                                            'num_instances_available': num_instances_available,
                                            'num_authors': num_authors,
                                            'num_genres': num_genres
                                        },
    )
    
    
class BookListView(generic.ListView):
    model = Book
    
    def get_queryset(self):
        return Book.objects.filter(title__icontains='war')[:5] # Получить 5 книг, содержащих 'war' в заголовке
        
    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста:
        context = super(BookListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением:
        context['some_data'] = 'This is just some data'
        return context
        
        
class BookDetailView(generic.DetailView):
    model = Book
    
    def book_detail_view(request, pk):
        try:
            book_id=Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404("Book does not exist")
            
        # book_id=get_object_or_404(Book, pk=pk)
        
        return render(
            request,
            'catalog/book_detail.html',
            context={'book: book_id',}
        )