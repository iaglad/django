import sys

class PageNotAnInteger(Exception):
    pass
class EmptyPage(Exception):
    pass

class Paginator:
    def __init__(self, list, c):
        self.list = list
        self.count_on_page = c
        self.total = self.list.count()
        self.num_pages = round((self.total / c) + 0.5)
        self.has_other_pages = self.num_pages > 1
    
    def page(self, n):
        try:
            n = int(n)
        except (ValueError, TypeError):
            raise PageNotAnInteger
            return
        if n < 1 or n > self.num_pages:
            raise EmptyPage
            return
        j = (n-1)*self.count_on_page
        k = (n-1)*self.count_on_page + self.count_on_page
        print(sys.stderr, "!@################      Paginator.Page    n= ", n, "  j= ", j, "  k=", k)
        pg = Page(self.list[j:k], n, self)
        #print(sys.stderr, "!@################      Paginator.Page    pg   ", pg)
        return pg

    @property
    def page_range(self):
        return range(1, self.num_pages + 1)

class Page:
    def __init__(self, list, number, paginator):
        self.list = list
        self.number = number
        self.paginator = paginator
    
    @property
    def has_next(self):
        return self.paginator.num_pages > self.number
    
    @property
    def has_previous(self):
        return self.number > 1
    
    @property
    def has_other_pages(self):
        return self.has_next or self.has_previous

    