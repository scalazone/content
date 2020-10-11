# Types

Scala uses _types_ during compilation to check that the code we write is self-consistent. Scala's type system
offers us the single greatest protection from coding mistakes; it makes it impossible for us to even attempt to
run code which the compiler can prove is inconsistent.

If, for example, we were to create a value which was a string of text, and then try to subtract five from it,
the Scala compiler would rightly identify that such code is not self-consistent; it's a compile error.
```scala
val message = "Hello, World!"
val result = message - 5
```

It could do this without us even mentioning the name of a type in our code.

At the simplest level, types give us the means to identify the sort of thing a value _is_ (or at least what it
_represents_), and from that the Scala compiler can work out if the value is being used in a way that makes
sense for something of that nature; for an instance of that type.

At a deeper level, types provide a complete language for describing, in precise detail, the known properties and
expectations we should have of an instance of a particular type, as well as scope for describing, as will become
apparent later, what aspects of the value are _unknown_.

Types provide a _language_ to express the capabilities and expectations of values, when writing code, and when
communicating errors from the compiler to the programmer. The language of types is rich and expressive, and has
at its foundation, the DOT calculus. As well as providing us with a basis to trust what the compiler tells us
(as long as we do not try to circumvent it!), DOT allows us to combine types algebraicly, almost as easily as we
would numbers.

## Properties

We can think of a type as shorthand for describing the properties that its instances will have. When we define
a new class, it introduces a new type (or many types) corresponding to that template. Having defined a new
class with a name, that name can be considered equivalent to the properties implied by the class definition.

What exactly is a "property", though? The concept is abstract, to the extent that a property may be any detail
the compiler knows to be true, which it may rely upon to guarantee the correctness of our code. Examples may be:
- "`length` may be called on this value"
- "`isEmpty` may be called on this value, and will return a `Boolean`"
- "this value conforms to the type `Seq[Int]`"
- "`++` may be called on this value with a parameter that conforms to `Seq[Int]` and will return a `Seq[Int]`"

These properties can be _implied_ on instances of these types because they were constructed by a template which
defined methods in its body which infer those properties. But properties should be thought of in a more abstract
sense than just _methods_ or _members_. For example a property of a `String` is that we can call the `substring`
method on it, passing it the integer `4`. But it also has the property that we can call the same method, passing
it the integer `2`. Though a single method, `def substring(index: Int)`, implies both properties.

There are certain details of an instance which cannot be represented by its type. It is not possible, for
example, to specify properties an instance should _not_ have. And details about the methods other than the
number and types of their parameters and their return type cannot be encoded in a type. For example, it would
not be possible to specify that a method is pure or deterministic in its type.

It's important to remember that a value has a type because it was constructed as an instance of a particular
template, and _not_ because it has the properties needed to conform to that type. In fact, a value may have
every property implied by a particular type, whilst still not having that type if it was not constructed using a
template related to that type.

This is a consequence of Scala's type system being _nominal_, that is to say, _name-based_. The name of the
type implies its structure, but a type's structure does not imply its name. This is in contrast to a
_structural_ type system which would consider two types to be equal if the set of properties each implies
is equal.

As a contrived example of why this may be useful, consider two classes,
```scala
class Relation():
  def close: Boolean

class Door():
  def close: Boolean
```
where the `Relation` class has a boolean parameter to determine if it is a close relation or not, and the `Door`
class has a method to close the door, returning `true` if the door was successfully closed. These methods have
the same name, but completely different purposes, and the classes have identical structures. But an instance
of a `Door` is never an instance of a `Relation`, nor is a `Relation` an instance of a `Door`.

The names of types share a namespace, the _type namespace_, and while Scala has a set of rules which dictate
exactly when and where a particular type name can be used (and resolve unambiguously to a definition the
compiler can use), if two different types with the same name are accessible in the same place, it will only be
possible to resolve one of them, and Scala may additionally produce an error in the event of such a conflict.
We will learn more about this during the topic of _scopes_.

