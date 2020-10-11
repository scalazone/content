# The Underscore

Scala's use of the underscore (`_`) character has been a point of contention for as long as the language has
existed, as a consequence of its many varied uses, and the difficulty in knowing how it should be interpreted in
different contexts.

Rather than thinking of the underscore as having numerous specific meanings, it is much easier to think of it as
having a single meaning whose interpretation is dependent on context.

That meaning can most easily be described as "nothing", "everything", "something" or "anything"; a convenient
way of saying "whatever" or instructing the compiler to do the obvious thing without specifying something
specific. Regardless of the context, the `_` character can always be interpreted in this way. So rather than a
confusing symbolic operator whose purpose is unclear, we should see it very consistently as a way of indicating
the _unspecified_.

The rest of this lesson cover the variety of contexts in which underscores may appear in Scala source code.
These might not make sense yet, but should provide hints about where to look to try to understand these concepts
better.

## Imports and Exports

Import and export statements in Scala may use the `_` to help define what should and should not be imported (or
exported).

The most common form is when importing _everything_ inside a named package or object. So,
```scala
import com.example.data._
```
will import every member of the `com.example.data` package, and bring it into the current scope.

The same applies to `export` statements, like so:
```scala
export parent._
```

Every member of the `parent` object will be exported from the current object.

More confusing is the usage of an `_` in an `import` or `export` statement to indicate that a member should
_not_ be imported. So, the following statement would import everything from the `java.io` package, except the
`File` class:
```scala
import java.io.{File => _, _}
```

The way to read this should be, "from within the `java.io` package, discard `File` and include everything else".
The `_` character appears twice, firstly to indicate that `File` is discarded, and secondly as a wildcard import
of everything else.

## Lambdas

Underscores are very common shorthand for writing simple lambdas in Scala, using what is usually called
_placeholder syntax_, for example in, `xs.exists(_ < 10)`, which is short for, `xs.exists { x => x < 10 }`. This
style makes it very clear to read a predicate such as `x => x < 10` without needing to choose a name for the
free variable, `x`. Using an `_` in place of the only parameter, and eliding the `x =>` which introduces that
parameter, produces more readable (and writable) code, without any ambiguity.

Lambdas which take more than one parameter are also supported through multiple placeholder underscores,
provided the order of the parameters matches the order of their placement in the expression. For example,
```scala
List(3, 5, 7, 11).reduce(_ * _)
```

## Wildcard types

We may sometimes encounter _wildcard types_ in Scala, which are a way of generalizing generic types with one or
more type parameters that is _indeterminate_. In Scala versions before 3, these were a subset of the
_existential types_, though these are no longer a part of Scala's type system.

An indeterminate type parameter is one which is not known at compile time. There are a variety of reasons why a
type parameter may not be known, but there are two sources of such types:

Firstly, the JVM permits us to pattern match a runtime value against its _runtime type_. Runtime types cannot
encode all the features that compile-time types can encode, and—in particular—the type parameters of a value's
type cannot be determined just by looking at the value. So we would not be able to distinguish between a value
of type `Option[Int]` and `Option[String]` by pattern matching. As a way of representing an option of
_something_, the compiler uses `Option[_]`, using the `_` to represent the indeterminate type parameter. The
type is _something_; it must exist, but we don't know what it is.

Secondly, we may need a single unified type to statically represent more than one different type. If we imagine
a list of sets,
```scala
val ints = Set(1, 8, 11)
val chars = Set('m', 't', 'b', 'a')
val xs = List(ints, chars)
```
we could ascribe `xs` a type of `List[Set[_]]` to indicate that every element of the list is a `Set[_]`, but the
elements of those sets are indeterminate. There is an important subtlety in interpretation here: While each
element of our `List[Set[_]]` is a set of indeterminate element type, each `Set[_]` in the list has elements of
an unknown _but consistent_ type: every element in the first `Set[_]` is an `Int` and every element in the
second `Set[_]` is a `Char`.

We could choose to represent our list as a `List[_]`, but this would discard type information about the
`Set[_]`s that may have been useful: we can call `.size` on every element of a `List[Set[_]]` but we cannot do
that on the elements of a `List[_]`.

## Uninitialized values

Sometimes we want to create a field in a class or object, but do not yet want to assign it a value. We can use
an underscore to indicate that its value should not (yet) be initialized.
```scala
var x: String = _
```

This will create a variable, `x`, which we can assign a value to, for example,
```scala
x = "Hello, World!"
```
but whose initial value is not a `String`. This will, in fact, initialize the value to `null`, which we normally
try to avoid, so it's often better to redesign our software to avoid the need for our field to exist without
being initialized.

Note that this only makes sense for fields in classes and objects. Local variables cannot be left uninitialized.

## Numeric spacing

Sometimes, when we work with vary large literal numbers, like `100000000000L` (that's one triillion) it is
useful to group the digits to make them easier to read. So we can write,
```scala
val trillion: Long = 1000_000_000_000
```

The `_` characters within the number behave as if they were not present, except to visually separate the chunks
of digits. The positions of the `_` characters in the number do not need to be in any particular pattern.
`1_00__000_0` is also a valid number, for example.

## Pattern matching

The `_` character also behaves as a wildcard in pattern matching. It will always match _any_ scrutinee, which
makes it useful for disregarding a value because we don't care about it.

```scala
anyValue match
  case head :: _ => head
  case (left, _) => s"left: $left"
  case Some(_)   => "present"
  case _         => "something else"
```

The underscore can also be used, as `$_`, when pattern matching against a string to ignore part of it, like so:
```scala
def isAdmin(email: String) = email match
  case s"admin@$_.com" => true
  case _               => false
```

## Higher-kinded type parameters

When defining a method or class that takes a type parameter, and that type parameter itself should be a type
that normally takes one or more type parameters (like `List` or `Either`), the `_` can be used to indicate that
constraint on the structure of the type parameter, known as its _kind_.

For example, a method `convertTo`, which will convert a `List[Int]` to a different collection type, could be
defined with the signature,
```scala
def convertTo[C[_]](xs: List[Int]): C[Int]
```

This would allow it to be called with, `convertTo[Set](ints)` or `convertTo[Option](ints)` but not,
`convertTo[String](ints)`. That is because the type parameter specification, `C[_]` indicates that the kind (or
structure) of the type specified should itself take a single type parameter, as `List` or `Set` or `Option` do,
but which `String` or `Int` or `Either` (which takes two type parameters) do not.

Note that when calling such a method, types such as `List` which would normally be written with a parameter,
like `List[T]`, should be written without that parameter when the context (i.e. the kind specified at the
definition site) indicates the need for a higher-kinded type of this nature.

While the uses of the underscore in Scala are quite varied, in is invariably used for every occasion where
terse syntax is useful, and there is no _need_ to introduce new identifiers or entities to represent that.
