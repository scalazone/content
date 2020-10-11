# Collections

As programmers we often need to store and operate on multiple similar values, where it's necessary to refer to
the values _collectively_ rather than individually, and where our code must work whether there is one value, a
million values, or zero. Scala provides a variety of _collection types_ with for this purpose.

An instance of a collection type is a value which provides us with the means to access the other values stored
within it. We can construct an instance of a collection from some initial values, and we get a new value
referring to the collection. But it is _just a value_ like any other, so we can pass it to a method, return it
as the result of a method, or add it to another collection, just like any other value.

Different collection types, such as `Vector`, `Set`, `List` and `Map` store values in different structures
within memory, which results in these collections having different characteristics for how their values can be
accessed, and how new collection instances are constructed from old ones, and how fast that can be done.

## Immutability

The collections we will learn about first are all _immutable_. This means that a collection value, once created,
can never change. But new collection values can be easily created based on existing collections, for example,
by adding a new `Int` to the start of a `List` of `Int`s: this will construct a new `List` of `Int`s, one
element longer, starting with the new value, but the old value will remain unchanged, so any object which refers
to the original list will not "see" the updated version, and both `List`s will continue to exist for as long as
they are needed.

This may seem unintuitive at first: we did not _need_ two lists! And we might be concerned about the memory
efficiency of storing multiple lists when we only needed one. This is a valid concern, but one which has good
answers, and for now we shouldn't worry. The benefit, which is a huge advantage the larger our code becomes, is
that immutable collections are much easier to reason about, particularly when multiple processes are using them
concurrently.

As an example, imagine a method which checks that a list in not empty, and if so, reads the first element of the
list. That _ought_ to work fine. But there's the possibility that another concurrent process is also modifying
the same list, and in the very short time that elapses between checking the size of the list, and trying to read
the first element, the other process may have emptied the list, so there would be no "first element", and an
error would be produced.

It might seem unlucky for the list to change in the nanoseconds between checking and reading the list, but that
might just make it more difficult to _discover_ a bug which remains genuinely _possible_, while it would be much
better to make the circumstances under which it could occur _impossible_.

Representing the list as an immutable value would mean that the list which is checked to be non-empty would be
exactly the same list whose first element is read, with no possibility that it could change in between. The
other process, whose job is to make updates to the list, could still make those changes, but each change would
produce a new list, with absolutely no effect on the original.

Scala also has several _mutable_ collection types too, whose elements can be modified like variables, where the
same reference may point to a different value at different times. These may be useful in some circumstances too,
but immutable collection types provide everything we need to work with collections for now.

### Talking about immutability

Much of programming in Scala involves constructing new immutable collections based on old immutable collections,
but it is cumbersome to have to explain the full detail of every change as the construction of a new instance of
a collection. So, for convenience, we will say instructions like, "add the value, `y`, to the set, `xs`",
knowing that what we mean is, "construct a new set from the set, `xs` plus the value, `y`", with the further
implication that the reference to the _new_ set will be used thereafter.

This may appear imprecise, or sound like _sleight of hand_, but in the context of immutable collections, it's
pragmatic, and will become very natural with practice. In the event of any ambiguity, we can always be precise
about the reality that the modification is made through the creation of a new value from the old.

## `Vector`s

A general-purpose collection for storing ordered lists of values (_ordered_, in the sense that their order is
significant and should always be preserved—not in the sense that "higher" values should come after "lower"
values) is `Vector`.

We can think about `Vector`s as sequences of values, where each element can be accessed by its numbered
position, or _index_, in the sequence. When a new element is appended to the end of a `Vector`, that new element
will be assigned an index one higher than the previous highest index.

Imagine we are storing a series of financial transactions using a `Vector`, where each transaction is
represented by an `Int`, being the change to the amount in the account. (We will not store any other details
about each transaction for now.)

If the account participates in three transactions: receipt of a deposit of $1000, a withdrawal of $200, and
finally, a withdrawal of $300. If each transaction is appended to an empty `Vector`, we could represent the
resultant `Vector[Int]` as follows:

| Index | Value |
|-------|-------|
| 0     | 1000  |
| 1     | -200  |
| 2     | -300  |

This sequence of actions could be written, in a verbose fashion, as
```scala
val emptyAccount: Vector[Int] = Vector()
val afterDeposit: Vector[Int] = emptyAccount :+ 1000
val afterWithdrawal1: Vector[Int] = afterDeposit :+ -200
val afterWithdrawal2: Vector[Int] = afterWithdrawal1 :+ -300
```

We first initialize the empty `Vector` of `Int`s and assign it to the `emptyAccount` identifier, which has the
type `Vector[Int]`, that is, a `Vector` containing `Int`s. In the subsequent lines we see the `:+` operator used
to append an integer value to the `Vector`, thereby constructing a new `Vector[Int]` from the old value.
Assigning each intermediate result to a named identifier should make it more obvious that every `Vector`
continues to exist after its creation: `emptyAccount`, for example, will always be a reference to a `Vector`
with zero elements.

