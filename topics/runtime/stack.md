## Tracking Execution

A program running in the JVM will use a _stack_ to track where, within a potentially-large program, execution is
currently happening. A stack is a _first-in last-out_ (FILO) data structure, so called because it behaves like a
stack of books on a table: we can add to the pile, and it gets higher, but we can only take a book from the top,
not from the bottom (we might knock the stack over!) or from an arbitrary point in the middle.

The stack only has two operations, called _push_ and _pop_, which add a value (a number, character, boolean
value, or object reference) to the top of the stack, and get the value off the top of the stack (removing it in
the process), respectively. We never write Scala code to manipulate the stack directly, but the Java bytecode
which is produced during compilation does.

The elements of a stack are called _frames_ and can contain a variety of different kinds of data: primitive
values like booleans, characters, integral numbers and floating-point numbers, and references to objects on the
heap. But most crucial to tracking the current position within a program is the stack's ability to store
pointers to the position within the code at which execution should continue, after a particular method has
completed.

We can think of the structure of bytecode as analogous, at a low-level, to the Scala code we write, and being
composable as parameterized methods; where methods can call other methods, once, many times or never. However,
ultimately, those methods must be linearized in time. So instead of calling one method from another, and then
"going back" to the first method, execution must always proceed onwards. We can think of it as a continual
stream of bytes, each one instructing the JVM what to do next, with pointers on the stack used to direct
execution to the next instruction.

## Operating with the Stack

When execution reaches the end of a method, it expects to find, at the top of the stack, a pointer to the next
bytecode instruction to execute. And crucially, that pointer is there simply because the JVM placed it there
when as method was invoked. And while, over the course of executing any method, the stack may grow and shrink
multiple times, as other methods are called, JVM bytecode is guaranteed never to change the total number of
frames on the stack over the course of executing a method, except in the (very common) case where a method
returns a value, in which case that value will be left on the top of the stack. However, that is exactly what
the method was expected to do, based on its definition, and the bytecode that is generated during compilation
will carefully manipulate the stack to ensure that when execution continues after calling another method, the
changes that method makes to the stack (i.e. leaving a return value at the top of the stack) will be expected
by the method which initiated the method call, and consequently used.

An method, when invoked, may also expect to find certain values at the top of the stack, for it to use in its
execution. These are analogous to the _parameters_ to the method, and the method's bytecode will expect them to
be present on the stack whenever it is called. Hence, any bytecode which calls a method must first ensure that
the values representing the method's parameters are at the top of the stack.

## A Worked Example

Here is an example of a simple method which calls a `factorial` method (whose implementation is irrelevant to
us).

```scala
def calc: Int = add(factorial(3), factorial(4))
```

The steps the JVM would go through to interpret this would be as follows:
1. push a pointer back to the current position onto the stack
2. push the integer `3` on the top of the stack
3. call the `factorial` method
  1. pop the parameter from the top of the stack
  2. do the factorial calculation somehow, which produces the integer `6`
  3. pop the return pointer from the stack
  4. push the integer `6` onto the stack
  5. follow the pointer, and continue execution there
4. push a pointer back to the current position onto the stack
5. push the integer `4` onto the top of the stack
6. call the `factorial` method (details omitted) which will leave the integer `24` at the top of the stack
7. call the `add` method (noting that `24` is at the top of the stack, and `6` is immediately beneath it)
8. with the integer `30` now on the top of the stack, we are done

We can see here that the stack contains a mixture of execution pointers, and data (in our case, integers),
sometimes serving as parameters, and other times as return values (which can become parameters). By virtue of
careful manipulation of the stack, this very short program can move back and forth between methods, exchanging
data, and performing calculations.

The low-level details of this operations like this may be an intriguing insight into the inner workings of the
JVM, but we rarely need to think about them in this level of detail. That is the challenge for compiler
developers.

But we should be aware of what the stack contains as a direct consequence of its use for tracking method calls:
at any time during execution, the frames within a stack contain pointers, in the order that they were called, to
all the methods that were invoked from the initial entry into our application, to our current position. This
living data structure will contain the sequence of method calls that were invoked to get to our current
position in the code. This turns out to be very useful information when trying to debug our software.

## Exceptions

When a method normally runs, it may modify some values in memory, or return a value. Though it is not always
possible to do that. There is nothing to stop us calling the `factorial` method we used above with a parameter
of `-1`. The definition of the type `Int`, which is `factorial`'s parameter type, allows negative numbers,
but the factorial function is not defined for negative values. How should we handle this?

One possibility is to throw an exception.

