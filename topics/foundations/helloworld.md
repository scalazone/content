## Hello, World!

It is a tradition to start programming by writing a program called "Hello, World!" which does nothing more than
print the words,
```
Hello, World!
```
on the screen, before exiting.

In Scala, we can create just such a program with the following code:
```scala
@main def hello() = println("Hello, World!")
```

## Compiling

We can put this into a plain text file called `hello.scala`, and compile it by running the Scala compiler.

This requires that the correct version of `dotc` is installed. We can check this by running,
```sh
dotc -version
```
which should display a message like the following:
```
Dotty compiler version 0.27.0-RC1 -- Copyright 2002-2020, LAMP/EPFL
```

We can compile our source file by running,
```sh
dotc hello.scala
```

If everything worked correctly, this will create some new files in the same directory, with names ending in
`.class`, and containing _compiled Java bytecode_. The `dotc` command will not print any output if the
compilation was successful, but error messages will be displayed if compilation fails.

## Compilation Errors

If we try to compile a slightly different program,
```scala
@main def hello() = println "Hello, World!"
```
which forgets to include the parentheses (`(`, `)`) around `"Hello, World!`, then we should see 
_compile errors_ (or, _compilation errors_) similar to this one:
```
-- Error: hello.scala:1:28 -----------------------------------------------------
1 |@main def hello() = println "Hello, World!"
  |                            ^
  |                        end of statement expected but string literal found
```

This is one error, which occurs on line 1 (the only line in our short program!), at character 28 of that line.
To make it easier to see where that is, the Scala compiler will print out the error line, with a blank line
beneath it containing one or more caret characters (`^`), pointing to the error position.

The message, `end of statement expected but string literal found`, tries to indicate the problem: that a string
was found in the source code, in an unexpected position. This might not be the clearest explanation of the
problem, but it should help: we need to put parentheses around the string literal in order for it to be
_applied_ to the method `println`. Simply juxtaposing the string next to the method name is not valid syntax!

## Programs

This is an example of a complete _program_. Although a program can mean different things in different contexts,
when we refer to a "program" we usually mean a standalone application that is launched by the operating system,
runs for some time, and then (usually) exits.

The term "program" might also be used more generally to refer to other forms of software that may be executed.
These could include:
- a script in a web browser written using [Scala.js](https://www.scala-js.org/)
- a "servlet" which runs inside a web server
- a Scala compiler plugin which runs inside the Scala compiler during compilation

These are all kinds of software that we can write, and may be executed to perform certain actions within some
context. Each will have an _entry point_: a method which will be executed first, and from which point all
subsequent execution will follow. This also implies that what happens _before_ the entry point will be opaque:
we generally don't know (and shouldn't need to know) the exact details of _how_ the entry point is invoked.

In the case of our "Hello, World!" example, that entry point is the method, `hello()`, which is a _main method_,
as indicated by the `@main` annotation. Prefixing a _top-level_ method (a method defined outside a class, trait 
or object) with the special annotation, `@main`, marks it as a program's entry point, and makes it accessible to
be invoked directly by the operating system, typically through the shell with the `dotr` command.

In general, other methods we write can only be called from expressions we write in Scala, and only _main_
methods can be invoked externally.

To run the program, we can invoke the following command in the console,
```sh
dotr hello
```
and we should see the output:
```
Hello, World!
```

These commands, `dotc hello.scala` and `dotr hello` are artificially simple, because our source file,
`hello.scala` is in the current directory, which we also use as an _output directory_. And that allows us to
invoke the method we have just invoked, `hello`, without any additional parameters. We also benefit from 
requiring no dependencies for our tiny program to run.

In reality, very few programs are so simple, and usually different _source_ and _output_ directories would be
used, along with a set of dependencies, defined using a _classpath_. The `dotc` and `dotr` commands support
a variety of parameters for specifying these details, but it is more usual to give this task to a _build tool_.

## Anatomy of Hello World

Our simple program,
```scala
@main def hello() = println("Hello, World!")
```
is nothing more than a method definition, indicated by the `def` keyword. The name of the method is `hello`, and
the empty parentheses after its name are where we could define its parameters, if it had any. The implementation
of the `hello` method is on the right-hand side of the `=` sign, and is a simple statement which invokes the
method `println`, pronounced "print line", passing it the string `Hello, World!`, enclosed in quotes as its only
parameter. The `println` method call is what produces output on the console.

And finally, as previously mentioned, `@main` is an _annotation_ which adds some "metadata" to the definition;
specifically, that it is a main method. Annotations are a versatile feature of Scala, but their use is
relatively uncommon.

So, we have created our first program. It's not particularly interesting, but now we can start building upon it
incrementally!

?---?

# The following program contains at least one mistake.

```scala
def factorial(x: Int) =
  if x == 0 then 1 else x * factorial(x)
```

Try to compile the program and read the error message to understand the problem that is preventing successful
compilation. Don't worry, you are not expected to understand the program or the error, only to identify what the
compiler is telling you!

- [ ] compilation fails because the `@main` annotation is missing
- [ ] compilation fails because the method is not called `main`
- [X] compilation fails because the method needs a return type
- [ ] compilation fails because the program never terminates

# Try to compile and run the following program

```scala
def go(x: Int): Int =
  if x == 0 then 1 else x * go(x/2)

@main def calculate() = go(24)
```

What happens?

 - [ ] An error is produced during compilation
 - [ ] The code compiles, but no runnable main method is produced
 - [ ] The code compiles, but fails with a runtime error
 - [X] The code compiles and runs, but prints no output
 - [ ] The code compiles, runs and prints `5184` in the console
