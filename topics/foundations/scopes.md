## Resolving Names

At any point within a Scala source file where we may refer to values, methods, objects, types, traits, enums and
classes by an identifier, Scala must resolve the name we use to the unique definition, somewhere else in our
code, or within libraries that we depend upon.

The process of resolving an identifier to a _symbol_, the general name for a uniquely defined entity that the
compiler needs to refer to, is context-dependent. For example, in the following code,

```scala
package com.example

case class File(path: String):
  import java.io.File
  val x = File("/tmp/file.txt")

val y = File("/tmp/file.txt")
```

the definitions for `x` and `y` are identical, though `x` creates a new instance of `java.io.File` whereas `y`
creates a new instance of `com.example.File`. Both are referred to as `File` but the presence of the import of
`java.io.File` affects the way that Scala chooses how `File` should be resolved.

While every position that an identifier may appear has its own context, these may be conveniently structured
into _lexical scopes_. Within one lexical scope (or just a _scope_) the same identifier will always resolve to
the same symbol.

## Nesting

The most important feature of scopes is that structurally, they _nest_, so apart from the _top-level scope_,
every scope is entirely nested _within_ another scope, potentially many layers deep. The significance of this
_nesting_ is that an inner scope automatically has available all of the context of its outer scope, and may add
to or modify that scope, but only within its own bounds.

Here is how that works in practice. Imagine a method nested within an object inside a class.
```scala
import utils.Server

class Form():
  val data: HashMap[Field, String] = HashMap()
  def complete: Boolean = ???
  object Submit:
    def send(): Unit =
      if complete then Server.send(data)
```

This short fragment of code introduces several scopes. In the top-level scope, the `Form` class is introduced,
and the `Server` object is imported. Every scope nested within the top-level scope will have access to these.

The body of `Form` is a new scope, which has available all of the top-level scope. It introduces a value,
`data`, a method, `complete` and an object, `Submit`.

The object `Submit` further introduces a new scope, which inherits the definitions from `Form`'s scope directly, and
transitively, `Server`. And also `Form` itself, from the top-level scope. Furthermore, the method `send()`
is defined in this scope. The body of `send()` introduces another new scope, but it introduces no new symbols, and it
may refer to symbols defined in any of the prior scopes we mentioned.

## Shadowing

A new scope may introduce new identifiers, but it is also permitted for these to have identical names to
identifiers defined in outer scopes. This does not produce any error or warning, and the identifier in an inner
scope will always take precedence over an identically-named identifier in an outer scope. This is called
_shadowing_ because the "closer" identifier casts a shadow on the outer identifier, making it invisible to the
user from within the inner scope.

Shadowing is occasionally useful, but can be the source of occasional confusion: when reading source code, we
can often relate the use of a value with a particular identifier in one place in the code to a definition for
an identifier with the same name elsewhere, in an outer scope, believing them to be the same, but to later
discover that a second (different) definition had been introduced to the inner scope, shadowing the identifier
we found.

While we can refer to an identifier within an outer scope directly, without any prefix (such as `list.name` for
a member called `name` in an object called `list`), the reverse is not true. A scope may contain any number of
nested scopes, and elements within those scopes may only be accessed via a prefix—if at all.

## Context and Paths

This makes sense from a semantic perspective: a new scope, whether it is a lambda or a class or a case
expression, generally introduces some new context—for example, the lambda's parameter, a class's `this` value,
or the identifiers bound to a matched pattern—and any new definitions we introduce can depend on this context.
It does not make sense to reference that context or any of its derivatives from outside of the scope of that
context.

Paths, such as `list.name`, are a means of providing the context—in this case, a value called `list`—that is
necessary to access the identifier `name` which is dependent on the context.

This is possible when the context is dependent on a named value, such as a class instance, but does not make
any sense for scopes that arise in the body of a method, or on the right-hand side of a case clause, where the
context does not have a convenient identifier, or exists only ephemerally. Hence, these scopes are inaccessible
from outside.

In general, working with Scala's scopes is usually very natural. They are an example of where syntax complements
semantics and the structure of source code has a close relationship to the context that is relevant and
accessible at any point within our code.

?---?

# From a nested scope, all identifiers defined the surrounding scope can be accessed, apart from:

* [ ] imported and exported members
* [X] members which are shadowed
* [ ] objects
* [ ] classes, traits and types

# Consider this code:

```scala
val button: Boolean = true
object App:
  import Events._
  def myButton: Boolean = button
  def run(): Unit = println(myButton)
```
When calling `App.run()`, what will be printed?

 - [ ] We know it will be `true`
 - [X] We cannot know for sure without also knowing whether `Events` contains a member called `button`
 - [ ] If it compiles, it will print `true`
 - [ ] Even if it compiles, and we know everything the definition of `Events`, we cannot know for sure whether `true` or `false` is printed

# Now consider the following code:

```scala
object Date:
  val date = Date(7, 9, 2022)

case class Date(day: Int, month: Int, year: Int):
  val date = Date

val date = Date(1, 1, 2000)
```

What is the result of, `Date.date == date.date.date`?

- [X] `true`
- [ ] `false`
- [ ] it does not compile

# And in the same example, what is the result of, `Date.date.date == date.date`?

- [X] `true`
- [ ] `false`
- [ ] it does not compile