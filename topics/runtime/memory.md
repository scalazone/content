## The Heap and the Stack

All data that is used by a running JVM—values, objects, arrays—will be stored in one of two places: on the
_heap_, a large block of memory, parts of which may be allocated by the JVM when needed, or in the _stack_,
a special data structure which stores the current position in a running program, and the history of how it got
there, along with certain local variables. If a program has several threads running concurrently, each one will
have its own stack.

Stack and heap sizes vary, but a typical JVM configuration on a 64-bit computer will use 1MB for each stack,
while the heap may be anything from about 100MB to the entire system memory.

Blocks of system memory, which is normally accessed like a big array—indexed by an offset from the start—will
be allocated to the JVM by the host operating system when it starts up. But from the perspective of a program
running inside the JVM, these regions of memory are never presented transparently as _addressable_ memory.

## Allocation

Instead, memory is automatically _allocated_ on the heap when we create a new array, or instantiate an object,
and instead of using a numerical index to access values on the heap, Scala provides us with _references_ to them
in the form of named identifiers.

So when we write,
```scala
val element = Element()
```
the JVM will find an empty region of its heap memory large enough to store an `Element` object (and an object of
a particular type will have a known size), and will modify the bytes in that region to store the new `Element`.
This is called the  _instantiation_ of the object; it is creating an _instance_ of the object. Having done so,
the JVM will return the address of the start of the `Element` instance in memory.

## Opaque Pointers

But that _address_, specifically the index of the memory containing the object, is completely opaque from within
the JVM to the Scala (or Java) code we write. Throughout our code, we refer to that instance by an symbolic
identifier, and never by a number, even though ultimately, that reference _is_ just a number which points to a
position in memory. But from within our program, it's inaccessible. We can't read it or change it; we can't
compare it to another reference, except to check if they are equal or different. We can't have our program
behave differently depending on a reference, except by equality check against another reference.

Opaque references offer a big benefit to safety. With no means to manipulate (or even see) a reference, it
becomes impossible to access arbitrary memory locations from within a program running on the JVM, either
deliberately or by accident. We therefore can never access or manipulate any memory that has not been explicitly
designated for that purpose, such as an array of bytes: doing so could make it possible to change the runtime
behavior of the JVM in unsafe, unpredictable, insecure or undesirable ways.

This "restricted" memory interface, which makes it impossible for a JVM program to depend on implementation
details of the JVM, allows different implementations to be used. Different computer systems with different CPU
architectures, 32-bit or 64-bit, and different operating systems with different memory allocation schemes, can
all host a JVM with their own memory management implementation, but the view from a program running inside any
of those JVMs will be the same. These implementations can also evolve (for example, with performance
improvements) over time, without affecting the _correctness_ of the programs which run within them, even if
their performance characteristics change.

## Garbage Collection

We have looked at how memory from the heap is assigned to objects in the JVM, but heap memory is a finite and
sometimes scarce resource. Once all the memory available to the operating system has been allocated to objects
(either directly, or as part of arrays) attempts to construct more objects will fail, because no further heap
memory can be found in which to store them.

This would result in a failure, which would usually be difficult to recover from. But thankfully, memory is only
allocated from the heap for as long as it is needed. Once a region of memory containing an object or an array of
objects is no longer required, its contents can be deleted and the memory made available again as free space.
This recovery happens automatically, and it means that an application running in the JVM can run for a long
time, constructing new objects over and over again, and as long as it stops using objects about as fast as it is
creating them, and the total number of "active" objects at any time isn't growing indefinitely, the program can
keep running forever.

This automatic recovery of unused objects is called _garbage collection_. But we need to consider what it means
for an object to be "no longer used". How does the JVM decide? How can it be certain, and what if we try to
access the memory location of an object that has already been garbage collected?

The simple answer is that the JVM will, from time to time, pause everything—all the running threads—and scan
the entire heap and the stack of every thread to find objects on the heap to which there are no references
elsewhere. If the entire memory of the JVM contains no references to an object, and the JVM provides us with no
way of accessing an object "directly" by its memory address, there is simply no opportunity to involve such an
object in any future computation. And therefore it is safe to delete it, and mark the memory it previously used
as free to use again.

