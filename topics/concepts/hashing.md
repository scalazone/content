# Hashing

The concept of _hash functions_ is fundamental to a number of different areas of software development, from high
performance access of elements in collections, to security, to caching, it has a variety of different
applications. A good understanding of the basics of _hashing_ is essential.

## What is a Hash Function?

A hash function is a pure, total, deterministic function from a large domain into a smaller range, where a
different input is _very likely_ to produce a different output.

The purpose of a hash function is to make it easier to check whether two things are _different_ with
_certainty_, or the same with some likelihood.

As a trivial example, a function which maps each integer to its remainder after dividing its absolute value by
`127` is a hash function: our domain is all the integers (infinity, in theory, though there are only 2³²
different `Int` values in Scala!) and the range is the integers from `0` to `126`, inclusive.

```scala
def hash(value: Int): Int = math.abs(value)%127
```

We could pass the numbers `395601`, `662`, `4` and `9563` to the hash function—which we call _hashing_ them—and
we would get the numbers, `123`, `27`, `4` and `38` in return, which all happen to be different. The fact that
the values we get back, which we call _hashes_, are different proves that the inputs were also all different,
because the same input will always generate the same hash.

But having two inputs which produce the same hash does not confirm that they are the same input, because there
are many different inputs which could all produce the same hash. Using our hash function, the inputs `50`,
`177`, `304` and `2147483563` would all hash to the same value, `50`, for example.

When two inputs produce the same hash value, we still do not know for sure if the inputs are the same or
different. We only get useful information that the inputs are different when the hash values are different, and
it is much more common that two different inputs will produce two different hash values. But it does mean that
if two inputs hash to the same value, we need to do further checks before we know if they are equal or unequal.

Hashes are useful because, having a smaller range, the computational cost of comparing two is smaller than it
would be for a full comparison of the inputs. Consider the numbers `38126976` and `38162976`. Are they the same?
It probably takes a couple of seconds to check the digits one by one, to discover that they are different.
However, the hashes of those two values are `52` and `111` respectively, which are _obviously_ different.

But how about the numbers, `38619276` and `38962176`? The hashes of `38619276` is `100`, and the hash of
`38962176` is also `100`. The hashes do not prove that the inputs are different, but do not prove that the
inputs are the same either. We must check `38619276` and `38962176` carefully to detect whether they are the
same.

In this case, they are not.

Most combinations of random numbers would have different hashes using our simplistic hash function, above, so
the majority of comparisons could be done very quickly just by comparing the hashes. But a tiny number, about
0.8% of comparisons would produce the same hash, which would require a full, slow equality check to be carried
out. So, if 99.2% of comparisons can be made fast, but 0.8% of comparisons are very slow, that represents a
significant improvement so long as the hash function itself is _fast_.

Modern computers are able to compare any two 32-bit integers equally fast, so the example above would not help a
computer in the same way as it helps a human. But hash functions can be defined for any kind of finite input,
such as strings, or files, or lists of objects.

## Hashing for storing data

Hash functions are useful for storing and accessing data fast. Consider another simple hash function on strings,
or the subset of strings that are people's names: we will hash every string to its first letter, ignoring case.
Assuming all inputs start with one of the 26 letters of the English alphabet, this yields a range of 26. For
example, `Smith` would hash to `S` and `Jackson` would hash to `J`.

We could use this hash function to file physical user records into an ordered set of folders. Storing a new
value would require calculating the hash, going directly to the folder for that letter, and then appending
the record to the end of the records already there.

Retrieving a record would require calculating the hash, going directly to the folder for that letter, and then
linearly searching through the records there to check for a match.

Of these two operations, every step can be completed in a constant time, regardless of how many records we are
storing, with the exception of the linear search upon retrieval, which would be dependent on how many records
were stored at that hash value. But the use of a hash function has removed any need to search through every
single record we store, and instead limited us to a linear search through just a few records.

But there are a few more observations we can make about this.

## Uniformity of Distribution

