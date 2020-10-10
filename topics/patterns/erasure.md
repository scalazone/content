# Erasure

## Abstract types

Another limitation of the Java runtime is that we cannot match against types unless we know, concretely, what
they are. Imagine, for example, the following method which we would like to return a `Some[S]`, if the
`Any`-typed value is an instance of the type `S`.
```scala
def asType[S](value: Any): Option[S] =
  value match
    case s: S => Some(s)
    case _    => None
```

There would be convenient, but it cannot work in its current form. Remember that a pattern match must compile
to bytecode, and a type test, such as that in `case s: S`, must compile to the bytecode `instanceof`
instruction, which checks a value against a class type, known concretely and statically.

And in this example, we only know `S` abstractly, not concretely, and so it is impossible to generate
bytecode to perform the `instanceof` test against an abstract type, because the could would need to be different
for different calls to `asType`.

Thankfully, though, there are a couple of solutions! We know that it's not possible to write a type test against
an abstract type, but if we could instead compile the `instanceof` type test elsewhere—somewhere where the type
we want to match against _is_ known concretely—and pass it in to the pattern match, we could use the type test
we pass in to decide whether to take one `case` of the match, or not.

The mechanism for doing this uses a typeclass called `ClassTag` in the `scala.reflect` package. An instance of
`ClassTag[T]` will provide a method that can test if a value is an instance of type `T` or not, and the compiler
can generate given instances of `ClassTag[T]` automatically for any type `T` that is known concretely. So by
demanding a `ClassTag` context bound on the type `S` in the signature of our `asType` method, we give the
compiler the context it needs to be able to generate bytecode to test against the abstract type `S`. Just having
a given instance of `ClassTag[S]` in scope is sufficient for the compiler to compile the pattern match against
an abstract type.

Here is the rewritten method:
```scala
def asType[S: ClassTag](value: Any): Option[S] =
  value match
    case s: S => Some(s)
    case _    => None
```

## Inlining

For a method like `asType`, there is an alternative solution which may work in many cases. Without the
`ClassTag` context, we can make `asType` an _inline_ method, like so,
```scala
inline def asType[S](value: Any): Option[S] =
  value match
    case s: S => Some(s)
    case _    => None
```
and then, an invocation of `asType` such as,
```scala
def printIfString(value: Any): Unit =
  asType[String](value).foreach(println)
```
would expand to,
```scala
def printIfString(value: Any): Unit = {
  value match
    case s: String => Some(s)
    case _         => None
}.foreach(println)
```

The process of inlining substitutes the known type, `String`, for the abstract type `S`, and once expanded
in-place, there no longer remain any pattern matches against abstract types.

But this will not always be sufficient. Imagine that we would like to generalize `printIfString` to a method
which will print instances of any specified type, `printIfType[T]`,
```scala
def printIfType[T](value: Any): Unit =
  asType[T](value).foreach(println)
```

Inlining would work exactly as before, except the expanded form would still contain a match against an abstract
type, `T`, and the compiler would still be unable to generate bytecode to test it.

But, in fact, the solution is the same: we must either require a `ClassType[T]` as context, or inline the method
`printIfType`. Inlining may be a cleaner solution for smaller method bodies, particularly if performance is
important, but inlining large bodies may not scale well. With both solutions, however, we must trace from the
type match on the abstract type, back through every call site, to an invocation when the type was known
statically and concretely.

### Pattern matching on arrays

While `Array` instances may appear to behave like other collection types, such as `List` and `Vector`, they are
special in that they have a native representation on the JVM. An `Array[String]` is represented as
`[Ljava.lang.String` and an `Array[Array[Option[String]]]]` as `[[Lscala.Option`. The `[` indicates that the
type is erased to an `Array` type (and may be repeated as necessary for nested `Array`s), while the name after
the `[`s is the normal erased type of each element in the `Array`. Note that we still lose the `String`
parameter type to `Option` due to erasure, but we can disambiguate between different types of `Array`, and
their depth of nesting.

?---?

