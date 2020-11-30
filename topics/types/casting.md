A type such as `List[String]` conforms to the type `Seq[String]`, and a value or expression which is a
`List[String]` may be used in any position that a `List[String]` or a `Seq[String]` or an `Iterable[String]` is
expected. We might as well say that such a value _is_ a `List[String]` and _is_ a `Seq[String]` and _is_ an
`Iterable[String]`, but at any given location in our code, a value can be proven to _be_ many different types,
but will have a single _most precise_ type known to the compiler, from which its conformance to other more
generaly types can be inferred by logical implication.

If, at any point, we explicitly _ascribe_ a specific type to a value, that type will _become_ the single most
precise type the compiler knows that it conforms to, and any subsequent usage of that value cannot assume the
earlier, more precise type. For example, the code,
```scala
val xs: Seq[Int] = List(4, 8, 16, 32)
val ys = 1 :: 2 :: xs
```
will not compile because the operator `::` is a member of `List[Int]` but not `Seq[Int]` and the ascription of
the type `Seq[Int]` explicitly _discards_ precision we know about the type of the expression,
`List(4, 8, 16, 32)`. It would have been equivalent (but less conventional) to have written this as,
```scala
val xs = List(4, 8, 16, 32): Seq[Int]
val ys = 1 :: 2 :: xs
```

Changing the type of a value is called _casting_, or _a cast_, and when the cast is from one type to a more
general type that it already conforms to, it is called an _upcast_. This is always a safe operation, which is to
say, Scala will only permit an upcast to a type for which conformance can be proven, and doing so will never
produce bytecode which would, under any circumstances, fail at runtime.

In fact, the operation of upcasting does not change anything at _runtime_. That is because every reference type
has a single _runtime type_ which is assigned to the reference when it is created, and is held (unchanged) for
its entire lifetime. So while the static type of a value may be different as that reference is used in different
contexts in the source code, its runtime type will not. That is because the runtime type of a value dictates
fixed details about the value, such as the number of bytes it uses in heap memory, and the offsets of each of
its fields within those bytes.

There are other occasions when upcasting may happen. The types `IOException` and `RuntimeException` are both
subtypes of the `Exception` type. If we had an instance of `IOException` and an instance of
`ArithmeticException` and we put them both into a `Set`, the compiler would have a quandry to decide what type
of `Set` it would be. It could not be a `Set[IOException]` if it contained an `ArithmeticException` because
`ArithmeticException` does not conform to `IOException`.

By exactly the same reasoning, it could not be a `Set[ArithmeticException]`. But it _could_ be a `Set[Exception]`
because both `IOException` and `ArithmeticException` conform to `Exception`.

If we were to subsequently iterate over both elements in this `Set[Exception]`, one element would be an
`IOException` and the other would be an `ArithmeticException`, but sets are unordered, so we would have no idea
which would come first, and all we would know about both elements is that they are `Exception`s.

## Downcasting

Given the possibility that values may be upcast to more general types, and the immutability of a value's runtime
type, we may have values with types that are known more precisely at runtime than at compile-time. But if we
do not know a value's precise type at compile time, we cannot rely on that value's more precise properties; the
Scala compiler will not permit us to compile any code which assumes those properties.

Thankfully, those values do not forever lose some of their functionality when their static type is upcast. It is
possible to test the runtime type of a value, and handle it in different ways depending on its type. If we
wanted to add an element to a `Seq[Int]`, we may prefer to add it to the end of a `Vector[Int]`, which can
perform that operation quickly, but compromise on prepending it to the start of a `List[Int]` which can
efficiently add elements at the beginning, but not the end.
```scala
def (seq: Seq[Int]).include(value: Int): Seq[Int] = seq match
  case seq: List[Int] => value :: seq
  case seq: Seq[Int]  => seq :+ value
```

Testing this, we get,
```scala
List(1, 2, 3).include(0)
```
and,
```scala
Vector(1, 2, 3).include(0)
```

