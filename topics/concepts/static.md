## Compilation vs Interpretation

Many programming languages allow us to write code, and run it directly, converting the source code into machine
code and running it, as it is being read. This is called _interpretation_, and contrasts with _compilation_,
which fully converts an entire program from source code to machine code before any of it is executed. Pieces of
software which perform these actions are called _interpreters_ and _compilers_ respectively.

The distinction between compilation and interpretation might, at first glance, seem to be a choice of how a
program is _run_, rather than a property of the language itself. And it's true that some languages have both
compilers and interpreters for their source code, and can be either compiled and run, or interpreted without
prior compilation.

But almost invariably, programming languages are designed primarily (or exclusively) for compilation _or_ for
interpretation, because the design of a language can take advantage of knowing how its source code will be
executed.

A compiled language can offer features in the language which allow the compiler to do additional
self-consistency checks on the code; checks which would require visibility of the _entire_ program to perform,
not just the current line under consideration. And likewise, an interpreted language can forego certain rigors
that a compiled language imposes, and offer more plasticity in source code.

In a hypothetical compiled language, if we refer to a value called `number` on an object called `Page`, then the
compiler would need to know that the object called `Page` exists, and be certain that it _has_ a value called
`number`, or else it would refuse to compile the entire program. But a hypothetical interpreted language would
only check that the `Page` object exists when it interprets a line of code referring to it, and would only check
whether the `number` value exists inside that object when interpreting it. An interpreted language designer
could offer a facility to add the `number` value to the `Page` object at a moment of the programmer's choosing,
and as long as it is present when it is accessed, no error would be produced while interpreting the program.

In compiled languages, such flexibility is not usually possible because it's hard or impossible for the compiler
to know, with certainty, whether a value (whose existence is conditional) exists at the time the attempt is made
to access it. And so compiled languages generally don't offer so many features for changing the way code is run
by the code itself.

Scala is exclusively a compiled language, and there are no interpreters for Scala source code. (There are,
however, ways of compiling series of small fragments of Scala to give the impression of interpretation, but no
interpreters in the traditional sense.) Scala is designed to maximise its advantages from being compiled, and
many of its features would be impossible (or pointless) in an interpreted language.

## Static vs Dynamic

The distinction between interpretation and compilation is often described as _dynamic_ vs _static_. Interpreted
languages have more flexibility to behave _dynamically_, because their code is interpreted as it is run, and
the state of the running program can therefore affect the nature of the interpretation. Whereas, during a
compilation, nothing is known about the program's state while it is running (or, at _runtime_), so the meaning
of the code cannot be dependent upon it in any way, and can therefore be understood (by human or computer)
unchangingly, or _statically_.

Both static and dynamic programming languages are common today, but Scala wholeheartedly chooses and endorses
the static approach, on the basis that dynamism introduces uncertainty to the behavior of a program, whereas
greater staticity throughout a program can provide guarantees about the reliability of that behavior, and the
majority of Scala programmers, and this course, agree.

Nevertheless, this is an ongoing debate, and many people still disagree over which approach is most
advantageous.

Even in the context of a compiled language, it is common to consider what information is known statically about
our code and the values we work with, and what information is unknown until the code is run, or, _dynamic_. For
example, the expression `2 + 2` is _statically_ known to be the integer `4` at compile time because the Scala
compiler has all the information it needs to compute it. Whereas, an expression which reads input from the
console and interprets it as an integer, `StdIn.readInt`, could evaluate to any integer, and while it is known
statically that it will always be an _integer_ (and not, say, a string or a boolean), the actual integer value
is unknown during compilation (or, at _compiletime_), may be different on different occasions that it is
evaluated, and is therefore called _dynamic_. (It could also result in a failure, of course.)

"Static" and "dynamic" can be used, quite generally, to describe those details of a program that are known at
compiletime and those which are known _only_ at runtime, and different Scala language features may be involved
in asserting them. But the vast majority of static assertions the Scala compiler makes are encoded through
_types_. Types can be thought of as a shorthand for describing (and hence having the compiler assert) all the
properties of a value that are known statically.

## Types (and Tests)

Scala is able to assert whether certain operations on a value are safe based on its _type_. For example, the
expression, `5 - StdIn.readLine`, which tries to subtract a _string_ from an _integer_ would not compile because
the type of `StdIn.readLine` is not a valid for subtraction from an integer. It makes no sense, so the Scala
compiler will refuse to compile it, and will report a _compile error_ and exit without producing any runnable
code.

All values have types, which encode, to a greater or lesser specificity, the facts known statically about each
value, and effectively constrain the uses of that value to preclude the nonsensical ones. Knowing the type of
every value (or expression) allows Scala to quickly check the valid and invalid uses of that value, without, for
example, having to trace the value's provenance back to its origins.

The _type system_, built upon the DOT Calculus, is the cornerstone of Scala, and it impacts many different
aspects of the language. But types are not the exclusive domain of compiled languages: interpreted languages can
use types too, but by their nature, they can only be checked at runtime, so there are limits to their efficacy.
So the terms _statically-typed_ and _dynamically-typed_ are often used to describe programming languages too.

Dynamically-typed languages usually make greater usage of tests, in particular _unit tests_, to verify the
correctness of code. These can provide useful assurances about the code, but do not offer the same guarantees as
a static type system: they attempt to verify code by running it with a representative sample of possible runtime
states, and comparing the results to expected values, but (unlike types) there is no proof of their correctness.

For dynamic values, even within a statically-typed language, tests can still be very useful. It is not always
possible or practical to encode enough precision with types to verify a program for _all_ possible inputs. And
in many scenarios, unit tests can offer additional confidence that our code does what we intend it to do.

## Summary

The distinction between the static and the dynamic will be a common theme in this course. It is our goal to
write _correct_ software, with fewer bugs, and static invariants, often asserted through types, should be
preferred wherever possible. So much of what we will learn in Scala will be motivated towards maximizing the
facts we encode statically in types, and having the Scala compiler do the hard work of checking our code.

?---?

# Scala is...

- [X] a statically-typed language
- [ ] a dynamically-typed language

# True or false? Interpreted languages never have types.

- [ ] True
- [X] False

# True or false? Unit tests may verify facts about a program that types cannot verify.

- [X] True
- [ ] False

# True or false? Most programming languages are either designed to be interpreted or designed to be compiled.

- [X] True
- [ ] False

# Select all the facts which can be known statically

* [X] the expression `5 + 4 > 3` is `true`
* [ ] the expression `x/2 > 0` is `true` where `x` is an integer
* [X] the expression `3*2` is `6`
* [X] the expression `StdIn.readDouble` is a `Double`
* [ ] the expression `math.random > 0` is `true`
