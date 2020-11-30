## Infix Extractors

We commonly want to match on collection types like `List[Int]` or `Vector[String]`, and Scala offers special
support for matching against collections using _infix extractors_.

Let's start with an example of matching on a `List[Int]` using the extractor, `::`. We can split a list into
its head and tail within a pattern, like so:
```scala
def tailOrNil(xs: List[Int]): List[Int] = xs match
  case head :: tail => tail
  case _            => Nil
```

The pattern `head :: tail` looks a little different from the patterns we have seen so far, but it's analogous to
the infix method `::` which constructs a new `List[_]` by prepending an element to an existing list, only this
time it's decomposing an existing list into a head and a tail—if, and only if, the list has at least one
element. If it doesn't, then the pattern won't match, and we can deduce that the scrutinee can only be the empty
list, `Nil`.

This can be particularly convenient for writing recursive functions using `List`s. We can define an efficient
`sum` method which operates on a `List` of integers.
```scala
def sum(xs: List[Int]): Int = xs match
  case head :: tail => head + sum(tail)
  case Nil          => 0
```
Each invocation adds the integer at the head to the sum of the tail, with a special case for `Nil`, whose sum is
zero. Note that the order of the case clauses does not matter, either. A list is either empty or it can be
decomposed into a head and a tail.

Here's another example of a recursive method which gets the second-to-last element of a `List[T]`, if it has
one.
```scala
def penultimate[T](xs: List[T]): Option[T] =
  xs match
    case head :: head2 :: Nil => Some(head)
    case Nil | _ :: Nil       => None
    case head :: tail         => penultimate(tail)
```

We first check if the scrutinee is a two-element list: or, literally, an element prepended to another element
prepended to the empty list. If this matches, we have our answer. If that fails to match, either because the
list is too short or too long, we first check if the list is one of the two cases that should not return a
value: a zero- or one-element list. If neither of the first two cases matches, it means the scrutinee is too
long, so we recurse on the tail of the list.

The `::` extractor is very useful for working with `List`s in particular because it corresponds exactly to their
recursively-defined structure: a head, which has the `List`'s element type, attached to a tail which is another
`List`. To split a list into its head and tail is a fast operation, regardless of whether the list is short or
long, much as it is a fast, constant-time operation to construct a new list by prepending an element.

Conversely, splitting a list into its initial and last elements is not a constant-time operation: it will be
slower and slower the longer the list is, so it's desirable to use the `::` extractor for working with `List`s.

## Matching Vectors

For other sequence-like collections, such as `Vector`, we have two additional extractors available to us:
`+:` and `:+`. The first, `+:` is equivalent to `::`, but works on any collection that is a `Seq`, not just
`List`s. The second, `:+` allows extraction of the last element of a collection. Here is how we could use it to
provide an alternative `sum` implementation for a `Vector[Int]`.
```scala
def sum(xs: Vector[Int]): Int = xs match
  case init :+ last => last + sum(init)
  case _            => 0
```

Like before, this finds the sum of all the elements in the collection, but it adds them in the opposite
direction: adding the last element to the sum of the initial elements (all apart from the last), instead of
adding the head element to the sum of the tail.

`:+` and `+:` are, character-for-character, the reverse of each other, and operate on reverse ends of a
sequence, but it's easy to mix them up. The easiest way to remember which way round they go is to remember that
the colon (which is a symbol containing _multiple_ dots—two!) is always on the side of the collection, whereas
the plus symbol is always on the side of exactly one element. So we could read a pattern such as
```scala
case a +: b
```
and know immediately that `b` is the collection type and `a` is a single element, event though their names do
not indicate this.

We might also expect there to be a `++` extractor for sequences, to complement the operator `++` which joins
two sequences together. But this wouldn't be possible, since there are many different ways a sequence may be
split into two, and the compiler would need to make a choice about which elements to include in the first part
and which to include in the remainder, and this is enforced by the order of evaluation during a pattern match:
the extractor must decompose the scrutinee into parts first, and only then could pattern matching continue to
check nested extractors.

## Desugaring

These infix extractors are actually just ordinary extractors with two parameters, used in an infix position. For
example, we could define a two-parameter extractor such as,
```scala
object Point:
  def unapply(value: Double): Some[(Double, Double)] =
    Some((value.floor, value - value.floor))
```
which will decompose a floating-point number into its integral part, and its fractional part. We can use it
in a pattern, like this,
```scala
def fractional(x: Double) = x match
  case Point(_, fraction) => fraction
```
but without changing the definition, we can also write the pattern as:
```scala
def fractional(x: Double) = x match
  case _ Point fraction => fraction
```

Scala interprets these in exactly the same way. While in the first version, `Point`'s two parameters appear
after the extractor (inside parentheses), the second "infix" version moves the first parameter before the
extractor name, `Point`, leaves the second parameter after, and removes the parentheses and comma.

## Generalizing Extractors

This works for any extractor, though it's less common to use it for extractors with alphanumeric names. We
could, however, rename `Point` to a symbolic name, like `+`, and then write,
```scala
object + :
  def unapply(value: Double): Some[(Double, Double)] =
    Some((value.floor, value - value.floor))

def fractional(x: Double) = x match
  case _ + f => f
```
to give us a method which returns just the fractional part of a `Double`.

Note that we have to add a space between the `+`, which is the name of the object, and the syntactic `:`, which
indicates the start of its definition, so that the two are not interpreted as the same name.

Infix extractors are convenient for _deconstructing_ objects which were _constructed_ using infix operators.
This maintains the syntactic correspondence between the construction of a value, and a pattern which matches
against it.

?---?

# Select the code that is equivalent to the pattern, `case In(Of(8, April), year) =>`:

- [ ] `case 8 In April Of year =>`
- [ ] `case 8 In (April Of year) =>`
- [ ] `case In(Of(8, April, year)) =>`
- [X] `case Of(8, April) In year =>`
- [ ] `case In(8, Of(April, year)) =>`

# The following code is equivalent to one case clause which matches against a scrutinee, `s`. Which case clause?

```scala
if ~.unapply(s) == Some(("abc", "xyz")) then f
else ... // handle other cases
```

- [ ] `case ~.unapply("abc", "xyz") => f`
- [X] `case "abc" ~ "xyz" => f`
- [ ] `case Some("abc" ~ "xyz") => f`
- [ ] `case s => if s == ("abc", "xyz") then f`
- [ ] `case "abc" Some "xyz" => f`
