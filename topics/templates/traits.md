## Generalizing Inheritance

Scala provides another kind of template, similar to a class, but trading some constraints for some additional
capabilities. Like a class, a _trait_ defines a body with methods, state and other members. A trait may also
define a constructor, but unlike a class, cannot be instantiated; not _directly_, at least. This compromise has
a benefit, however: a class or object may extend—that is, inherit from—more than one trait, and the object or
instances of the class will share the union of all the properties of all the traits it inherits.

The rules for combining multiple traits in the same class are quite detailed, but are nevertheless logical.

Imagine that we wanted to add some additional functionality to our `Log` class. Specifically, we would like to
provide a method which times how long (in milliseconds) it takes to perform an operation, and gives us a
`String` log message telling us the elapsed time. We can define that method in a trait.

```scala
trait Timer:
  def time(msg: String)(action: => Unit): String =
    val t0 = System.currentTimeMillis
    action
    val time = System.currentTimeMillis - t0
    s"${msg} (${time}ms)"
```

With this definition, it is now possible to construct a class which _inherits_ the `time` method, using the
`extends` keyword in the class definition, like this:
```scala
class BasicLog(id: String) extends Timer:
  val writer: FileWriter = FileWriter(s"/var/log/$id.log")
  def record(msg: String): Unit = writer.write(s"$msg\n")
```

This now means that calling the `BasicLog` constructor, for example, `BasicLog("app")`, will construct an
object which not only has the value `writer` and the method `record`, but also the method `time`. We sometimes
use the terminology _mixed-in_ to describe the construction of a template which combines, or _mixes in_ other
traits containing other members. We could use both methods like this:

```scala
val log = BasicLog("app")
val msg = log.time("Check file length") {
  File("example.txt").length
}

log.record(msg)
```

Running this code will log a message to the file `/var/log/app.log` showing the time taken to check the
length of the file, (probably a very short time on modern hardware).

If we were to define other traits, such as `Closable` or `Pausable` which define their own methods (but let's
not worry about their implementations for now), we could define the class `BasicLog` to extend `Timer`,
`Closable` and `Pausable`.
```scala
class BasicLog(id: String) extends Timer, Closable, Pausable
```

It's common to name traits after their capabilities (though some people discourage the practice, as it leads to
a proliferation of entities all with names ending in `-able`), and we might expect `Closable` to define a method
`close()`, and `Pausable` a method `pause()`. But traits' names are entirely our choice.

## Abstract methods

Looking back at our example using `Timer`, written here in equivalent, but slightly shorter form,
```scala
val log = BasicLog("app")
val msg = log.time("Check file length")(File("example.txt").length)
log.record(msg)
```
a couple of flaws may be apparent with the design of the `time` method. Firstly, we receive a `String` in
response to calling the `time` method, and have to pass the value to a second method of `log`, `record`, to
record the message in the log, when a single command would be preferable. Secondly, by returning the `String`
from the `time` method, we have no way to access the result of the operation we are timing!

Let's try to fix this by changing the definition of `Timer` to call the `record` method with the message string,
and to return the value it has calculated.

```scala
trait Timer:
  def time[T](msg: String)(action: => T): T =
    val t0 = System.currentTimeMillis
    val result = action
    val time = System.currentTimeMillis - t0
    record(s"${msg} (${time}ms)")
    
    result
```

The last line of the definition of `time` now returns the result of performing the `action`, whose return type
is `T`, an abstract type, so it will depend on the type of the `action` parameter.

This looks better, but will not compile. The reason is that we attempt to call a method called `record` in the
body of `time`, and the Scala compiler has no knowledge of this, or proof that it exists. We certainly intend
for `Timer` to be mixed in to a class `BasicLog`, which defines a method called `record`, but that is just one
potential usage, and for generality, we don't want to assume that is the only possible usage of our trait.

One way or another, we need to provide the compiler with an explanation for, or a declaration of, what the call
to `record` _means_ and the evidence that it can be used in the way we are using it: by passing it a `String`.
One possibility would be to include the definition of `record` in the body of the `Timer` trait, but at the time
we define the `Timer` trait, we don't _know_ how `record` should be defined!

The solution is to write an _abstract_ method definition. This looks identical any other method definition,
except that the `=` sign, and the method body which would usually follow it, are completely omitted; so all that
remains is the _method signature_.

```scala
def record(msg: String): Unit
```

This can be thought as both a specification for the `record` method—that it takes a single parameter, a
`String` and returns the `Unit` value—and also a _promise_ that any concrete implementation of a `Timer` _must_
define a `record` method, with a fully-implemented body.

The full definition of `Timer` looks like this:
```scala
trait Timer:
  def record(msg: String): Unit

  def time[T](msg: String)(action: => T): T =
    val t0 = System.currentTimeMillis
    val result = action
    val time = System.currentTimeMillis - t0
    record(s"${msg} (${time}ms)")
    
    result
```