Firstly, Names are not evenly distributed through the alphabet, so there are many more people with names
beginning with "S" than there are people with names beginning with "Q". So the linear search to look up someone
called "Smith" in a store that already contains lots of data would probably take longer than a search for
someone called "Quentin".

That is a flaw in our hash function: its inputs are not evenly distributed over the range, with a
disproportionate number of inputs getting hashed to certain values. We could choose a different hash function
to try to make the distribution over the hash values more even, so that the time spent doing a linear search
through records would be roughly equal for any input.

Here is a suggestion:
```scala
def hash(str: String): Int = str.toUpperCase.map(_ - 64).sum%26
```

This hash function will assign the numbers 1-26 to each letter in the input, add them all up, and find the
remainder after dividing by 26. Here are some examples:

| Name    | Hash |
|---------|------|
| Gilmour | 17   |
| Smit    | 9    |
| Smith   | 17   |
| Smyth   | 7    |

Despite the similarity of "Smit", "Smith" and "Smyth", these names will all produce different hashes, while
seemingly-unrelated names "Gilmour" and "Smith" have the same hash. But in general, we would get a roughly even
distribution across the values `0` to `25` for a set of names.

A second observation, given that the slowest part of retrieval is the linear search through all values at a
particular hash value, is that this could be reduced by increasing the number of valid hash values (or folders
in our original example), and storing fewer records at each. We could find a new hash function with a range of
`0` to `999`, and if we were to store a thousand records, there would be an average of one record per hash
value. (Some would be empty, while others would have two or three records.) This would require more storage
space, but would offer faster retrieval.

## Collisions

When two values do hash to the same value, this is known as a _hash collision_ or just a _collision_. It's
generally considered undesirable, because it implies an additional cost _somewhere_ to disambiguate between
those two inputs. For hash functions with a small range, collisions are inevitable, and should not be considered
catastrophic. But if they occur too frequently, either by accident, or because a malicious user is deliberately
seeking to attack a running system, they can reduce the performance of hash lookups from constant time, on
average, to linear time, which could have serious performance implications.

## Cryptographic Hash Functions

The _MD5_ algorithm is another hash function which takes an arbitrary length input and produces a 128-bit hash,
often represented as 32 hexadecimal digits, for example, `54fb1a9ecc18bc71d53d6420deabcf69`.

This sequence of hexadecimal characters is like a fingerprint for the input, a file, which produced it.
Different inputs will produce different hashes, and there are
340,282,366,920,938,463,463,374,607,431,768,211,456 different possible MD5 hash values. Unlike the trivial hash
functions above, the range of MD5 is much larger. But by virtue of being finite, it is still smaller than the
infinite domain of possible inputs.

What this means is that there must exist multiple different inputs which produce the same MD5 hash, but the
range is so large, and hashes are distributed uniformly and unpredictably across that range that it is
infeasible to try to find multiple inputs which produce the same output, and such an event wouldn't happen by
chance.

This fact may be used to our advantage: it is usually sufficient to make the assertion that if two files had the
same MD5 hash, their content is identical; we can assume that the vanishingly small possibility that the two
files had different content which generated the same MD5 hash is actually zero.

The MD5 algorithm, like the various SHA algorithms, are _cryptographic_ hash functions. They are designed to
make it as hard as possible to find two different inputs which produce the same output, or to manipulate an
input by adding additional data to produce a specific desired hash.

## Hashing in Scala

All objects in Scala have a `hashCode` method, defined for each type, and intended to hash the state of that
object, in some way, to a 32-bit integer. The `hashCode` method is intimately related to the `equals` method:
if two values are considered equal, according to the `equals` method, then the `hashCode` method must produce
the same value. This invariant is relied upon in the Scala standard library, the Java standard library, and
throughout the ecosystems of both languages.

`hashCode` has a medium-sized range of 32-bits, and is not intended to be cryptographically secure. It's usually
difficult to find two different objects with the same `hashCode` value, but not impossible, and the risk of
a collision is real. So `hashCode` is useful for identifying a difference between objects, but is not sufficient
to identify that two objects are identical.