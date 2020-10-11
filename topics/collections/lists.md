## Why are there so many collections in scala?

Scala's standard library provides many different collection types, which differ primarily in the structure they
use to store the values contained within them. The way a collection's internal data is structured has
implications for how that data is stored and accessed, and certain operations will be performed much more
quickly with some collection types than others.

This means that the choice of which collection type to use can play an important role in the performance
characteristics of an application when it is run. The knowledge we have about how values will be added to,
removed from or updated within a collection and the way and the frequency with which they are accessed are
important considerations when making choosing a collection type.

There is no single "ideal" collection for all purposes, and every collection type will have certain advantages
in some areas and make certain compromises in others. Some, like `Vector` provide a good general balance for
working with ordered sequences of data, whereas `List`s can provide much better performance if we are not
reading or writing elements at arbitrary locations within it. `Stream`s are similar to `List`s, but where the
end of the list is computed _lazily_, or "on-demand", and whose total length is not known at the outset, and may
actually be infinite.

`Set`s are optimized for deduplicated, unordered values while `TreeSet`s can take take advantage on a sort order
on the set's elements. These have _map-like_ counterparts which associate with each item, which we call the
_key_, a secondary associated value of another type (which is our choice), allowing the associated values to be
accessed using a key as an index. These types are called `Map` and `TreeMap`.

Other types in the collections library provide generalizations of these interfaces for when we need to operate
on a collection without requiring that it be a particular one. For example, the `Iterable` type is a
generalization of `List`s, `Vector`s and `Set`s because we can iterate over their elements, without concerning
ourselves with the exact structure of the elements in that data structure. `Seq` is a generalization of `List`
and `Vector`, but not `Set`, as its elements are unordered, so don't exhibit the "sequential" nature that the
`Seq` type is intended to encapsulate.

## List

`List`s are the most commonly-used Scala collection, particularly (but not only) for working with small
collections of data. Accessing the first element of a list, the _head_, is very quick, as is accessing the
_tail_, the remainder of the list after the head is removed, which is itself a `List`.

To access element 1 of the list (the second element) requires looking at the head of the list's tail, which is
_two_ operations. Element 2 requires accessing the head of the tail of the list's tail, which is _three_
operations. While each operation is very fast, in general it takes _n_ operations to access the _nth_ element,
which makes `List` unsuitable for operations which require _random access_ of elements within the sequence.
The method `List#last` exists, but the cost of executing it will be proportional to the length of the sequence.

The structure of Scala's `List` is usually called a _linked list_, or more precisely, a _singly-linked list_.
Each List instance is an element (the head) attached to another list containing (potentially) more of the same
type of value. That is true apart from one special `List` instance called `Nil`, which is an empty list. It has
no head and no tail, but it's necessary to terminate every list.

There is only one `Nil` instance. While we can create an empty list of `String`s or an empty list of `Int`s, as
there is nothing in either of those lists, the element type is not relevant, and the lists are not only
indistinguishable, but literally the same value, so every `List` in Scala will share a tiny part of its tail.
`Nil` is necessary in Scala to terminate every list; without it, every list would have to provide a link to
another `List` instance as its tail, which could only carry on infinitely.

Diagrammatically, a `List` looks like this,
![Singly-linked list](/api/content/contentImages/singly-linked.svg)
or, if we were to describe the _structure_ of Scala's `List` using an `enum`, it would look similar to this:
```scala
enum List[+T]:
  case Nil
  case ::(head: T, tail: List[T])
```
where a `LinkedList` of the first three natural numbers would be written,
```scala
val xs = ::(1, ::(2, ::(3, Nil)))
```
or using _infix_ style, where the right-associative method `::`, defined on `List` will call the `::`
constructor, meaning that `::(head, tail)` can, in general, be written as `head :: tail`. So we can more neatly
write,
```scala
val xs = 1 :: 2 :: 3 :: Nil
```
Scala permits the use of a symbolic name for a type, `::`, which is generally referred to as "cons", short for
"construct", and equivalent to the arrows on the diagram, above.

Constructing new `List`s presents a similar compromise in performance: prepending an element to the start is
fast, regardless of the length of the original list, because it requires only the creation of a single new `::`
object which links the new element to the pre-existing tail. But adding an element to the end of the list is
less trivial.

