The patterns we have seen so far have been described in terms of literal values and case classes. But we can
also match a value by type, subject to some important restrictions.

A limitation of running code on the Java Virtual Machine is that its runtime type system is much less expressive
than Scala's, and Scala's rich types, which are known at compile-time, must be simplified or _erased_ to pale
shadows of themselves. At runtime, of course, we do have the advantage of having actual values which can be
inspected, but we can not always accurately know the type a value had when it was created, just by inspecting
it.

This is rarely a problem most of the time, but pattern matching can often expose this mismatch between Scala's
type system and the JVM's more limited type system when we attempt to match a value by its type.

For simple types, we can use the familiar `: Type` syntax after any pattern, and Scala will add an additional
constraint to the match that the value must be of that type. For example,
```scala
def getId(values: Map[String, Any]): String = values("id") match
  case _: String => "string"
  case _: Int    => "integer"
  case _: Node   => "node"
  case _         => "something else"
```

Be careful not to write `case Node =>` instead of `case _: Node`. The former would attempt to match for equality
with a _value_ called `Node` (if it exists, the `Node` type's companion object), not a value which is an
instance of `Node`. As usual, an identifier we see after a `:` will be a type.

## Union types

A value with a union type, such as `Int | Double | BigDecimal`, will be an instance of one of the types in the
union—`Int`, `Double` or `BigDecimal`—and we would normally use pattern matching to process the value
according to its type. Often, this would be an operation which transforms the value into an
instance of a unified (non-union) return type, which should make further processing easier, but not always.

We can pattern match by type on each type in the union, like this:
```scala
def increment(value: Int | Double | BigDecimal): Int | Double | BigDecimal =
  value match
    case value: Int        => value + 1
    case value: Double     => value + 1
    case value: BigDecimal => value + 1
```

Be careful with operator precedence. Writing `case _: Int | Long` is not the same as writing
`case _: Int | _: Long`: the `|` in both of these examples has lower precedence than the `:` which indicates
that a type should follow. `|` is interpreted as _pattern alternation_. So `case _: Int | Long` means
`case (_: Int) | Long`, which would match on any value which is an `Int` _or_ a value which is equal to the
companion object, `scala.Long`. It's unlikely we would ever mean that!

To match on a union type, we should write `case _: (Int | Long)`.

## Generic types

It would seem very natural to extend this functionality to matching on generic types, like `List[Int]` or
`Option[String]`, but this is not quite so easy.

```scala
def elementType(values: Seq[Any]): String = values match
  case _: List[Int]    => "integers"
  case _: List[String] => "strings"
```

Unfortunately, however, the runtime instance `values` is erased to a parameterless type (represented
internally as a runtime type such as `Lscala/collection/immutable/Vector` or `Lscala/collection/immutable/List`)
and is the same regardless of whether it was created as a `List[Int]` or a `List[String]`. In Scala, we can
accurately use the wildcard type `List[_]` to represent the runtime type of all varieties of `List` or `Vector[_]` to represent all varieties of `Vector`, specifying no more or less detail than
is knowable at runtime about the time. But, of course, the type parameter of `values` is lost.

If we attempt to write a match expression like the one above, Scala would warn us that the `Int` and `String`
type parameters are unchecked, though the code would still compile. But unfortunately, if we were to call the
method as `elementType(List("one", "two", "three"))`, it would match the first case, and the expression would return
`"integers"`. In fact, the second case is unreachable for this reason.

This may seem like an annoying limitation. It would certainly be more convenient to know the value's exact type.
But it is usually more of an inconvenience than a complete dead end. This is because we can often proceed
without knowing the generic type parameter until we have an instance of the type of the parameter, such as the first
element of a `List[String]`.

Here is the same example, rewritten to use the head of the list to determine its type,
```scala
def elementType(values: Seq[Any]): String = values match
  case xs: List[Any] => xs.head match
    case x: Int        => "integers"
    case x: String     => "strings"
```
The `head` value is a different value, with its own runtime type, and can be used to provide evidence of the
`List[_]`'s type parameter.

But, this requires the `head` value to exist, of course! If we had an empty list, the evidence we need would be
unavailable. So, how would we identify whether we have an empty list of `Int`s or an empty list of `String`s?
But this would be asking the wrong question: it doesn't matter! If we have no elements, it makes no difference
whether we assume that "all zero elements" are `String`s or `Int`s. And at any point that we have a value, we
can test its type.

This might seem a little unintuitive at first, but to further enforce the point, remember that we only have one
instance of the empty list, `Nil`. Whether we have the list, `1 :: 2 :: 3 :: Nil` or `"a" :: "b" :: "c" :: Nil`,
they both point to exactly the same object: an empty list can be a list of any type, and likewise `None` can be
an `Option` of any type.

Here is a safer way to write the expression above,
```scala
def elementType(values: Seq[Any]): String = values match
  case xs: List[Any] => xs.headOption match
    case None            => "empty"
    case Some(x: Int)    => "integers"
    case Some(x: String) => "strings"
    case _               => "other"
  case _             => "other"
```
which also shows how a type pattern can be nested within an extractor. Note also how there are two separate
`match` expressions here, and we are using the indentation of the `case` lines to indicate which `match` block
each one belongs to. We have also aligned the `=>`s vertically, and differently for each `match`, but this is
just a stylistic choice to help readability.

It is easy to reason about collection types such as `List[_]` so `Option[_]` in this way, but what about other
parameterized types? In general, for generic types whose type parameter appears in the return types of its
member methods, we can always match using wildcard types, and defer matching on their type parameter until
we have an instance of that type to inspect. The cost of erasure is that pattern-matching code may be
distributed widely throughout a program.

?---?
# Which code correctly checks if `list` values are of a numeric type?
 - [ ] ```scala
 list.head match 
   case None                => "Empty!"
   case Some(x: Int | Long) => "Numeric"
   case _                   => "Non-numeric"
```
 - [ ] ```scala
 list.headOption match 
   case None                => "Empty!"
   case Some(x: Int | Long) => "Numeric"
   case _                   => "Non-numeric"
```
 - [X] ```scala
 list.headOption match 
   case None                  => "Empty!"
   case Some(x: (Int | Long)) => "Numeric"
   case _                     => "Non-numeric"
```
