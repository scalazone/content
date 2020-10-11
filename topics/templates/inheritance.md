# Inheritance

Often we want to define a class which has all of the state and methods of another class, but provides additional
functionality; extra methods and/or state. Scala provides this through _inheritance_, and establishes a
_subtyping relationship_ between the new template and the template in inherits from.

Here is the `BasicLog` class from earlier in this topic:

```scala
class BasicLog(id: String):
  val writer: FileWriter = FileWriter(s"/var/log/$id.log")
  def record(msg: String): Unit = writer.write(s"$msg\n")
```

Imagine that, in addition to the `record` method in our `BasicLog` class, we wish to provide the ability to log
messages marked with a level: `debug`, `info`, `warn` or `error`. These will be the names of the additional
methods. Here is a possible implementation of that class, called `Log`:

```scala
class Log(id: String) extends BasicLog(id):
  def debug(msg: String): Unit = record(s"[DEBUG] $msg")
  def info(msg: String): Unit = record(s"[INFO]  $msg")
  def warn(msg: String): Unit = record(s"[WARN]  $msg")
  def error(msg: String): Unit = record(s"[ERROR] $msg")
```

We declare that our new `Log` class _extends_ the `BasicLog` class; `Log` is now a _subclass_ of `BasicLog`.
This requires, first of all, that the `BasicLog` constructor have its `id` parameter specified. Remember we are
defining a new template from an existing template, and the `BasicLog` template still has the same unknowns which
must be specified for a new instance of that template to be constructed. Here, we specify that the `id`
parameter that `BasicLog` requires will be fulfilled with an `id` parameter that will be passed in to `Log`'s
constructor. In a sense, the `id` parameter is just as much an unknown for `Log` as it is for `BasicLog`, and we
delegate it from one template definition to the next.

The parameter `id` from `BasicLog` is not visible in `Log`. We used the same name for the `id` parameter in
`Log` too—and it's a sensible choice because they represent the same value—but we didn't have to. It would be
acceptable to write, instead,
```scala
class Log(logId: String) extends BasicLog(logId)
```

An alternative implementation of `Log` could have specified a fixed value for `BasicLog`'s `id` parameter. This
would have changed `Log`s signature to `Log()`, while every instance of `Log` would have been instantiated with
the same `id` parameter, for example, `"application"`:

```scala
class Log() extends BasicLog("application")
```

Note also that our implementations of `debug`, `info`, `warn` and `error` all call the `record` method, which
was defined in `BasicLog`. This, and any other methods and state that was defined in `BasicLog` (for example,
`writer`) is automatically available to use, without a prefix, in subclasses. So our new `Log` class is very
much defined in terms of `BasicLog`; a class may refer to members in its _superclass_, and all members, whether
they originated in the class or one of its superclasses, can be accessed (by default—there are ways to hide
them which we will see later) from within the body of that class, or by dereferencing an instance of the class.

Constructing a new instance of any class requires executing its body, that is, instantiating all the `val`s and
`var`s, and any code in the body of the class. Executing the body of a class is a necessary step in the
construction of a value. It may make perform operations on the fields of the object to ensure that it is in a
consistent state when it is constructed, or it may perform actions which "register" the new instance in global
state as it is being created (though there are often better ways of achieving this goal).

For a class which inherits from another, this means executing the bodies of each class, in the correct order.
And as each class may have its own superclass, instantiating a class will naturally execute the body of each in
turn. The body of a superclass will always be executed before the class itself, so by defining an inheritance
relationship with the `extends` keyword, we define not only the members to inherit into our new class, but also
the class bodies that must be executed prior to the body of our new class.

The easiest way to demonstrate this is to add some code to the class bodies which makes the execution order
clear. Let's define `BasicLog` and `Log` as follows,
```scala
class BasicLog(id: String):
  println(s"Initializing BasicLog with id=$id")
  val writer = FileWriter(s"/var/log/$id.log")
  def record(message: String): Unit = writer.write(s"$message\n")

class Log(id: String) extends BasicLog(id):
  println("Initializing Log with id=$id")
  def debug(msg: String): Unit = record(s"[DEBUG] $msg")
  def info(msg: String): Unit = record(s"[INFO]  $msg")
  def warn(msg: String): Unit = record(s"[WARN]  $msg")
  def error(msg: String): Unit = record(s"[ERROR] $msg")
```

When we construct a new instance of `Log` with `Log("application")`, the output we will see is,
```
Initializing BasicLog with id=application
Initializing Log with id=application
```
which should confirm the body of `BasicLog` is executed before the body of `Log`.

In much the same way that defining the `BasicLog` template introduced a new type, called `BasicLog`, by defining
`Log` we introduce a new type, called `Log`. These types act as representations of the properties that all
instances of `BasicLog` and `Log` will have. Some examples of these properties are,
- we can access the `writer` value on an instance of `BasicLog`, with the type `FileWriter`
- we can call the method `info` on an instance of `Log`, passing it a `String`, and it will return the `Unit`
  value

The Scala compiler uses properties such as these to decide whether it is safe to execute code, such as,
```scala
value.info("Hello, World!")
```

If `value` is known to conform to the type `Log`, then this is provably a safe operation, because the `Log` type
has the property that the method `info` can be called on it, passing a `String` as a parameter. If `value` were
instead known only to conform to the `BasicLog` type, the compiler could not prove the invocation safe; it would
be considered a compile error.

The inheritance relationship between a class and its superclass confers a subtyping relationship between the
subclass type and its superclass type. We can say that `Log` is a _subtype_ of `BasicLog`. What that means is
that any property that is provable about an instance of `BasicLog` will also be provable about an instance of
`Log`. Therefore, if we can prove that we can access the `writer` value of a `BasicLog`, and we know that `Log`
is a subtype of `BasicLog`, then we can prove that we can access the `writer` value of a `Log` too. An instance
of a class has all the properties of its superclasses.

?---?
Consider the following code:
```scala
class Animal(name: String):
  val id: String = name.toUpperCase+"-001"

class Sheep(name: String) extends Animal("Sheep"):
  val description: String = id

val sheep = Sheep("Aries")
```
# What is the result of `println(sheep.name)`?
 * [ ] prints `"Sheep"`
 * [ ] prints `"Aries"`
 * [ ] prints `"SHEEP-001"`
 * [ ] prints `"ARIES-001"`
 * [X] does not compile

 # What is the result of `println(sheep.description)`?
 * [ ] prints `"Sheep"`
 * [ ] prints `"Aries"`
 * [X] prints `"SHEEP-001"`
 * [ ] prints `"ARIES-001"`
 * [ ] does not compile
 
 # What is the result of `println(sheep.id)`?
 * [ ] prints `"Sheep"`
 * [ ] prints `"Aries"`
 * [X] prints `"SHEEP-001"`
 * [ ] prints `"ARIES-001"`
 * [ ] does not compile

 Consider the following code:
 ```scala
var counter = 1

class Parent(n: Int):
  counter += n

class Child(n) extends Parent(n + 1):
  counter += n

Child(2)
```
# What is the value of `counter` after running this code?
 * [ ] 1
 * [ ] 3
 * [ ] 4
 * [ ] 5
 * [X] 6