Imagine we wanted to add `4` to our list of natural numbers, above. That is, we want to construct,
`1 :: 2 :: 3 :: 4 :: Nil` from `1 :: 2 :: 3 :: Nil`. Unlike prepending, we cannot "reuse" the existing list,
because `1` is attached to `2 :: 3 :: Nil`, and `2` is attached to `3 :: Nil`, and `3` is attached to `Nil`,
each one being an independent `List` instance in memory. We can construct the new `List`, `4 :: Nil`, and
then use that as the tail to the new instance, `3 :: 4 :: Nil`. We can continue to produce, `2 :: 3 :: 4 :: Nil`
and finally, `1 :: 2 :: 3 :: 4 :: Nil`. But in comparison to prepending an element to an existing list, which
took a single operation, _appending_ requires a number of operations proportional to the length of the list,
making it very inefficient for large lists.

Despite this difference, the methods available on `List`s and `Vector`s are mostly the same. Both have `head`
and `last` methods and both have the `+:` (prepend) and `:+` (append) methods, even though some of these methods
may have quite different performance characteristics for long sequences.

In comparison, none of `Vector`s operations are proportional to the size of the collection, all being
guaranteed to complete in fewer than a small, fixed number of operations. Accessing the first element of a
`Vector` will require more operations than accessing the first element of a `List`, so it will be slower, as
will constructing a new `Vector` by prepeding an element to the start of the `Vector`, because `List`s are
structurally optimized for precisely these operations.

But the guarantee that `Vector` provides is very useful for understanding scalability of operations. The
guarantee assures us that operations on `Vector`s will have more _predictable_ performance than those on
`List`s as the number of elements we store within them grows, even if the performance of `Vector`s is
notably worse for smaller-sized collections.

Often, the biggest challenge when learning Scala's collections is knowing the performance characteristics of
their methods. This requires practice and experience, and even then the analysis can be difficult and
error-prone. Often the only solution is to use _benchmarking_, which we will learn about later.

## Set

`Set` is a collection that keeps neither the order of its elements nor multiple copies of the same element
within it. This is equivalent to the algebraic concept of a
[set](https://en.wikipedia.org/wiki/Set_(mathematics)).

Sets provide some simple operations for inclusion and removal of elements. As the elements of a `Set` have no
order, no distinction needs to be made between _prepending_ and _appending_, so an element may be added to an
instance of a `Set` with the `+` operator, though as `+` is a left-associative method on the `Set` type, the
`Set` must go on the left, while the element to be added should be on the right of the operator, like so:

```scala
val powersOfTwo = Set(2, 4, 8)
val evenNumbers = powersOfTwo + 6 + 10
```

The `evenNumbers` value is a `Set` containing five elements, though care should be taken in interpreting the
expression which created it. Scala's left-to-right expression order is particularly important in interpreting
the addition of `6` to `powersOfTwo`, followed by the addition of `10` to the resultant `Set`. With explicit
parentheses, this would be written,
```scala
val evenNumbers = (powersOfTwo + 6) + 10
```
which is quite different from,
```scala
val evenNumbers = powersOfTwo + (6 + 10)
```
which would first evaluate the arithmetic expression `6 + 10`, to give `16`, which would then be included as an
element of the set.

The important observation to make is that `powersOfTwo + 6` is an expresion which constructs an intermediate
value, whose type is known to be `Set[Int]`, a set of integers, which provides the context to interpret the
subsequent `+` operator as a subsequent addition to the set, and not as the identically-named `+` operator on
`Int`s (or even the `+` concatenation operator on `String`s).

An element can likewise be removed from a `Set` with the `-` operator.

A useful operaton on `Set`s is their ability to test whether they contain a particular element or not. This can
be done with the `contains` method, which returns `true` if the element exists in the `Set`, or `false`
otherwise.

The test, for example,
```scala
Set(1, 2, 3, 4).contains(2)
```
would evaluate to `true`.

`Set`'s `contains` method is fast because of the way a `Set` stores its elements. The method `contains` exists,
equivalently, for all `List`s and `Vector`s too, but with performance that varies depending on the size of the
sequence: their implementation of `contains` can only produce an answer by comparing `contains`'s parameter to
each element in turn, until a match is found, or the end of the sequence is reached. This does not scale well.

`Set`, by comparison, uses hashing to store the elements in a data structure that is optimized for operations
such as `contains`. This enables the presence of values in the set to be tested in _constant time_. That is to
say, no matter how large the set is, the computational time taken to perform the `contains` operation is fixed,
or at least, bounded above.

Sets offer a rich assortment of other operations. The most useful of these are,
- `set ++ collection`, for appending every element of `collection` to `set`,
- `set -- collection`, for removing every element of `collection` from `set`,
- `xs.intersect(ys)` or `xs & ys`, for calculating the intersection of the elements of `xs` and `ys`,
- `xs.union(ys)` or `xs | ys`, for calculating the union of the elements of `xs` and `ys`
