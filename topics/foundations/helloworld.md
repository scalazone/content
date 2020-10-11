# A first program

It is a tradition to start programming by writing a program called "Hello, World!" which does nothing more than
print the words,
```
Hello, World!
```
on the screen, before exiting.

In Scala, we can create just such a program
```scala
@main
def hello() = println("Hello, World!")
```

This is an example of a complete _program_. Although a program can mean different things in different contexts,
when we refer to a program we usually mean a standalone application that is launched by the operating system,
runs for some time, and then exits.

Other times, the term "program" might be used more generally to refer to other forms of software that may be
executed. These may include:
- a script in a web browser written using [Scala.js](https://www.scala-js.org/)
- a "servlet" which runs inside a web server
- a Scala compiler plugin which runs during compilation

These are all kinds of software that we can write, and may be executed to perform certain actions within some
context. Each will have an _entry point_: a method which will be executed first, and from which point all
subsequent execution will follow. This also implies that what happens _before_ the entry point will be opaque:
we generally don't know (and shouldn't need to know) the exact details of _how_ the entry point is invoked.

In the case of our "Hello, World!" example, that entry point is the method, `hello()`, which is a _main method_,
as indicated by the `@main` annotation. Prefixing a top-level method (a method defined outside a class, trait or
object) with `@main` marks it as a program's entry point, and makes it accessible to invoked directly by the
operating system with the `scala` command.

That command, typed into the console, will look like this:
```sh
scala -cp bin hello
```

