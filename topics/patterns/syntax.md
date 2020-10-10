# Pattern Matching Syntax

Reading and writing match expressions requires us to understand a couple of fundamental details of Scala's
syntax. In this lesson, we will examine a couple more of these details: the significance of identifier names in
a pattern, and alternation.

## Naming and Patterns

In a match such as,
```scala
enum Validation:
  case Invalid, Valid

val Blank = Some("")

def valid(input: Option[String]): Validation =
  input match
    case None  => Invalid
    case Blank => Invalid
    case other => Valid
```
there is a subtle difference between the first two patterns and the final one. `None` and `Blank` are values
which are already defined outside of the scope of the match, and the `input` value is compared to each of them,
in turn. But `other` is not defined anywhere else: it's a new identifier which is _introduced_ by the pattern.

The choice between these two behaviors depends on a detail that might not be obvious at first: both `None` and
`Blank` start with a capital letter, whereas `other` does not. The compiler will look at the name given to the
identifier, and match by equality if it starts with a capital letter, or will introduce a new identifier if
it does not, binding it to the extracted value, regardless of whether an identifier with the same name already
exists in scope.

For this reason, when we know in advance that a particular value is likely to be used in a pattern, it's good
practice to assign it a name which begins with a capital letter.

But sometimes we don't have the luxury of _choosing_ the name for a value, and we want to match against a value
whose identifier starts with a lower-case letter. Normally, this would be impossible because writing an
identifier which does not start with a capital letter would introduce a new identifier which would always match,
and which would _shadow_ an identifier with the same name, silently. This is something to be very wary of.
Here's an example of that trap:

```scala
val red: Color = Color(1.0, 0.0, 0.0)
val cyan: Color = Color(0.0, 1.0, 1.0)

def describe(color: Color): String = color match
  case red  => "red"
  case cyan => "cyan"

describe(cyan)
```

If we follow the code, we might assume that the call to `describe(cyan)` would return the value `"cyan"`.

But calling `describe(cyan)` will return `"red"`. That's because `case red` will match on _any_ scrutinee, and
bind it to the identifier `red`. The second `case` will never match, and, in fact, the compiler will warn us
about this, but we can't always rely on the second case being present to force the warning.

One solution would be to create new `val`s starting with capital letters, which reference `red` and `cyan`,
```scala
val Red = red
val Cyan = cyan
```
but a better solution is available, which is to wrap the identifier in backticks. That ensures that it is
treated as a _reference_ instead of a new identifier. Here is the previous example, rewritten: 

```scala
val red: Color = Color(1.0, 0.0, 0.0)
val cyan: Color = Color(0.0, 1.0, 1.0)

def describe(color: Color): String = color match
  case `red`  => "red"
  case `cyan` => "cyan"

describe(cyan)
```

The call to `describe(cyan)` will now return the `String`, `"cyan"`.

The capitalization rule applies to all values, with a few exceptions: `true`, `false` and the `null` are three
examples, but as it is not possible to create values named `true`, `false` or `null` (and would be a bad idea,
anyway), these three values can be specified in patterns unambiguously with lower-case initial letters, and they
are treated as literals.

Likewise, numbers such as `5` and `3.14159` are treated as literals, and so are `String`s, like `"this"`. They
are therefore compared to the scrutinee with an equality check.

## Alternation

Sometimes we have two cases in a match expression which should invoke exactly the same behavior. For example:
```scala
def validate(name: Option[String]): Validation =
  name match
    case None =>
      log.warn("A valid name was not provided.")
      Invalid
    case Some("") =>
      log.warn("A valid name was not provided.")
      Invalid
    case Some(_) =>
      Valid
```

In this instance, both `None` and `Some("")` should log a warning and be considered invalid responses. The
right-hand side of each case clause is identical, and yet we are repeating it verbatim, twice.

Scala provides a convenient operator, `|`, which may be used between patterns to indicate that either one or the
other pattern in that case may match. We can use it to reduce this example into just two cases, like so:
```scala
def validate(name: Option[String]): Validation =
  name match
    case None | Some("") =>
      log.warn("A valid name was not provided.")
      Invalid
    case Some(_) =>
      Valid
```

This is called _alternation_, because it provides _alternative_ patterns to try to match against.

Of course, the `|` operator may be repeated, and it may be used on nested scrutinees. Here's another example
which tries to read a `Boolean` value from an `Option[String]`, but which will return `None` for invalid input:
```scala
def readBoolean(input: Option[String]): Option[Boolean] =
  input match
    case Some("true" | "yes" | "on" | "1")         => Some(true)
    case None | Some("false" | "no" | "off" | "0") => Some(false)
    case _                                         => None
```

Imagine having to list every one of those cases on a separate line!

Alternation does not permit us, however, to bind identifiers to patterns in an alternation. It would not, for
example, make sense to match on `case Some(a) | None` and expect to use `a` on the right-hand side of the case
clause; if it matched on `None` there would be no value for it to bind to.

Hypothetically, we could imagine matching on an `Option[Either[Int, Int]]` instance with
`case Some(Left(a)) | Some(Right(a))` and using the value `a` on the right-hand side of the case clause, but for
generality, even this is forbidden. Thankfully, it is not a significant loss, and knowing it is forbidden makes
it easier to reason about where, within a pattern, an identifier originates.

This simple machinery gives us some useful tools for writing more expressive patterns.

?---?

# Choose which pattern will match the expression
```scala
val red = Color(1.0, 0.0, 0.0)
val green = Color(0.0, 1.0, 0.0)
val Blue = Color(0.0, 0.0, 1.0)

green match
  case Blue => 
    println("First")
  case Color(1.0, _, _) =>
    println("Second")
  case red =>
    println("Third")
```
- [ ] First
- [ ] Second
- [X] Third

# Choose pattern that *does not* contain syntax errors, given color definitions from previous question
 - [ ] ```scala
  red match 
    case Color(r, g, b) | Blue => println("Match!")
 ```
 - [X] ```scala
 green match 
   case red => println("Match!")
 ```
  - [ ] ```scala
  Blue match 
    case `blue` => println("Match!")
  ```