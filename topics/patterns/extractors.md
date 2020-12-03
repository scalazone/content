## Introducing Extractors

Every case class or enum we define may be used in a pattern. But the same is not true by default for all types.
It is possible for case classes and enums because, by design, their signatures should be what defines them: the
notion of equality on a case class is defined in terms of equality on its parameters, as is its `hashCode`
implementation. And, given the parameters of a case class or enum, we can construct an instance, and from an
instance we can extract the parameters that were used to construct it.

This is the motivation for patterns to support case classes. The mechanism by which case classes signatures can
be used in patterns is a more general facility in Scala, called _pattern extractors_ or just _extractors_.

An extractor allows an object to be used to _deconstruct_ a value into some component parts. In the case of a
case class, the object is the case class's companion object, and the component parts are its constructor
parameters, but there is no strict requirement this be the case: any object may be an extractor, and it can
deconstruct into any components.

## The `unapply` method

What makes an object an extractor is the presence of a member method called `unapply` with an appropriate
signature. We will look later at the variety of different signatures that are suitable for the `unapply` method,
but we will typically start with a simple example: an extractor called `Integral` which will extract an `Int`
from a `Double` if and only if the `Double` value is a whole number. Here's how we want to use it:
```scala
def readInt(input: Double): Int = input match
  case Integral(int) => int
  case _             => 0
```

Against the `input` scrutinee, which is a `Double`, we will attempt to extract an `Int`. When interpreting the
pattern, Scala will resolve `Integral` to an object, and check for an `unapply` method, and that is what we must
now implement.

The easiest way to think about how to write such a method is to keep in mind exactly what the `unapply` method
must do:
- it takes a `Double` as input
- it may return an `Int` if the input represents an integral value
- or it may not, if the input does not

A signature which meets those requirements is,
```scala
def unapply(input: Double): Option[Int]
```
and we can provide the full implementation in an `Integral` object like so:
```scala
object Integral:
  def unapply(input: String): Option[Int] =
    if input == input.floor then Some(input.toInt) else None
```

## Return Type

Having this definition in scope is enough to allow us to use it in a pattern. The return value of `unapply` will
be either `Some` of an integer in the case where we want the extractor to match, or `None` when we do not wish
it to match.

What can be most confusing when writing an `unapply` method is correctly choosing the parameter and return
type of the method. In the pattern we _read_ `Integral(int)` which _looks_ like it is applying a function to an
`Int` and the return type of the entire "expression" is `Double`... but this is a mistake because it is not an
expression, it is a pattern, and we have to think about it _backwards_. The best approach is usually to remind
ourselves that the `unapply` method must take an instance of the _scrutinee_'s type, and will produce an
instance—optionally—of the component or components we want to extract.

The example above is for a single-parameter extractor, but it's also possible to extract multiple parameters,
as is the case with multi-parameter case classes. Thinking again about the signature of the `unapply` method,
we need to take a single parameter as input, but—optionally—return multiple parameters. We can achieve this by
returning an `Option` of a tuple type, instead of an `Option` of a single value.

Imagine, for example, that we would like to extract the bytes from an IP address, provided as a `String`. Here
is an example of how such an extractor might be used:
```scala
def local(ip: String): Boolean = ip match
  case Ip(192, 168, _, _) => true
  case Ip(10, _, _, _)    => true
  case Ip(172, x, _, _)   => x >= 16 && x < 32
  case _                  => false
```

Note that bytes on the JVM are signed, whereas IP addresses use unsigned bytes, so we will simply use `Int`s
instead of `Byte`s for convenience. A better implementation could use an opaque type based on `Byte`.

## Defining An Extractor

Our extractor would look like this:
```scala
object Ip:
  def unapply(addr: String): Option[(Int, Int, Int, Int)] =
    addr.split("\.").map(_.toInt) match
      case Array(b1, b2, b3, b4) => Some((b1, b2, b3, b4))
      case _                     => None
```

In order to extract into a four-parameter `Ip` pattern, we must return an `Option` of a four-tuple.

## Binary Extractors

Scala also supports extractors which take an empty parameter list, and dont extract any new values. For example,
```scala
def describe(number: Int): String =
  number match
    case Even() => "even"
    case _      => "odd"
```

Given that no value needs to be returned, the return type of the `unapply` method can be simplified to
`Boolean`: we return `true` if the number should match, or `false` if it should not, like so:
```scala
object Even:
  def unapply(value: Int): Boolean = value%2 == 0
```

The definition of an `unapply` method hints at a limitation for defining extractors: unlike a method application which
can have multiple overloaded implementations, disambiguated by the number and type of its parameters, the input to
an `unapply` method is always a single parameter (the scrutinee type) which is not selected on the basis of its return
type, only by the _static_ type of the scrutinee. This means that it's not possible to define alternative extractors
with different arities, and have the compiler choose a different one based on the number of parameters that appear in
the pattern.

But there is no restriction on defining multiple `unapply` methods for different scrutinee types. We could reasonably
define the following extractor, which extracts hours and minutes from a time given in minutes, whereby giving the time
as a `Double` will use an extractor which also extracts a number of seconds.
```scala
object Time:
  def unapply(mins: Int): Option[(Int, Int)] =
    Some((value/60, value%60))
  
  def unapply(time: Double): Option[(Int, Int, Int)] =
    val hours = (time/60).toInt
    val mins = (value - hours*60).toInt
    val secs = (time - hours*60 - minutes)*60

    Some((hours, mins, secs))
```

We can then use it as,
```scala
(time: Int) match
  case Time(h, m) => ...
```
or,
```scala
(time: Double) match
  case Time(h, m, s) => ...
```
but not as,
```scala
(time: AnyVal) match
  case Time(h, m)    => ...
  case Time(h, m, s) => ...
```
because the type of `time` is not statically known.

?---?
