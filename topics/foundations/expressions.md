# Expressions

The most fundamental components of Scala source code are _expressions_: code which _evaluates_ when a program is
run to produce a single _value_. Most of the code we write, excluding the signatures which define the structure
of classes, objects, traits and methods, will be expressions; they most closely represent the code that is doing
the _work_, as they describe the operations and processes that will be executed: the implementations of methods
and values that will be run to produce values.

Here are some example expressions:

- `7 + 4`, which evaluates to the value `11`
- `println("Hello, World!")`, which prints `"Hello, World!"` to the console when it is evaluated
- `xs.init ++ ys.tail`, which evaluates to a list which is the "init" of `xs` (all but the last element) joined
   to the tail of `ys`
- `list`, a reference to some value called `list`
- `name.substring(2, 4)`, which evaluates to the segment of the string `name` between characters `2` and `4`

## Composition

Expressions may be simple references to existing named values, selections using the `.` operator to access
members of an object (sometimes called _dereferencing_), or invocations of methods. Where a method takes
parameters, those parameters may themselves be expressions, which must be evaluated to values first, before the
method itself is evaluated with those values _passed_ to it as parameters.

In the example above, `xs.init ++ ys.tail`, `xs.init` and `ys.tail` are both expressions which evaluate to
values, before they are combined as parameters to the `++` method, and the entire expression evaluates to a
single value.

Furthermore, `xs` and `ys` are also expressions, albeit just simple references to named values, and they are
dereferenced to access their `init` and `tail` members, respectively.

In total, there are five different expressions in this short code fragment, which are evaluated in the following
order:
1. `xs`
2. `xs.init`
3. `ys`
4. `ys.tail`
5. `xs.init ++ ys.tail`

While Scala's syntax has some subtleties in its evaluation order, it should be clear that, for example, the
expression `xs` _must_ be evaluated as a prerequisite of evaluating `xs.init`, and likewise, `ys.tail` must
be evaluated before `xs.init ++ ys.tail`. We will discover why Scala chooses to evaluate `xs.init` before
`ys.tail` later.

So in general, all but the simplest expressions are composed of other expressions, each evaluating to a single
value. This value may exist only for the briefest moment, as an intermediate value which is immediately passed
as a parameter to another method (and never used thereafter), or may be a result which is kept for a long time,
and referred to multiple times during the program's life.

## Purity and Side-Effects

Some expressions can, during their evaluation, make changes which could be detected by an external observer.
The sorts of changes we consider "detectable" would include all of the following:
- writing a file to disk
- sending an HTTP download request across the Internet
- writing a character of text to the console
- modifying a globally-accessible set of integers
- accessing a value which counts the number of times it has been accessed

These may seem increasingly subtle, but all are considered _side-effects_, sometimes described as "changes to
the state of the universe". Though referring to the "state of the universe" may seem overly gradiose, it
nevertheless makes an important point: that the mere evaluation of a _side-effecting expression_ could be
detected by an external observer in some way, and by virtue of being detectable, code elsewhere could depend
upon the change, however subtle, and behave differently as a consequence, potentially in more significant ways.

Conversely, an expression which does not make detectable changes to the state of the universe leaves no trace of
whether it has been evaluated, and no other code can detect or depend on that fact. We call such expressions
_pure_.

Because pure expressions cannot make externally-detectable changes, the only way they can be useful is through
the value they evaluate to, and which they return; it is the only way the result of any computations they
perform can be used. But it is usable _only_ from the code which evaluates it.

Generally, this greatly limits the power or potential impact of pure expressions: they can have consequences
only within the expression from which they are called. But this lack of power is an enormous advantage for
programmers, because it means we can rely entirely upon _local reasoning_ without having to consider an infinity
of potential _global_ changes.

Pure expressions are therefore usually preferred to side-effecting expressions, because they make it easier for
us to reason about. But Scala supports both, and (in almost all respects) gives no special status to pure
expressions. We can use both pure and side-effecting expressions in Scala.

The definition of what we consider a side-effect can be a little nuanced. There are certainly ways of detecting
whether a pure method has been evaluated or not: time may have passed for an expensive computation, a JVM memory
dump could be analysed for leftover intermediate objects instantiated during the expression's evaluation, or
low-level system tools could be used to inspect the state of the computer's CPU. But these are all considered
intrusive, impractical and potentially unreliable, so we only consider those changes which are detectable from
within the JVM by means of "standard" unintrusive, reliable operations to be "side-effects".

## Exceptions

Expressions should return a single value, but sometimes problems occur during their evaluation which make it
impossible to return a value. For example when the expression,
- needs to allocate a new object in memory, but there is not enough free memory
- tries to access an element which is beyond the end of an array
- attempts to write a file to disk, but does not have permission to do so
- tries to download a file while the computer is offline

These are called _exceptions_, and evaluating an expression can always cause an exception to be _thrown_,
precluding the possibility of that expression returning a value. Consequently, any expression composed from an
expression that throws an exception is also unable to return a value. And hence, exceptions are like an "abort
mechanism" that progressively escapes from an expression which can't be evaluated, until the exception is
_handled_ and the programmer can provide some mechanism for recovering from the failure.

We will look at exceptions in more detail later in the course.

## Statements

Sometimes an expression will perform a useful action through a side-effect, but will not return any useful
value, for example, the expression,
```scala
println("Completed.")
```
will result in the side-effect of `"Completed."` being printed on the console, but will return no useful value.

But every expression which does not throw an exception must return a single value, so a `println` expression
will return the _unit value_, which we write as `()`. There is virtually nothing interesting that can be done
with the value `()`, but it exists in order to maintain the invariant that every expression returns a value.
Nevertheless, expressions which return `()` are called _statements_, and the invariant on returning a value
means that we can treat them like any other expression.

When two statements appear after each other on separate lines, or separated by a semicolon (`;`), they will be
evaluated one after the other. For example,
```scala
println("Waiting...")
Thread.sleep(1000L)
println("Done.")
```
will print `"Waiting..."` on the console, will then wait for 1000 milliseconds, before finally printing
`"Done."` on the console. Each line is a statement, evaluated in series, and each returns the unit value. But
because the first two are not used in any subsequent expression, they are effectively discarded. The result of
the final statement will be kept (though it depends on the context of these lines).

The same is actually true not just of statements, but of any expression, though unlike the unit values returned
from statements, we normally want to use the return values of other expressions. And when placed on separate
lines like this (or separated by semicolons), all but the last return value will be discarded.

Expressions are the most fundamental building-blocks of Scala code. Understanding them as the consistent and
composable means of specifying computations or sequences of operations is key to writing even basic Scala code.