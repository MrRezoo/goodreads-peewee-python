import json
from abc import ABC

from models import database, User, Book, Author, Shelf, BookShelf, BookAuthor


class AbstractImporter(ABC):
    filename = None
    model = None

    @classmethod
    def load(cls):
        with open(f'fixtures/{cls.filename}.json') as f:
            data = json.loads(f.read())

        instances = list()
        for instance in data:
            instances.append(cls.model.create(**instance))

        return instances


class UserImporter(AbstractImporter):
    filename = 'users'
    model = User


class AuthorImporter(AbstractImporter):
    filename = 'authors'
    model = Author


class BookImporter(AbstractImporter):
    filename = 'books'
    model = Book


class ShelfImporter(AbstractImporter):
    filename = None
    model = Shelf
    default_shelves = ['read', 'currently read', 'want to read']

    @classmethod
    def load(cls):
        instances = list()
        for user in User.select():
            for shelf in cls.default_shelves:
                instances.append(cls.model.create(user=user, name=shelf))
        return instances


class BookAuthorImporter(AbstractImporter):
    filename = 'books-authors'
    model = BookAuthor


class BookShelfImporter(AbstractImporter):
    filename = 'books-shelves'
    model = BookShelf
