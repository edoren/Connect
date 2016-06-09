from threading import Lock

__all__ = ["SafeList", "SafeDict"]


class SafeMutableContainer(object):

    def __init__(self, *args, **kwargs):
        super(SafeMutableContainer, self).__init__(*args, **kwargs)
        self._lock = Lock()

    def __setitem__(self, key, value):
        with self._lock:
            return super(SafeMutableContainer, self).__setitem__(key, value)

    def __delitem__(self, key):
        with self._lock:
            return super(SafeMutableContainer, self).__delitem__(key)

    def __contains__(self, item):
        with self._lock:
            return super(SafeMutableContainer, self).__contains__(item)

    def __len__(self):
        with self._lock:
            return super(SafeMutableContainer, self).__len__()


class SafeList(SafeMutableContainer, list):

    def append(self, elem):
        with self._lock:
            return super(SafeList, self).append(elem)

    def extend(self, L):
        with self._lock:
            return super(SafeList, self).extend(L)

    def insert(self, i, value):
        with self._lock:
            return super(SafeList, self).insert(i, value)

    def remove(self, x):
        with self._lock:
            return super(SafeList, self).remove(x)

    def pop(self, i=-1):
        with self._lock:
            return super(SafeList, self).pop(i)

    def clear(self):
        with self._lock:
            return super(SafeList, self).clear()

    def sort(self, key=None, reverse=False):
        with self._lock:
            return super(SafeList, self).sort(key, reverse)

    def reverse(self):
        with self._lock:
            return super(SafeList, self).reverse()


class SafeDict(SafeMutableContainer, dict):

    def clear(self):
        with self._lock:
            return super(SafeDict, self).clear()

    def get(self, *args, **kwargs):
        with self._lock:
            return super(SafeDict, self).get(*args, **kwargs)

    def pop(self, *args, **kwargs):
        with self._lock:
            return super(SafeDict, self).pop(*args, **kwargs)

    def popitem(self):
        with self._lock:
            return super(SafeDict, self).popitem()

    def setdefault(self, *args, **kwargs):
        with self._lock:
            return super(SafeDict, self).setdefault(*args, **kwargs)

    def update(self, *args, **kwargs):
        with self._lock:
            return super(SafeDict, self).update(*args, **kwargs)
