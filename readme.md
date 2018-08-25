# Multiple string pattern matcher

This module contains a class that allows you to quickly search a text string for multiple chosen patterns. The search method utilizes the [Aho-Corasick algorithm](https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm).

## Usage instructions

Import the matcher class from the module, and instantiate it

```python
from string_matcher import matcher
m = matcher()
```

Call the matcher.search() method, which takes a string of text to search and a list of string patterns (case sensitive) to search for. The return value is a list of 2-tuples, in each tuple the first element is the matched pattern, and the second is the text index where the match was found.

```python
m.search("Text to search", ["Text", "to", "search"])
# returns [("Text", 0), ("to", 5), ("search", 8)]
```

Alternatively, if you know beforehand which patterns you will search for, you can use the matcher.load_patterns method to preload the patterns. Then, you can call search and only pass in the text to search.

```python
# preload the patterns
m.load_patterns(["Text", "to", "search"])
# At a later point in time, search the text
m.search("Text to search")
# returns [("Text", 0), ("to", 5), ("search", 8)]
```