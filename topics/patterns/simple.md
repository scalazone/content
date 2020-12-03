## Pattern Matching Keywords

Scala provides two keywords, `match` and `case` for inspecting a value, and making a choice between several
possible actions, based on what the value is.

Here's an example of a very simple pattern match expression:

```scala
enum Direction:
  case Up, Down, Right, Left

def move(dir: Direction, n: Int, x: Int, y: Int): (Int, Int) =
  dir match
    case Up    => (x, y - n)
    case Down  => (x, y + n)
    case Right => (x + n, y)
    case Left  => (x - n, y)
```

In this example, we _match_ on a `dir` value, which is an enumeration, `Direction`, and depending on its runtime
value—`Up`, `Down`, `Left` or `Right`—we return new `x` and `y` coordinates. For each possible value of `dir`,
the expression that appears to its right will be evaluated and returned. You could imagine this method being
used, for example, to recalculate the position of a rook on a chessboard.

## Generalized Branching

Pattern matching provides a more general way of performing branching than an `if`/`then`/`else` construct, though a
pattern match expression could be rewritten as an `if` expression. Here is the same `move` method, rewritten using `if`
, `then` and `else`:

```scala
def move(dir: Direction, n: Int, x: Int, y: Int): (Int, Int) =
  if dir == Up then (x, y - n)
  else if dir == Down then (x, y + n)
  else if dir == Right then (x + n, y)
  else (x - n, y)
```

We can see that the `direction` value is compared to the values `Up`, `Down` and `Right` in turn, returning a
different expression if any of these values is equal to `direction`. If not, we know that the value can only
possibly be `Left`, without needing to check for it, and the expression for the `Left` case is returned.

The behavior of both versions of this code is identical, but the first should look more readable, and this is a
key advantage Scala's pattern matching syntax provides. That should be clear just from this simple example, but
this advantage becomes even more significant with more complex examples.

## Match expressions

The entire `match`/`case` construction is an _expression_, so it returns a value for the body of the `move`
method. And we can use a match expression in the same places any other expression can be used. But when we write
a match expression like,
```scala
def move(dir: Direction, n: Int, x: Int, y: Int): (Int, Int) =
  dir match
    case Up    => (x, y - n)
    case Down  => (x, y + n)
    case Right => (x + n, y)
    case Left  => (x - n, y)
```
the value `dir`, immediately before the keyword `match`, is also an expression, albeit a very simple
one—just a reference to a value! It's called the _scrutinee_, because its value is what will be scrutinized in
order to decide which of the cases to execute, and what to return.

If we matched against a more complex scrutinee expression, such as a method call, it would be evaluated only
once, and its result value would be the scrutinee.

Each line beginning with the word `case` is called a _case clause_, and consists of a _pattern_ which we can
think of as a way of specifying what we want to compare the scrutinee to.

Sometimes the pattern will be an exact value, like `Up` or the integer `5`, where _equality_ between the pattern
value and the scrutinee determines whether the pattern matches or not. But other times the pattern may describe
only certain aspects of the scrutinee which we consider important. We will see examples of these later in this
topic.

Finally, after each pattern, to the right of the arrow (`=>`, which is often read verbally as "goes to") is the
expression that gets evaluated if that pattern matches the runtime value of the scrutinee, and, of course, only
one of the expressions to the right of the arrows will be evaluated each time the expression is evaluated.

## A Warning

Note that in some languages, once a case matches, the runtime will evaluate the right-hand side of the case
clause, and carry on evaluating the right-hand side of _every_ case clause after it, unless we explicitly
_break_ out of the match. This was rarely ever useful behavior for any program, and thankfully Scala does not
work this way, and only one single case clause will ever be evaluated.

For a functional language where every expression evaluates to a single value, it would not make sense, anyway:
how could an expression return a value and then return another value? Where would the first value go?

Pattern matching in Scala provides very convenient syntax for branching to different actions, by checking a
value, the scrutinee, against a series of patterns to try to find one which matches, then taking that branch.
A pattern match expression can be written as a cascade of `if`/`then`/`else` expressions, but is usually much
easier to read and maintain.

?---?