When we instantiate any new object, there can be no abstract method definitions. And we can rely on the Scala
compiler to tell us if we attempt to instantiate an object without providing an implementation for every
declared method.

If, for example we attempted to declare a singleton object extending `Timer`, compilation would fail.

```scala
object SimpleTimer extends Timer
```

This can be solved quite easily by following the advice in the error message. It would, for example, be
sufficient for the `record` method to print its message to standard output,
```scala
object SimpleTimer extends Timer:
  def record(msg: String): Unit = println(msg)
```
which would allow it to be used like this,
```scala
SimpleTimer.time("Check the file length") {
  File("example.txt").length
}
```
returning the length of the file, and printing the time taken in doing so to standard output as a side-effect.

Our solution to the absence of an implementation to the `record` method was to directly provide the
implementation, but concrete implementations of abstract methods may also be provided through inheritance. We
could define a trait, `StdoutRecorder` which provides a concrete `record` implementation,
```scala
trait StdoutRecorder:
  def record(msg: String): Unit = println(msg)
```
and redefine our `SimpleTimer` object in terms of `StdoutRecorder` and `Timer`:
```scala
object SimpleTimer extends Timer, StdoutRecorder
```

## Linearization Order

The order of the traits does not matter. Each trait that is mixed in to a template may _provide_ any number of
method implementations, and may _declare_ any number of abstract methods, so a trait may both satisfy a
requirement by providing a method definition, whilst introducing a new requirement which must subsequently be
satisfied.

Consider a `FileRecorder` trait which provides an alternative implementation of `record`,
```scala
trait FileRecorder:
  def writer: FileWriter
  def record(msg: String): Unit = writer.write(s"$msg\n")
```

We could use this to redefine `BasicLog` as,
```scala
class BasicLog(id: String) extends Timer, FileRecorder:
  val writer: FileWriter = FileWriter(s"/var/log/$id.log")
```

Dissecting this, we are defining a new `BasicLog` class, which inherits a `time` method from `Timer`, but
requires a `record` method, which we inherit from the `FileRecorder` trait, which requires a `writer`
implementation, which we provide directly in the body of `BasicLog`. Ultimately, there are no abstract methods
remaining.

But what if there were? It would be impossible to create an instance of the class, so Scala requires that any
_class_ (not _trait_) that has unimplemented abstract methods be annotated with the `abstract` modifier, so
we could choose to implement `writer` later (in a subclass), and define `BasicLog` as,
```scala
abstract class BasicLog(id: String) extends Timer, FileRecorder
```

## A Warning

Traits provide a very powerful system for defining and satisfying constraints, in the form of methods, and the
Scala compiler can very capably provide guarantees that those constraints are satisfied, with helpful guidance
on satisfying them. While powerful, overuse of these capabilities can lead to unwieldy code which is difficult
to modify.

A common trap when using traits in this way is commonly known as the _cake pattern_, so-called because the
body of a large class or object may be "sliced" up into many traits, each with its own abstract and concrete
methods. Unfortunately this style makes it too easy to create subtle dependencies, or strong couplings, between
traits, and this somewhat defeats their purpose.

?---?

# Given the following trait definitions,

```scala
trait Publication(title: String)
trait Novel(title: String) extends Publication
trait Inventory(copies: Int) extends Publication
```
select every object definition which will compile without error.

* [X] `object JaneEyre extends Novel("Jane Eyre"), Publication("Jane Eyre"), Inventory(1)`
* [ ] `object WarAndPeace extends Novel("War and Peace")`
* [ ] `object MobyDick extends Novel("Moby Dick"), Inventory(10)`
* [ ] `object Ulysses extends Publication, Novel("Ulysses")`
* [X] `object Middlemarch extends Novel("Middlemarch"), Publication("Middlemarch")`
* [ ] `object Catch22 extends Novel("Catch-22"), Publication, Inventory(0)`

# The following code will not compile:

```scala
val Origin = Point(0, 0)

trait Position(point: Point):
  def center: Point = point

trait Shape extends Position:
  def inside(point: Point): Boolean
  def area: Double

trait Circle(radius: Double) extends Shape:
  def area: Double = math.Pi*radius*radius
  def inside(point: Point): Boolean = point.distanceTo(center) < radius

object Dot extends Circle(1.0)
```

Which of the following solutions would avoid the compile error?

* [ ] add a method, `def center: Point = Origin`, to the body of `object Dot`
* [ ] change the definition of `def center` in `trait Position` to `def center: Point = Origin`
* [ ] remove the method `def center` and the parameter block, `(point: Point)` from `trait Position`
* [ ] remove `extends Position` from the definition of `trait Shape`
* [X] change the definition of `object Dot` to `object Dot extends Circle(1.0), Position(Origin)`