This is in contrast to the _term namespace_ which contains the names of _terms_, that is, objects, values,
methods and values. The _term namespace_ has the same constraint that a single identifier must consistently
resolve to only one _term_ object, but the distinction between the two namespaces is important because the same
name may refer to both a _type_ and a _term_, which are different entities. The syntactic context is all that
the compiler needs to decide whether a particular name refers to the type or the term by that name. Put another
way, Scala always knows from the place in the code whether it is expecting us to write the name of a type or the
name of a term.

By convention, types always begin with capital letters, except in some very unusual circumstances. Terms
_usually_ start with a lower-case letter, but not always: terms starting with capital letters are very common
too. We will learn about these later.

It is useful, when reading Scala code, to get a feel for which identifiers represent types. The case of the
first letter of the name is a strong indicator, but additionally, whenever we see a colon with a name after it,
that name is a type, assigned to the term or definition that comes before it. Here are some examples:
- `var count: Int = 0`, introducing the variable, `count`, and declaring it to have type, `Int`
- `def add(n: Double): Double`, defines the `add` method, which returns an instance of the type `Double`, and
  furthermore, its parameter, `n` has the type `Double`
- `val s = None: Option[String]`, where the right-hand side has the value `None`, but whose type is explicitly
  specified to be `Option[String]`
- `case class Address(name: String, lines: List[String], country: Country)`, defining the parameters, `name`,
  `lines` and `country` with the types, `String`, `List[String]` and `Country`, respectively; note that
  `Address` is also a type, introduced by this definition
- `case _: Boolean =>`, a pattern which tests if the value is an instance of a `Boolean`.

Types also commonly appear inside square brackets (`[` and `]`), following another identifier (which may or may
not be a type itself), for example,
- `Set[String]`, where `String` is a type, and applied to another type, `Set`; we would normally read this as,
  "a set of strings"
- `value.as[Int]`, where `Int` is a type, applied to the method `as`
- `private[Table] var count = 0`, a less common occurrence, which restricts access to the variable, `count`
  to within the `Table` template, whose name is in the type-namespace.

The understanding of types in Scala is important, and the depth of the subject means that it can, at times, be
complex. Scala's type system has a variety of features which can represent many precisely- or
imprecisely-defined collections of objects and their common properties.

Luckily, almost all the types we work with in a typical program will use only a few common features of Scala's
type system, so we can focus on learning these, and leave the more advanced features until later, without
putting many limitations on the code we can write straight away.

?---?

Below are several short fragments of code which include a single reference to either `alpha` or `Alpha`. In some
fragments, it is a term, while in others it represents a type. Even if you don't fully understand the code, try
to understand whether each is a term or a type.

# Select all the fragments of Scala code where `alpha` or `Alpha` looks like a type (and not a term). There
# are no trick questions!
- [X] `val x: Alpha = get()`
- [ ] `val alpha = "a"`
- [ ] `val Alpha = "A"`
- [X] `case x: Alpha => "a"`
- [ ] `def go() = alpha[String]()`
- [X] `def go() = get[Alpha]`
- [X] `class Item(value: Alpha)`
- [ ] `2 + Alpha()`
- [X] `private[Alpha] def apply(): Unit`

Consider the following class and object definitions:
```scala
class Rectangle(width: Double, height: Double):
  def size: Double = width*height

object Square:
  def width: Double = 4.0
  def height: Double = width
  def size: Double = width*height
```
# Is the object `Square` an instance of the type `Rectangle`?
* [ ] Yes
* [X] No

# Which of the following properties of a value could be represented by its type?
- [X] "it has a member called `apply()` which will always return the value `2`"
- [X] "it has a member called `count` which takes any number of parameters of the same type"
- [ ] "it does not have a member called `run()`"
- [ ] "it has a member called `apply()` which will always return a different value"