# Classes

The `object` keyword allows us to create "one-off", or _singleton_, instances of objects with state and methods
(collectively, we will call these _members_), but we often need to create multiple instances of similar objects;
a _class_ of objects.

A _class_ allows us to define a body, similar to an object's body, with the same members, and to create new
instances of it on demand. Let's convert the `BasicLog` object from the previous lesson into a class:

```scala
class BasicLog():
  val writer: FileWriter = FileWriter("/var/log/application.log")
  def record(msg: String): Unit = writer.write(s"$msg\n")
```

We can instantiate, or _construct_, a new `BasicLog` instance just by calling `BasicLog()`. For example,
```scala
lazy val log = BasicLog()
```

This lazy value, with the identifier `log`, is essentially the same as our original object, `BasicLog`. We have
made the value lazy, to mimic the instantiation lifecycle of the `BasicLog` object, but we could also eagerly
instantiate the new `BasicLog` value with:
```scala
val log = BasicLog()
```

Either definition will construct at most one instance of the `BasicLog` class. However, being a class, it is
possible to construct more than one instance, with the same behavior:
```scala
val log = BasicLog()
val reportStream = BasicLog()
```

For many classes, this would be enough, but our particular example includes a `FileWriter` instance encapsulated
in the state of every instance of the `BasicLog` class, which writes to the file `/var/log/application.log`.

Now, either `log` or `reportStream` could use its own instance of `FileWriter` to write to disk, but we would
prefer to have _different_ `BasicLog` instances writing to _different_ files. We can achieve this by
parameterizing the `BasicLog` class with an `id` from which we derive the filename to write to.

```scala
class BasicLog(id: String):
  val writer: FileWriter = FileWriter(s"/var/log/$id.log")
  def record(msg: String): Unit = writer.write(s"$msg\n")
```

And this is a _template_ for creating new objects. It is like a blueprint for the state and methods of an
object, but is incomplete until the parameter, a `String` called `id`, is supplied. It is therefore impossible
to instantiate an object from a template without every parameter being specified.

We can now construct different `BasicLog` instances which log to different files. The parameter, `id`, becomes
part of the state of each `BasicLog` instance, so it's accessible like `val`s defined within the class body, but
unlike `val`s, class parameters are not accessible from _outside_ the class's body.

The signature of the class, `BasicLog(id: String)` in this example, looks and behaves a lot like a method, and
is called a _constructor_ because it _constructs_ a new object instance. Consequencly, parameters such as `id`
are called _constructor parameters_.

We can instantiate a new `BasicLog` instance by calling its constructor, for example:
```scala
val log = BasicLog("app")
```

Scala also permits the `new` keyword to be used when calling a constructor, as was necessary in earlier versions
of Scala, but is no longer required. It is, nevertheless, equivalent to write:
```scala
val log = new BasicLog("app")
```

## Templates and Types

When a class such as `BasicLog` is defined, it introduces _two_ new entities relevant to us as programmers, and
although, in practice, they are usually treated as the same thing, it is useful to have a clear understanding of
the differences.

The two concepts are,
1. a template, invoked by a constructor, defining the creation process and structure for new objects, and,
2. a type representing objects created by that template.

The same name is used for both entities, which is convenient because it is not always useful to distinguish
between them. But by defining the class `BasicLog`, we introduce a constructor called `BasicLog` which
constructs objects conforming to the type also called `BasicLog`. `BasicLog` is introduced as a new identifier
into both the _term_ and the _type_ namespaces.

It is also important not to confuse a class definition and an object definition: Although their bodies look
the same, only the object definition defines a new object; a class definition only defines a template or
blueprint for creating new objects. The term _template_ is not so widely used in the Scala ecosystem, perhaps
because it evokes some developers' bad memories from templates in C++, but it's nevertheless appropriate: the
definition is a partial specification for an object, but potentially with "gaps". In the `BasicLog` example, the
`id` parameter is just such a gap, and to construct a new instance, that gap must be "filled in", that is, the
`id` parameter must be known at the point of construction, when the class's body is executed.

This is an important point when trying to understand the relationship between templates and types. Every
instance of a type, apart from the primitives, must have been constructed from a template, and to construct a
value, the template's parameters must have been fully specified. Looking at this from the other side, given an
instance of a particular type, we know that a choice of parameters must have been made in order to construct that
value, and the value's existence itself serves as evidence of this.

For example, we can reason that, if the method,
```scala
def recordInit(log: BasicLog): Unit =
  log.record("Initializing application...")
```
were called, with a `log` parameter, we would know that somewhere, that instance of `BasicLog` must have been
instantiated, and a choice of `id` parameter must have been made. After all, we expect `log` to log a message to
a file, and that file must be written with a `FileWriter`, which must have been instantiated with a filename,
and our code only ever instantiate a `FileWriter` with a location string provided by an `id` value in its
constructor parameter.

But an interesting point in this example is that we cannot easily recover what that `id` parameter was from just
a `BasicLog` instance. We may access its `writer` state, but the API of `FileWriter` does not expose any methods
for accessing the file (or filename) it is writing to.

Often, this is a deliberate design choice: the object provides an abstraction over an implementation detail, and
as such, we make a choice not to expose that detail, because it _is not_, and _should not be_ important to the
users of the object.

?---?

Consider the following definitions
```scala
class JobRole(title: String, company: String):
  val entity = "job-role"
  val description = s"$title at $company"

val pearCeo = JobRole("CEO", "Pear Inc")
```

# What does the experession `pearCeo.description` evaluate to?
* [ ] `"CEO"`
* [X] `"CEO at Pear Inc"`
* [ ] the expression does not compile
* [ ] the expression throws an exception at runtime

# What does the experession `pearCeo.title` evaluate to?
* [ ] `"CEO"`
* [ ] `"CEO at Pear Inc"`
* [X] the expression does not compile
* [ ] the expression throws an exception at runtime

# What does the experession `JobRole("Analyst", "Quince Inc").title` evaluate to?
* [ ] `"Analyst"`
* [ ] `"Analyst at Quince Inc"`
* [ ] `"job-role"`
* [X] the expression does not compile
* [ ] the expression throws an exception at runtime

Now consider a class whose body contains a `println` statement,
```scala
class Info(msg: String):
  val message = s"[INFO] $msg"
  println(message)

def go() = Info("Hello, World!")
```
and imagine evaluating the following main method:
```scala

@main
def run(): Unit =
  val info = go()
  println(info.message)
  println(go().message)
```

# The `run()` method will cause `[INFO] Hello, World!` to be printed a number of times. How many?
* [ ] one
* [ ] two
* [ ] three
* [X] four
* [ ] five

# How many different instances of the `Info` class are constructed when executing the `run()` method?
* [ ] one
* [X] two
* [ ] three
* [ ] four
* [ ] five