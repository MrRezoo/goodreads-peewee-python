from peewee import fn

from fixtures.reports import show_users, show_books
from importer import UserImporter, BookImporter, AuthorImporter, \
    BookShelfImporter, BookAuthorImporter, ShelfImporter
from models import database, User, Book, Author, BookShelf, BookAuthor, \
    BookTranslator, UserAuthorRelation, UserRelation, Shelf


def load_data():
    importer_classes = [UserImporter, BookImporter, AuthorImporter,
                        BookAuthorImporter, ShelfImporter, BookShelfImporter, ]

    for _class in importer_classes:
        print(_class.load())


def create_table():
    database.create_tables([User, Book, Author, Shelf, BookShelf, BookAuthor,
                            BookTranslator, UserAuthorRelation, UserRelation])


def show_data():
    show_users()
    print("==" * 31)
    show_books()


def show_user_data(username='reza', password='654321'):
    user = User.authenticate(username, password='654321')
    if user is None:
        print("user not found")
        return
    print(user.username)
    print("book shelves:")
    for shelf in user.shelves:
        print(shelf.name, shelf.book_shelves.count())

    print("book:")
    for book_shelf_instance in user.book_shelves:
        print(book_shelf_instance.book.name)
    book = Book.get_by_id(3)
    # book = Book.get_or_none(Book.id == 3)
    # read_shelf = user.shelves.where(Shelf.name == Shelf.READ)
    # new_book_shelf = BookShelf.create(user=user, book=book, shelf=read_shelf,
    #                                   rate=6,content='good')


def show_book_rates():
    query = BookShelf.select(
        BookShelf.book,
        fn.AVG(BookShelf.rate).alias('rates_avg'),  # wrong data
        fn.SUM(BookShelf.rate).alias('rates_sum'),
        fn.COUNT(BookShelf.rate).alias('rates_count'),
    ).group_by(BookShelf.book)

    for q in query:
        print(q.book.id, q.rates_avg, q.rates_sum / q.rates_count)


def show_book_shelves():
    query = BookShelf.select(
        BookShelf.user,
        BookShelf.shelf,
        fn.COUNT(BookShelf.book).alias('books_count')
    ).group_by(BookShelf.shelf).order_by(fn.COUNT(BookShelf.book))

    for q in query:
        print(q.user.username, q.shelf.name, q.books_count)


def show_all_book_shelf():
    query = BookShelf.select()  # hit 1
    for q in query:
        print(q.rate)  # no hit
        print(q.user.username)  # hit 2
        print(q.shelf.name)  # hit 3
        print(q.book.name)  # hit 4
        print('#' * 20)


def show_all_book_shelf_optimize():
    query = BookShelf.select().join(User) \
        .switch(BookShelf).join(Book) \
        .switch(BookShelf).join(Shelf)  # hit 1
    for q in query:
        print(q.rate)  # no hit
        print(q.user.username)  # not hit
        print(q.shelf.name)  # not hit
        print(q.book.name)  # no hit
        print('#' * 20)


if __name__ == '__main__':
    print("==" * 10, " We Can Do It . . . ", "==" * 10)
    # create_table()
    # load_data()
    # show_data()
    # show_user_data()
    # show_book_rates()
    # show_book_shelves()
    # show_all_book_shelf()
    # show_all_book_shelf_optimize()
