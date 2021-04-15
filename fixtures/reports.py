from models import User, Shelf, Book


def show_users():
    users = User.select()

    for user in users:
        # shelves = Shelf.select().where(Shelf.user == user).count()
        shelves_count = user.shelves.count()
        shelf = ', '.join([shelf.name for shelf in user.shelves])
        print(user.username, '\t', shelves_count, shelf)


def show_books():
    books = Book.select()
    for book in books:
        authors = ', '.join(
            [book_author.author.name for book_author in book.authors])
        print(f"{book.name}({book.isbn})\t {authors}")


def show_user_data(username='reza'):
    pass