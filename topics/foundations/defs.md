# Declarations

From a syntactic perspective, the code we write in Scala will be a composition of:
- literal values, such as `"orange"`, `1`, `82.7` and `'z'`
- Scala keywords, such as `trait`, `def`, `for` and `lazy`
- some special symbols to help with parsing, such as `:`, `[`, `]` and `,`
- other identifiers chosen by _us_ and other library developers, such as `Option`, `document` and `+`

These identifiers fall into two categories, _term identifiers_ and _type identifiers_. In both cases, the use
of the identifier will either _introduce_ that identifier into the current context, or will be a reference to a
unique definition, elsewhere in the code where that identifier is first introduced.

The Scala compiler will know from the syntactic context of the source code whether an identifier is a _term_ or
a _type_. For example, in,
```scala
class Item(element: Element):
  def describe: String = s"This is a ${element.name}"
```
the compiler knows that `Element` and `String` are type identifiers which refer to definitions elsewhere. A big
clue, in general, is that `Element` and `String` appear after a colon (`:`), while `Item` is also a type
identifier, albeit a definition, because it appears after the keyword `class`.

Likewise, `element`, `describe` and `name` are term definitions. Similarly, their appearance before a colon
suggests this. The first occurrence of `element` and `describe` are definitions which introduce these terms, and
`element` and `name`—which appear in the expression `element.name`—are references.

We often describe the place in the source code where the new identifier is introduced as the _definition site_,
while every usage is referred to as the _use site_ (where "use" is pronounced like the noun—with a hard `s`—not
like the verb) or _call site_, particularly in the case of methods.

## Term Identifiers

Term identifier references usually appear in _expressions_ (even if that expression is nothing more than just
the term itself!) and in this context they refer to a definition which will produce some value when evaluated at
runtime.

Identifiers are used in expressions to refer to methods and values defined elsewhere. But in the context of an
expression, an identifier which refers to a _value_ is indistinguishable from an identifier which refers to a
_method_: in both cases, without looking up the origin of that identifier, all we know is that it will
_evaluate_ to a single _value_ when the code is run, almost as if we had written that value directly in place of
the identifier.

For example, we can create a new identifier called `version` with a `val` definition, like so,
```scala
val version = 7
```
and then refer to `version` multiple times elsewhere in the context of that definition, for example:
```scala
if fileVersion < version
then println(s"The file version is lower than the current version ($version)")
```

And this would would behave exactly as if we had written:
```scala
if fileVersion < 7
then println(s"The file version is lower than the current version (7)")
```

If, as we maintain our code, the version number needs to change, for example, from `7` to `8`, then we can
change this just once in the definition,
```scala
val version = 8
```
without having to make any changes to code elsewhere. And this is essentially the same as how we use words in
natural language. Most words do not change meaning very often, but sometimes our understanding of a word such as
"home" might change, for example, when we move somewhere else. We can still use phrases such as, "I'll meet you
at home," unchanged, and we know that at different times the particular location "home" refers to may be
different.

Identifiers are typically concise words or a couple of words joined together without spaces. Their purpose is to
_identify_ what they refer to, so they should do that unambiguously and with enough precision, but should not be
overly long if a shorter term suffices.

The rules for what constitutes a valid identifier are more complex than might seem necessary, but to begin with,
we can choose identifier names that are alphanumeric, do not begin with a number, and are not the same as any
other Scala keyword. This should provide all the flexibility we need. In a later lesson, we can look at more
complex naming rules.

Identifiers are always case sensitive. For example, values called `head` and `Head` are unrelated to each other,
and considered as different from each other as two identifiers called `alpha` and `omega`.

New term identifiers can be introduced into a scope via several different routes, but the most direct way is
through a new definition, using the keywords `val`, `def`, or occasionally, `var`. The usage of each of these
keywords looks very similar. For example,
```scala
val first: String = "one"
def second: String = "two"
var third: String = "three"
```
will introduce three new identifiers, `first`, `second` and `third`, each with a type specified as `String`,
which can all be referenced in exactly the same way,
```scala
println(s"The first few cardinal numbers are ${first}, ${second} and ${third}.")
```
and we could not observe any apparent difference in their behavior from an example like this; in each case, it
would appear as if the values `"one"`, `"two"` and `"three"` had been substituted into the string in exactly the
same way, despite all being introduced with different keywords.

But there are subtle differences.

The keyword `val` defines a new _value_: a field in a class, trait or object, or a local value within a method.
This can be thought of as an allocation of some memory to store a value (either a primitive value, or a
reference to an object) for as long as necessary. In the case of an object (or an object created from a class),
that means until the object can no longer possibly be used, or in the case of a method, until the method
completes and returns a value.

Every time an identifier which refers to a `val` definition is evaluated, it will supply the value stored in
memory. That operation will always be near-instaneous, because it just has to look up a value in memory which
has already been calculated.

A definition using the `def` keyword will behave in exactly the same way if it's implementation is just a simple
expression, as in our earlier example,
```scala
def second: String = "two"
```

But the keyword `def` actually defines a new _method_; a reusable piece of code which is executed every single
time it is evaluated; that is, every single time it is referenced. The "code" in `second`'s definition is so
simple that it does nothing more than return the same value each time. Though it could do something more
interesting, like this:
```scala
def second: String =
  println("Accessed the second method.")

  "two"
```

With this definition, whenever a reference to `second` is evaluated, a message will be printed to the console.
That means that code such as,
```scala
println("The result of ${second} plus ${second} is four.")
```
would print the following, in order:
```
Accessed the second method.
Accessed the second method.
The result of two plus two is four.
```

Even though the references to the identifier `second` appear on the same line, it nevertheless appears _twice_,
and because `second` is a method and not a value, it must be evaluated twice, and the `println` statement is
executed twice.

Compare that to what would happen if we similarly included a `println` statement in a `val` definition for the
value `first`:
```scala
val first: String =
  println("Accessed the first method.")

  "one"

println(s"The result of ${first} plus ${first} is two.")
```

The output on the console would be,
```
Accessed the first method.
The result of one plus one is two.
```
even though there are two references to the identifier `first`.

The runtime will execute the implementation of the value, `first`, as soon as it encounters it, in the process
printing the line, `Accessed the first method.`, once, and storing the result, `"one"` in memory, so that
subsequent references to `first` can use the value directly. And thus, in the `println` statement, both
references to the identifier `first` behave as if the value, `"first"`, had been substituted directly into the
string.

This should demonstrate the difference between `val` and `def` definitions, and how that difference is largely
opaque at the use site.