More likely, we don't need all the intermediate results, so we could write this as,
```scala
val afterWithdrawal2: Vector[Int] = Vector() :+ 1000 :+ -200 :+ -300
```

The intermediate values are still computed, and are still stored in memory, but we no longer have any means to
refer to them, since we didn't assign them to named identifiers.

This syntax is still quite verbose, so Scala provides concise shorthand for `Vector`s (and most other
collections) to simply supply the elements as arguments to the name of the collection type, like so:
```scala
val afterWithdrawal2: Vector[Int] = Vector(1000, -200, -300)
```

`Vector`s also provide a counterpart to the `:+` operator for _prepending_ elements to the start of a `Vector`.
That operator is `+:`, the mirror-image of the `:+` operator. For example,
```scala
val account = -100 +: afterWithdrawal2
```

After this operation, `account`'s elements would look like this:

| Index | Value |
|-------|-------|
| 0     | -100  |
| 1     | 1000  |
| 2     | -200  |
| 3     | -300  |

Both `:+` and `+:` have one operand which is a `Vector` and one operand which is the element type, in our case,
`Int`. We need to remember which operator is which, and the easiest way is to remember that `:` is always on the
side of the collection, and the `+` is on the side of the element.

It is also possible to join two `Vector`s together, regardless of the lengths of the inputs. The `++` operator
(which unfortunately does not conform to the mnemonic above!) will construct a new `Vector` from two existing
`Vector`s as operands, for example,
```scala
val transactions = account ++ Vector(200, 400, 100)
```
will construct a new `Vector` with a total of seven elements.

## Accessing `Vector` Elements

Convenient methods exist for accessing the first and last elements of a `Vector`, `Vector#head` and
`Vector#last`, which must be called on a non-empty `Vector`, or they will throw an exception. They have
complementary methods called `Vector#tail` and `Vector#init` (in the sense of _initial_ values) which will
construct new `Vector`s from the elements remaining after the `head` and the `last` values are removed,
respectively. Again, these methods will throw exceptions if they are called on an empty `Vector`.

We can test if a `Vector` is empty using the `Vector#isEmpty` method or its complementary `Vector#nonEmpty`
method. These methods always return the inverse of each other, and while only one is _necessary_, both exist to
give the programmer an opportunity to subtly signal the positive or primary branch. In all cases,
- `xs.nonEmpty == !xs.isEmpty`, and therefore,
- `xs.isEmpty == !xs.nonEmpty`

Furthermore, assuming the `Vector` `xs` has at least one element, then the following expressions are all equal:
- `xs`
- `xs.head +: xs.tail`
- `xs.init :+ xs.last`

Occasionally, though, the element we need is not the first or last element, but an element at a particular index
within the `Vector`, for example the third element, which has the index `2`.

This has been a frequent point of confusion for decades, as collection indices in Scala, as with many languages
that came before it, always start at `0`. So the "first" element has index `0`, which means that the "second"
element has index `1`.

Using the example of our earlier `Vector`, `account`, its elements are:

| Index | Ordinal | Value |
|-------|---------|-------|
| 0     | first   | -100  |
| 1     | second  | 1000  |
| 2     | third   | -200  |
| 3     | fourth  | -300  |

It's also common to refer to element `0` as the "zeroth" element, but we will avoid that, and always call it the
"first" element, and will avoid—as much as possible—referring to any element in a `Vector` or other collection
by its ordinal name, and instead refer to each as "element _n_", where _n_ starts at `0`; the `head` element.

Thankfully, accessing element _n_ in a `Vector` is very easy: we apply, in parentheses, the number _n_ to the
`Vector`'s identifier, for example, `account(3)`, which would return a single element, the `Int`, `-300`.

It's not possible to access an element beyond the last element of the `Vector` (or before element `0`!), so
indices less than `0`, or equal to the length of the `Vector` or higher will throw an exception. We could safely
check this using the `Vector#length` method of any `Vector`, like so:
```scala
def safeGet(idx: Index, xs: Vector[Int]): Int =
  if idx >= 0 && idx < xs.length then xs(idx) else 0
```

There are, however, likely better ways of achieving the same safety, without explicitly checking the length of
the `Vector`. There are many more methods available for `Vector`s and other Scala collections that make working
with them very safe and easy. Later lessons will explore these in more detail, but a few interesting ones are:
- `count`, for counting the number of elements which adhere to a given predicate
- `distinct`, for removing duplicate elements from the `Vector`
- `permutations`, for generating every permutation of the elements of the `Vector`
- `min`, for finding the _lowest_ element in a `Vector` (as long as the element type is ordered)
- `reverse`, for reversing the order of the `Vector`'s elements