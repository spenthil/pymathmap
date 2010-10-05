py**m**ath**m**ap implements [mathematical map](http://en.wikipedia.org/wiki/Map_(mathematics\)) data structures in Python.

The latest documentation can be found at http://github.com/spenthil/pymathmap/

# Todo

In rough order of priority:

1. make OneToOneDict pickleable (guessing it isn't)
1. `OneToMany` map
1. `ManyToMany` map
1. `OneToOne` that implements `collections.MutableMapping` and doesn't have to be surjective. This is different than `OneToOneDict` which instead inherits from `dict`.
1. make everything thread safe.

# License

Licensed under the MIT License.

Copyright (c) 2010 Senthil Palanisami

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
