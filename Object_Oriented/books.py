#!/usr/bin/env python

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        
    def __str__(self):
        return '<Book: {} by {}>'.format(self.title, self.author)

book = Book(title='All the light', author='some person')

print(book)

raise NotImplementedError