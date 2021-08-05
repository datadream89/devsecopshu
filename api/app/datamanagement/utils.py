from more_itertools import one
from itertools import chain, repeat, islice

from typing import List, Optional, Set, Tuple, Union

def ensure_list(s: Optional[Union[str, List[str], Tuple[str], Set[str]]]) -> List[str]:
    # Ref: https://stackoverflow.com/a/56641168/
    return s if isinstance(s, list) else list(s) if isinstance(s, (tuple, set)) else [] if s is None else [s]

def pad_infinite(iterable, padding):
    return chain(iterable, repeat(padding))

def pad(iterable, size, padding=None):
    iterable = ensure_list(iterable)
    return islice(pad_infinite(iterable, padding), size)

def replaceNone(val, chr):
    if val is None:
        return chr
    return val

def replaceEscape(report):
    return report.replace('\n', '<br>')