## A Worked Example

So, we cannot explicitly destroy objects on the JVM; we can only remove all references to them. That can happen
when a mutable field containing a reference to an object is changed to a different reference, or when a local
variable in the stack is discarded.

Here is a contrived example:

```scala
def example: String =
  var str = "one"
  // Point A
  str = "two"
  // Point B
  str = str + " three"
  // Point C

  "four"
```

We can't predict when the garbage collector process will pause execution, and collect unreferenced objects. It
could happen at point A, B or C, or more than one of these (though that is practically unlikely in this
example).

At point A, we have a reference to the `String` object `"one"`, but the reference to it is still accessible
through the identifier `str`, so the garbage collector cannot safely remove it. At point B, `str` is still
accessible, but the reference to the object `"one"`, which still exists on the heap, has been replaced by a
reference to the object `"two"` (somewhere else on the heap). So the garbage collector will find zero
references to `"one"` but one reference to `"two"`, which means it can delete the object `"one"` and free up the
memory it was using. At point C, we have constructed a new `String` object, namely `"two three"` using the
`String` `+` method. That takes the reference to the original `str` object (`"two"`) and the `" three"` object
as parameters, and combines them to produce a new `String` object, and "consumes" the objects `"two"` and
`" three"` in the process: their references and removed from the stack when the new `String` is returned. So
a garbage collector running at point C would collect the objects `"one"`, `"two"` and `" three"`.

The beauty of this design, in practise, is that we usually don't need to think about it. We can just _expect_
memory to be freed up when it's possible to do so, and we never need to worry about it.

We do, however, need to be careful about accidentally leaving references to objects that we no longer intend to
refer to in data structures such as sets and maps. Merely having these references (within other objects) is
enough to prevent them from ever being garbage collected. If this is unintended, it is usually called a
_memory leak_ because the effect is a gradual, continuous, undesirable loss of heap memory, as garbage
collection fails to delete objects we would otherwise expect it to.

## GC Pauses

Garbage collection occurs every so often, whenever the JVM decides it is necessary or beneficial. That's not
something that can be controlled by a program running in the JVM. Sometimes we would like to have more control
over the process, because unfortunately, the "pause" which happens while the garbage collector is running—which
may be 5ms or 5000ms in some extreme cases—can be detrimental to a user's experience of our software: it may
look unresponsive, or "jittery".

In practice, the garbage collection pauses are so small that they would barely be noticed by users, and the
longer, more apparent pauses occur only when running code which creates very large numbers of objects. A common
approach to improving the performance of our code is to try to write it in ways which do not produce so many
objects, as it will typically save time on both constructing objects and garbage collecting.

In order to minimize the time spent garbage collecting, the heap is split into several regions. Many objects
are very ephemeral (short-lived) which means that the first time the garbage collector sees them, there may
already be no remaining references to them. Such objects are created in a part of the heap called _Eden space_
within the _young generation_. A shorter, quicker garbage collection run can check the _Eden space_, removing
all these ephemeral objects, while those still referenced are said to "survive", and are promoted—and
moved—into a different region called _survivor space_. Objects which survive for some time in _survivor space_
will be considered long-lived objects, and moved to _tenured space_.

This, however, is just an optimization, designed to minimize the impact of garbage collection.

?---?

# Which of the following describe parts of the JVM's memory? (Note that some may be overlapping regions.)

* [X] Tenured space
* [X] Survivor space
* [X] Young Generation
* [X] The Heap
* [ ] Garbage
* [X] The Stack
* [X] Eden space

# Garbage collection of JVM objects happens:

- [ ] When the objects are left unused in collections for a period of time
- [X] When no references to those objects exist
- [ ] After having spent a period of time in survior space
- [ ] At regular intervals

# Does the string `"Hello"` exist as an object on the heap at the point marked `Z`, in the following code?

```scala
object Main:
  val x = "Hello"
  var y = x+" World!"
  y = ""
  // Z
```

- [X] Yes
- [ ] No
- [ ] Maybe, or maybe not; it may have been garbage collected already
