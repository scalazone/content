# Subtyping

Some types may share some features or behaviors in common, and we can assert useful relationships between
certain types to indicate, at a very fundamental level, allows us to encode the concepts of _generality_ and
_specificity_ through the type system.

Unlike many other languages where all types are different from each other, and "equally different", subtyping is
fundamental to Scala's type system. It has to be considered by the compiler on almost every line of code; every
time a method is invoked, or a value is returned, the compiler may have to consider subtyping relationships
between types.

We can say, for example, that a `List` of `String`s has all of the properties of a `Seq` of `String`s, or
equivalently, a `Seq[String]`s has no properties which a `List[String]` doesn't. But a `List[String]` also has
the `::` operator for prepending an element which `Seq[String]` does not.

This is called a _subtyping_ relationship, and we say that `List[String]` is a _subtype_ of `Seq[String]`.
Conversely, we would say that `Seq[String]` is a supertype of `List[String]`. `Seq[String]` is also a
supertype of `Vector[String]`, because `Vector[String]` has all of the properties of `Seq[String]` (plus some
more). But this does not imply any particular subtyping relationship between `List[String]` and
`Vector[String]` because `List[String]` has methods which `Vector[String]` does not have, and `Vector[String]`
has methods which `List[String]` does not have. They are unrelated types, though later we will see that it is
still significant that `List[String]` and `Vector[String]` have a common supertype of `Seq[String]`.

The usefulness of subtyping arises from the Liskov Substitution Principle, which asserts that anywhere in our
code that a particular type, `T`, is expected, a value of a different type, `S` may be provided as long as `S`
is a subtype of `T`. This applies when specifying the parameters of a method when it is called, where the method
definition specifies the expected types for each parameter, and to the body of a method, variable or value,
where the implementation must result in a value of a type which is a subtype of the declared return type.

Here's an example of how that can work. We can define a simple method, `product` which will multiply a
sequence of integers together.
```scala
def product(xs: Seq[Int]): Int =
  if xs.isEmpty then 1 else xs.head*product(xs.tail)
```

This implementation uses three methods of `Seq[Int]`: `isEmpty`, `head` and `tail`.

We can now call this with a `List` of `Int`s,
```scala
val xs: List[Int] = List(2, 3, 5, 7, 11)
val result: Int = product(xs)
```
or a `Vector` of `Int`s,
```scala
product(Vector(3, 3, 3, 7))
```
and, as we would hope and expect, these will both typecheck and run, even though the types were not an exact
match.

This works because `List[Int]` and `Vector[Int]` are both subtypes of `Seq[Int]`, which means that every
property of `Seq[Int]` is also a property of `List[Int]` and `Vector[Int]`, and if the body of the method
`product` typechecks at the definition site (which expects only a `Seq[Int]` and does not even need to know of
the existence of the types `List[Int]` or `Vector[Int]`), then providing a value which satisfies _more_
properties than required, is `List[Int]` and `Vector[Int]` do, will certainly be sufficient.

We often say that `List[Int]` _conforms to_ `Seq[Int]`. That means it is a _more specific_ or a _more precise_
type than `Seq[Int]`, and that `Seq[Int]` is a _more general_ or _less precise_ type than `List[Int]` or
`Vector[Int]`.

The motivation for defining `product` in terms of a `Seq[Int]` instead of one of a more precise type is that
we should not impose unnecessary requirements on users of our programming interface. This may be described
through the [Principle of Least Power](https://en.wikipedia.org/wiki/Rule_of_least_power). By this logic,
`Seq[Int]` is not the only type we could have chosen for the definition of `product`. `Iterable[Int]` is a
supertype of `Seq[Int]` which also has the methods `isEmpty`, `head` and `tail`. Subtype (and supertype)
relations are _transitive_ so given that `Seq[Int]` is a subtype of `Iterable[Int]` and `List[Int]` is a
subtype of `Seq[Int]`, then it follows naturally that `List[Int]` is a subtype of `Iterable[Int]`.

But we might ask _why_ these subtype relationships exist at all. The answer comes from the definitions of the
generic template types `List[T]`, `Seq[T]` and `Iterable[T]`: these template definitions specify inheritance
relationships between them. While the full story is more complex, the definitions for these templates look
similar to this:
```scala
abstract class List[+A] extends Seq[A]
trait Seq[+A] extends Iterable[A]
trait Iterable[+A]
```

The fact that the class `List[A]` extends `Seq[A]` means that the properties implied by every member defined in
`Seq[A]` are also properties of `List[A]` just as those members are inherited. Likewise every property of
`Iterable[A]` is a property of `Seq[A]` and herce `List[A]`.

Defining a template is not the only way to introduce a new type into Scala, but it is the most familiar for most
developers, and inheritance between templates is therefore the most familiar way to introduce subtype
relationships between types. But new types can also be created by composing existing types, and depending on the
nature of the composition, subtyping relationships may automatically be conferred by the compiler between these
new types and other types, without any explicit inheritance being defined. We will look at these rules later.

## Types as Sets

Although they are foundationally different, types can be viewed as sets of properties or sets of instances, and
a _subtyping_ relationship between types translates in an interesting way into _subset_ relationships when
viewed this way.

If `A` is a subtype of `B`, the set of instances of implied by the type `A` is a _subset_ of the set of
instances implied by `B`, or conversely, if `a` is an element of the set `A`, that implies that `a` is also an
element of the set `B`. Clearly, we can make a similar claim about _supertype_ and _superset_ relationships.

But if we view the type `A` as a set of properties, and `B` as a set of properties, then the subset relationship
is reversed: if `A` is a subtype of `B`, then the set of properties of `A` is a superset of the set of
properties of `B`.

Or put simply, subtypes have more properties and fewer instances; supertypes have fewer properties and more
instances.

Category Theory is a profound and interesting topic, but is beyond the scope of this course. However, it
provides good context for understanding these relationships, and the duality between properties and instances in
the context of types.

For an experienced Scala developer, thinking about types should become second nature, but it remains a complex
topic, and sometimes we need to reason about types more carefully. This is where thinking about types as sets of
instances or sets of properties can be useful. Understanding subtyping is crucial to understanding how Scala
works. With pracitice, experience and familiarity, it can become very easy to reason about types and their
relationships, and to harness the power it provides us to express specificity and generality in our code.
