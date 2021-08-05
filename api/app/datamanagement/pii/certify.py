from datamanagement.pii.commonregex import CommonRegex, date, price, time
import functools
from functools import partial

import re

def logme(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        print(f.__name__)
        return f(*args, **kwargs)
    return wrapped

a=['sd', 'ds','a1$', '^re', '#', ' 09 march', '$ 950', 'Ç', '1989 Jan', '9:40']
m=['isalnum', 'price_check', 'date_check', 'time_check']

def regex_match(re_pattern):
    return re_pattern.match()

def date_check(string):
    return date.search(string) != None

def price_check(string):
    return price.search(string) != None

def time_check(string):
    return price.search(string) != None

no_spec_char=[]
for i in range(len(a)):
    no_spec_char.append(eval(m[3])(a[i]))

print(no_spec_char)
