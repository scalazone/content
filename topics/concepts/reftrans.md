# Referential Transparency

In an earlier example, we saw how,
```scala
def second: String =
  println("Accessed the second method.")

  "two"
```
would execute the `println` command, and output a line to the console, every single time the method `second` is
referenced.

It may be surprising that an identifier which looks as innocuous as `second` would execute some code that could
cause changes to occur elsewhere—on the console—because it looks just like a reference to a field would. So it
is common-practice to write such a definition as,
```scala
def second(): String =
  println("Accessed the second method.")

  "two"
```
and correspondingly we must thereafter write these empty parentheses for every usage of the method, `second`,
like so:
```scala
println("The result of ${second()} plus ${second()} is four.")
```

In general, methods defined with `def` 

Referential transparency

The property that 

Identifiers may contain letters (both upper-case and lower-case), numbers and underscores, as long as the first
character is not a number. Spaces are permitted, so conventionally, if an identifier contains more than one
word, the spaces are removed, and every word from the second word onwards is capitalized to set it apart from
the previous word. This is known as medial capitalization, or more commonly, _camel-case_, because the capital
letters amongst the miniscules looks like the humps of a camel.

The first letter of the first word may or may not be capitalized, depending on the nature of the identifier:
this is not strict, but values and methods usually begin with a lower-case letter, while types and singleton
objects begin with an upper-case letter. Regardless of the first letter, camel-case is used for the second word,
onwards.

Here are some examples:
- `first`
- `Element`
- `nextItem`
- `lastLetterInWord`
- `GraphNode`

Identifiers may also be _symbolic_, meaning that they consist entirely of symbolic characters, such as `+`, `~`,
`^` or `*`. Certain symbolic characters which have a special meaning in Scala are forbidden in identifier names.
These include various brackets (`(`, `)`, `{`, `}`, `[` and `]`), quotes (`'`, `` ` `` and `"`) and other
characters which would significantly complicate parsing source code if they were to be permitted (`,`, `.`, `#`,
`@` and `=`), though `#`, `@` and `=` may still be used as long as they are not the first character of an
identifier.

Underscores (`_`) may also be used in identifier names, though their use is uncommon. Nevertheless, they do
allow symbolic characters to be combined with alphanumeric characters in an identifier name: alphanumeric
characters may only be adjacent to other alphanumeric characters, and symbolic characters may be adjacent to
other symbols, and an underscore may be considered _both_ alphanumeric and symbolic.

To avoid ambiguity, identifier names cannot be the same as many keywords like `class`, while others, such as
`inline`, are considered _soft keywords_ which allows them to be parsed unambiguously as keywords or
identifiers.

However, for all that complexity, such identifiers are not particularly useful. But the fact that a symbolic
character cannot appear adjacent to an alphanumeric character makes it permissible to write some expressions,
such as `a*b` or `value/3.2`, unambiguously without spaces between the identifiers: `a`, `*`, `b`; `value` and
`/` because, the combination of letters and symbols in the same identifier, for example, `a*b`, would be
invalid.

Very occasionally, we may want to define or use an identifier name which would be forbidden by one of these
rules. This is permitted, with one compromise: it must be enclosed within backticks (`` ` ``). For example,
- `` `#` ``
- `` `object` ``
- `` `Hello, World!` ``
- `` `()` ``
