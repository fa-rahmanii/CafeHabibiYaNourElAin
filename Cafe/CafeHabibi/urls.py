from django.urls import path, include
from .views import *# home_page, login_page

urlpatterns = [
    path('', home_page, name='home'),
    path('/login', login_page, name='login'),
    path('/signup', signup_page, name='signup'),
    # # path('books/', book_list, name="book-list"),
    # # path('books/', book_list_db, name="book-list"),
    # path('books/', books_html, name="book-list"),
    # path('books/add/', add_book, name="book-add"),
    # path('books/detail/<int:pk>', books_detail, name="book-detail"),
    # path('books/update/<int:pk>', edit_book, name="edit-book"),
    # path('books/delete/<int:pk>', book_delete, name="delete-book"),
    # path('authors', author_list, name="author-list"),
    # path('authors/add/', add_author, name="author-add"),
    # path('authors/details/<int:pk>', authors_details, name="author-details"),
    # path('authors/delete/<int:pk>', authors_delete, name="author-delete"),
    # path('publishers', publisher_list, name="publisher-list"),
    # path('publishers/add/', add_publisher, name="publisher-add"),
    # path('publishers/update/<int:pk>', publisher_update, name="publisher-update"),
    # path('publishers/details/<int:pk>', publisher_details, name="publisher-details"),
    # path('publishers/delete/<int:pk>', publisher_delete, name="publisher-delete"),

    # #     Authenticated paths
    # # path("user/books", LoanedBooksByUserListView.as_view(), name="user-books"),
    # path("user/books", user_books, name="user-books"),
    # path("register", register, name="register"),
    # path("borrow/<int:borrower_id>/<int:book_id>", borrow_a_book, name="borrow-a-book")
]
