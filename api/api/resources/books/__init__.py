# -*- coding: utf-8 -*-
from .books import *

resources = [
    ('books', BookCollection, "books.lists"),
    ('books/<int:id>', BookResource, "books.detail"),

]
