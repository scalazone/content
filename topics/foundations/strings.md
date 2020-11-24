
In the programs we write, we will inevitably need to work with text, whether it's for other humans to read, or
as a carrier for computer-readable formats like JSON or XML. These sequences of characters are called _strings_,
and in Scala, they are objects with the type `String`.

There is special syntax for creating new `String` instances. The usual way to write a string in code is to place
the text between two quote characters (`"`), for example,
```scala
"The quick brown fox jumps over the lazy dog."
```

This is called a _string literal_ because we have written the text content of the string _literally_, rather
than as a reference to a string object which originates somewhere else; it's like the string is _embedded_ in
our code.

Almost any character can be included in a string literal when we write it using the style above, and we are
certainly not restricted only to the "English" alphabet, or to the widely-used ASCII character set, which
defines just 96 different characters. So this,
```scala
"სწრაფი ყავისფერი მელა ხტება ზარმაც ძაღლს."
```
is a valid Scala string literal, and so is this:
```scala
"速い茶色のキツネは怠惰な犬を飛び越えます。"
```

Strings are composed of sequences of _characters_: letters in a variety of different international alphabets,
numbers, and a huge selection of symbols and emoji characters for almost every purpose imaginable. Each
character is an atomic _glyph_, which means they can be counted, and accessed within a string using an integer
index, for example, given,
```scala
val str = "Hello, World!"
```
the expression `str.length` evaluates to `13`, and `str(7)` is the character, `W`.

## Unicode

The JVM's abstraction of a string hides its internal representation from us, but it is nevertheless represented
in memory as a sequence of _Unicode codepoints_, that is, characters in the set of characters that are
representable in the _Unicode standard_.

Unicode is a set of standards which cover, primarily, a one-to-one mapping between integers and glyphs, and
secondarily, a few ways of representing sequences of those integers as binary data. The latter is known as the
_character encoding_ and will be covered in a later lesson: the JVM's representation of strings as sequences of
characters means we do not need to concern ourselves with the details of their binary representation in memory.

Scala uses the type `Char` to represents a single Unicode character. It can be readily converted to its Unicode
codepoint as an integer, and in version 13.0 of the Unicode standard (the latest version at the time of writing)
there are 143859 valid codepoints.

## Escaping

While every codepoint represents _something_ in the Unicode standard, not every font will provide a visible
_glyph_ (the actual shape of the character) for that codepoint. String literals can still hold these values, but
it may be more convenient to write them as explicit references to Unicode codepoints. We can do this by writing
the character sequence `\uxxxx` in the string, where each `x` is a hexadecimal digit.

For example, the Greek letter, `π`, can be written inside a string literal as, `\u03c0`, because the
hexadecimal number `03c0` (which is equivalent to the decimal number `960`) corresponds to the Unicode codepoint
for `π`. We could represent the formula for the circumference of a circle as a string with either `"2πr"` or
`"2\u03c0r"`.

Note that the Unicode escape sequence always contains four hexadecimal digits, and as soon as the Scala parser
reads `\u` it knows to consume the next four characters as the Unicode codepoint.

There are a few characters which need to be treated specially to be included in a string literal, and can only
be included if they are _escaped_: written in a special way so that they can be interpreted as intended.

The quote character, `"`, if it were to appear in the middle of a string literal, would terminate the string, so
to indicate that to the Scala compiler, we need to write every `"` symbol preceded with a backslash, `\`. For
example,
```scala
"The \"quote\" character."
```

## Character literals

Unicode can also represent special whitespace characters. In Scala, we write a newline character is as `\n`, a
carriage return as `\r`, a form feed as `\f`, a tab as `\t` and a backspace character as `\b`. While it's rare
(and potentially confusing!) to ever need to write a backspace character, newlines occur much more frequently.

And because the `\` character has a special meaning inside strings as the escape character, it must itself be
escaped. So to represent the string `\` we must write it twice, as `"\\"`. This can sometimes make it awkward to
write certain strings, such as a path on Windows, for example, `C:\Program Files\`. This would need to be
written in Scala code as, `"C:\\Program Files\\"`.

Finally, although a single-quote character, `'`, can be written directly into any string, it may _optionally_ be
escaped with a backslash, as `\'`. This is because, in addition to String literals, Scala also provides syntax
for `Char` literals, and maintains consistency between their escaping rules. This syntax uses single-quotes
instead of double-quotes, and obviously can accommodate only a single character.

Examples of `Char` literals are, `'a'`, `'\''`, `'"'`, `'\"'`, `'\b'`, `'π'` and `'\u03c0'`. Note that the
double-quote in a charecter literal may be _optionally_ escaped, much like a single-quote in a string literal.

Note that a one-character string literal, such as `"a"`, represents a different type of object to a character
literal, such as `'a'`.

## Triple-quoted strings

Sometimes having to escape these characters can lead to code becoming less readable, particularly when a string
flows onto several lines.

To help, Scala provides an alternative way of delimiting a string literal using three double-quotes (`"""`) to
start and end the string, so that it becomes possible to use _any_ characters (including newlines,
double-quotes, and backslashes) inside the string, apart from the special sequence, `"""`, which will terminate
the string literal.

