# Licensed under the MIT License.

# Copyright (c) 2010 Senthil Palanisami

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Mathematical map data structures in python.

For more information: http://github.com/spenthil/pymathmap/
"""

__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)

import weakref

class OneToOneDict(dict):
    """ Effectively a key, key dictionary as apposed to traditional key, value dict

    >>> dict1 = OneToOneDict()
    >>> dict2 = OneToOneDict()
    >>> dict1.partner = dict2
    >>> assert(dict1 is dict2.partner)
    >>> assert(dict2 is dict1.partner)
    >>> dict1['one'] = '1'
    >>> dict2['2'] = '1'
    >>> dict1['one'] = 'wow'
    >>> assert(dict1 == dict((v,k) for k,v in dict2.items()))
    >>> dict1['one'] = '1'
    >>> assert(dict1 == dict((v,k) for k,v in dict2.items()))
    >>> dict1.update({'three': '3', 'four': '4'})
    >>> assert(dict1 == dict((v,k) for k,v in dict2.items()))
    >>> dict3 = OneToOneDict({'4':'four'})
    >>> assert(dict3.partner is None)
    >>> assert(dict3 == {'4':'four'})
    >>> dict1.partner = dict3
    >>> assert(dict1.partner is not dict2)
    >>> assert(dict2.partner is None)
    >>> assert(dict1.partner is dict3)
    >>> assert(dict3.partner is dict1)
    >>> dict1.setdefault('five', '5')
    >>> dict1['five']
    '5'
    >>> dict1.setdefault('five', '0')
    >>> dict1['five']
    '5'
    """
    def __init__(self, *args, **kwargs):
        self._partner = None
        return super(OneToOneDict, self).__init__(*args, **kwargs)

    def requires_partner(func):
        def _requires_partner(self, *args, **kwargs):
            if self.partner is None:
                raise AttributeError("Must set partner first.")
            return func(self, *args, **kwargs)
        return _requires_partner

    def get_partner(self):
        if self._partner is None:
            return None
        return self._partner()
    def set_partner(self, other):
        # Particular dictionary behavior: `id({}) == id({})` is `True`. Hence the `self != {}` check, otherwise wouldn't be able to set two empty `OneToOneDict`s as partners.
        if self != {} and other == self:
            raise AttributeError("Can't set partner to self.")
        if not hasattr(other, 'partner'):
            raise TypeError("The partner must allow having partners itself.")
        del self.partner
        self._partner = weakref.ref(other)
        self.partner._partner = weakref.ref(self)
        # need to make everything consistent
        # clobber self's entries if necessary, preserving other
        self.update(((v,k) for k,v in other.items()))
        other.update(((v,k) for k,v in self.items()))
    def del_partner(self):
        if self.partner is not None:
            self.partner._partner = None
            self._partner = None
    partner = property(get_partner, set_partner, del_partner)

    @requires_partner
    def __delitem__(self, key):
        super(OneToOneDict, self.partner).__delitem__(self[key])
        super(OneToOneDict, self).__delitem__(key)

    @requires_partner
    def __setitem__(self, key, value):
        # delete what this key used to point to if it already exists
        if self.has_key(key):
            super(OneToOneDict, self.partner).__delitem__(self[key])
        super(OneToOneDict, self.partner).__setitem__(value, key)
        super(OneToOneDict, self).__setitem__(key, value)

    @requires_partner
    def clear(self):
        super(OneToOneDict, self.partner).clear()
        super(OneToOneDict, self).clear()

    def copy(self):
        """ returns a copy with all the key, values but without a partner """
        result = OneToOneDict(data = OneToOneDict)

    @requires_partner
    def pop(self, key):
        result = super(OneToOneDict, self).pop(key)
        super(OneToOneDict, self.partner).__delitem__(result)
        return result

    @requires_partner
    def popitem(self):
        result = super(OneToOneDict, self).popitem()
        super(OneToOneDict, self.partner).__delitem__(result)
        return result

    @requires_partner
    def setdefault(self, key, value = None):
        super(OneToOneDict, self).setdefault(key, value)
        super(OneToOneDict, self.partner).__setitem__(value, key)

    @requires_partner
    def update(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError("update expected at most 1 arguments, got %d" % len(args))
        if len(args) == 1:
            if hasattr(args[0], 'keys'):
                for key in args[0]:
                    self[key] = args[0][key]
            else:
                for (key, value) in args[0]:
                    self[key] = value
        for key in kwargs:
            self[key] = kwargs[key]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