On the right-hand side of each case clause, the `seq` value will be known to have the type which was matched in
the pattern. That means that we can recover the functionality, or properties, of a `List[Int]` even if it has
been lost, but we were forced to pattern match on the runtime value, and forced to consider the alternative case
where our value did not match the specified type (or risk a `MatchError` being thrown).

But pattern matching provides a safe way of converting from one type to another. Occasionally, though, we will
know with some certainty that a value has a particular more precise type, while the compiler is not able to make
the same assertion. These occasions are rare: the Scala compiler has very broad capabilities for reperesenting
the types of different values precisely, but they nevertheless occur.

To further exacerbate the problem, pattern matching cannot always test the full static precision of a type from
just its _runtime_ type. For example, a value may be known to be a `List[_]`, without it being possible to know
if it is a `List[Int]` or and `List[String]`, at least, not without checking at least one of its elements, and
that's not usually practical to do.

So there is a rare set of problems where the programmer can make stronger assertions about the types of values
in our code than the compiler is able to prove, and stronger than we are able to test at runtime. In these
cases, it may be necessary to _cast_ the value to a more precise static type, and this can be done using the
method `asInstanceOf`, specifying the type we wish to cast to.

Casting does not actually _change_ a runtime type in any way. It merely changes its _static_ type, and
correspondingly checks at runtime that the value's _runtime_ type is compatible with its _static_ type. This
check could fail, of course, and a `ClassCastException` would be thrown.

Here is an example:
```scala
val details: Map[String, Any] = Map(
  "age" -> 27,
  "locations" -> List("Vienna", "Tbilisi", "Bilbao")
)

val age: Int = details("age") match
  case n: Int => n
  case n      => 0

val locations: List[String] =
  details("locations").asInstanceOf[List[String]]
```

Here, we are storing some fields, indexed by `String`s, in a generic `Map`. We can access the age and a list
of locations by their indices, but the values taken from the map will have the type `Any`, which means that at
compile-time we know very little about them.

In the case of `details("age")` we can pattern match on the value to test that it is an `Int`, but we should
consider the case where it is not an `Int`, in order to avoid the risk of a `ClassCastException`. For the list
of locations, the runtime type does not hold enough information to check what type the `List`'s elements are.
(If we attempted a pattern match, the compiler would warn us that it can't check `List`'s parameter.) In this
instance, if we are certain that our value is a `List[String]` we may as well call `asInstanceOf[List[String]]`
on the value, to assign it the new static type.

Code like this should always be seen as a compromise, and while it is possible to cast values to different
types, this puts a greater reliance on the programmer to make no mistakes (or comprehensive tests) and less on
the compiler. If the compiler cannot prove that a value has a particular type, it may be an indication just that
the compiler cannot prove it, or it may further be an indication that it is not true!

Such code is also less resilient to change: an `asInstanceOf` cast may be justified thanks to careful analysis
of the code by a programmer that the value being cast always has the correct type. But if the basis of that
analysis changes, as the program changes, it may no longer be true that the cast is always correct. And
unfortunately, that is not something that the compiler can check.

Casting should therefore be used as a last resort, and while every effort should be taken to avoid writing
casts, refactoring as necessary, we may still see them in Scala code, and we need to understand what they are
doing.

?---?

# Consider the following code:

```scala
val berlin: List[Any] = List("Berlin", 1237, 13.405, 52.52)

val city = berlin(0).asInstanceOf[String]
val foundation = berlin(1).asInstanceOf[String]
val east: Int = berlin(2)
val north = berlin(3): Double
val city2 = city.asInstanceOf[Any]
```

Select every value definition which would compile successfully:

* [X] `val city`
* [X] `val foundation`
* [ ] `val east`
* [ ] `val north`
* [X] `val city2`

# Here is a similar example, which does compile successfully.

```scala
val chicago = List("Chicago", 1833, 41.8781, 87.6298)

val city = chicago(0).asInstanceOf[String]
val foundation = chicago(1).asInstanceOf[String]
val west = chicago(2).asInstanceOf[Double]
val north = chicago(3).asInstanceOf[Any]
```

Select every value definition which will run without exception:

* [X] `val city`
* [ ] `val foundation`
* [X] `val west`
* [X] `val north`