So this enables strings such as,
```scala
"""C:\Program Files\"""
```
or,
```scala
val address = """221B Baker Street
London
England"""
```

This last example features a potential (but slight) annoyance: the first line does not align vertically with the
second and third lines, and these latter lines will not typically match the code's indentation style. We would
prefer to write code which looks like this,
```scala
val address = """221B Baker Street
                 London
                 England"""
```
but unfortunately this will include seventeen spaces before each of the last two lines.

Scala provides a simple solution through the `stripMargin` method which can be called on a `String` instance,
requiring a small amendment to how we write the string:
```scala
val address = """|221B Baker Street
                 |London
                 |England""".stripMargin
```

The pipe symbols, `|`, and any tab or space characters that appear to the left of them on the same line will be
removed from the resultant string.

## Immutability

Strings in Scala are _immutable_. That means that a reference to a string will always point to exactly the same
sequence of characters in memory. When we want to modify a string, we cannot simply mutate the characters in
memory; we can only construct a new string, possibly deriving it from the original string, but leaving that
original string unchanged.

One of the most commonly-used operations on a string is its `+` operator, which will join one string to another.
It's used in exactly the same way as additing two numbers together, and while it's an identical symbol with a
_similar_ purpose, it's a _different_ method.

```scala
def sayHello(name: String): Unit =
  println("Hello, "+name+"!")
```

This can be convenient for constructing simple joins between a few strings, but the syntax can become less
readable (and less easy to write) when many strings are combined, typically when a number of dynamic string
expressions are interspersed with static string literals, for example,
```scala
"There are three characters, "+c1+", "+c2+" and "+c3+"."
```

## Interpolated strings

And thankfully, alternative syntax exists for uses such as this. For the string above, we can instead write:
```scala
s"There are three characters, $c1, $c2 and $c3."
```

This should appear more readable than before. This is an _interpolated string_, an expression which generates
a new `String` value by _substituting_ or _interpolating_ the values `c1`, `c2` and `c3` into the string
literal, based on their runtime values.

The `s` prefix before the opening quote is required to a string literal as an interpolated string, and the `$`
symbols indicate that the identifiers which follow them represent a substitution. Following an `$`, the
identifier names will be read until reaching a character which could not be a valid continuation of an
identifier name.

That means that a substitution, `"$string"` would refer to the identifier `string`, even if an identifier called
`str` were in scope, and `string` were not. Or conversely, when making a substitution, we must ensure that the
character immediately following the identifier we want to use would be invalid as a continuation of the
identifier name, for example, `.`, `,` or ` `.

But when this isn't possible, we can use braces (`{` and `}`) to wrap the identifer, for example,
```scala
val thing = "character"
s"There are three ${thing}s, $c1, $c2 and $c3."
```

Within substitution braces, Scala permits not just identifiers, but any expression. We could, for example, write
an arithmetic expression inside a substitution in an interpolated string:
```scala
def describe(width: Int, height: Int): String =
  s"The rectangle's area is ${width*height}."
```

While the result of `width*height` is an `Int` value, it will—as with any expression—be converted automatically
to a `String` when the substitution is made.

In an interpolated string, a `$` _always_ indicates a substitution, which introduces a new escaping problem: how
to substitute an actual `$` character into an interpolated string. That may be achieved simply by writing the
`$` character _twice_, for example, `"$$400"` represents `$400` as a string.

Interpolated strings may be single-quoted or triple-quoted, so this would also be a valid interpolated string:
```scala
val str = s"""|   Name: $name.
              |    Age: $age
              |Address: $address""".stripMargin
```
One very subtle potential trap remains when working with interpolated triple-quoted strings, though. Unlike
their non-interpolated counterparts, backslash escapes _are_ interpreted as escapes, and this can be extremely
unintuitive. For example, the string, `s"""\t"""`, and the string, `"""\t"""`, do not represent the same values.
The first is a one-character string containing the tab character, whereas the second is a two-character string
of a backslash and the letter `t`.

Thankfully, most of the time, using a triple-quoted string obviates the need to use escaping, but it remains a
counterintuitive detail of the language. But in general, Scala's string-handling capabilities are comprehensive
and offer a selection of convenient syntax for many different use-cases.

?---?

# If we define a string,

```scala
val str = """\\u0033"""
```

then what is the value of `str.length`?

- [ ] `1`
- [ ] `2`
- [ ] `3`
- [ ] `5`
- [ ] `6`
- [X] `7`
- [ ] `11`

# We will define a string containing a single newline character, thus,

```scala
val newline: String = "\n"
```

Now, all of the following string expressions look like they _might_ contain a newline character. Select all of
the expressions that actually do contain a newline somewhere in their resultant `String` value.

* [X] `"\n"`
* [X] `s"\n"`
* [X] `s"""\n"""`
* [ ] `"""\n"""`
* [ ] `s"${"$newline"}"`
* [ ] `"$$newline"`
* [X] `s"${'\n'}"`