```scala
def factorial(n: Int): Int =
  if n < 1 then throw Exception("Parameter is non-positive")
  else if n == 1 then 1
  else n*factorial(n - 1)
```

This allows us to abort execution of the method, and exit to the method which called ours. But, the way the
stack works in Java, whenever a method exits _exceptionally_ there can be no value left at the top of the stack,
because we have just failed to create that return value. Instead, a new `Exception` object is constructed,
containing a representation of the stack, and the class definitions are checked (remember, every method
definition lives within some class) to find the most recent method called that is able to handle the particular
exception thrown.

This way, the `Exception` object that is constructed will contain a representation of the stack in the state it
was in when the exception was thrown, and that `Exception` object will effectively be a parameter to the most
immediate matching handler defined within a calling method. Finding this handler is an iterative process: first,
the top frame of the stack is popped, to point to a code location in a class, then that class is inspected to
test whether that code lies in a range which is protected by a `try`/`catch` block, which is checked to see
whether the exception that is thrown can be handled by the `catch` definition. If it can, then control is
redirected to that handler, and normal operations will continue. If it is not, then the next frame is popped
from the stack, and this sequence repeats, until either a matching handler is found, or it reaches the bottom
entry on the stack, and the application fails irrecoverably.

## Stack Traces

In this case, the JVM will print a _stack trace_ using the information encapsulated in the `Exception` object.
This can provide many useful clues about the state of the application at the point it failed, but importantly,
it shows us every method that was called from the entry point (the `main` method) of the program, up to the
point where the exception was thrown, with one line for each method call, and references to the source file and
position within that file that the method was defined.

Here is an example of a stack trace thrown by a simple program which calls the `factorial` method above on a
series of integers in a `List`. One of them is `-1`:

```
Exception in thread "main" java.lang.Exception: Parameter is non-positive
    at example$package$.factorial(example.scala:3)
    at example$package$.run$$anonfun$1(example.scala:10)
    at dotty.runtime.function.JFunction1$mcII$sp.apply(JFunction1$mcII$sp.java:12)
    at scala.collection.immutable.List.map(List.scala:250)
    at example$package$.run(example.scala:10)
    at run.main(example.scala:8)
```

## Interpretation of Stack Traces

The first line shows that there was an exception thrown, with the type `java.lang.Exception` (the "standard"
exception type), with a custom message. The next line indicates that this exception happened in a method called
`factorial` in an object with an encoded name, `example$package$`, the package corresponding to a file called
`example.scala`, and that point is made explicit with the detail `(example.scala:3)` which states the name of
the source file where the error occurred, and also the line number, `3`.

Other lines in this stack trace indicate that the `map` method of the class `scala.collection.immutable.List`
was called, defined in a source file called `List.scala` (which is part of the Scala standard library source
code). A generated Java source file, `JFunction1$mcII$sp.java`, also appears, exemplifying how both Java and
Scala can compile methods which can call each other.

Finally, at the bottom of the stack trace, the line `at run.main(example.scala:8)` indicates the entry point of
the entire application: the `main` method of the class `run`, defined on line `8` of `example.scala`.

Stack traces are one of the most basic concepts we need to understand when programming in Scala, and they will
often be our only means to understand why a failure has occurred in our code. The call stack is what makes them
possible. And while the details of how a stack is used are very intricate, our understanding of the exact
process of a program can remain superficial, so long as we understand how to read stack traces.

?---?

# Stack traces can reveal:
  * [x] The type of exception that was thrown
  * [ ] The exact time that the exception was thrown
  * [ ] All values stored on the stack
  * [x] Each method that has been called (but which has not yet returned)
  * [x] The name of each source file from which those methods were compiled 
  * [ ] The parameters to those methods
  * [x] The line numbers in the source files from which those methods were compiled

# Have a look at the following stack trace:

```
Exception in thread "main" java.lang.Exception: there was an unfortunate failure
        at example$package$.beta(defs.scala:11)
        at example$package$.alpha(defs.scala:8)
        at example$package$.beta(defs.scala:12)
        at example$package$.alpha(defs.scala:8)
        at example$package$.beta(defs.scala:12)
        at example$package$.alpha(defs.scala:8)
        at example$package$.run(example.scala:3)
        at run.main(example.scala:2)
```

On which line of which file, and in which method was the exception thrown? You will need to select a line,
method and file.

* [ ] line 2
* [ ] line 3
* [ ] line 8
* [X] line 11
* [ ] line 12
* [X] method `beta`
* [ ] method `alpha`
* [ ] method `example`
* [ ] method `run`
* [X] file `defs.scala`
* [ ] file `example.scala`
