## Introduction

In the previous lessons you learned about `Vector`, `List`, and the `Set` collections with basics of operating on them. In fact, scala equips you with a rich assortment of functions that enable you to perform various operations on them. In this lesson we will cover the most common of these functions. It is important for you to keep in mind that `Vector` and `List` share most of their functions. Following examples will present them with a `List` type, but all of them can be used with a `Vector` as well.

## Initializing Collections

### Vector and List

One of the most useful initialization methods on the `List` and the `Set` collection is the `fill` method. Just like its name suggests it fills the collection with some element. It receives two `curried` parameters: `n` and `elem`. `n` indicates size of the collection and the `elem` is the element you want the collection to be filled with. For example:

```scala
val fivesList = List.fill(4)(5)
```

The code above makes a new list that contains four `5` values. It is equivalent of writing `List(5, 5, 5, 5)` or `5 :: 5 :: 5 :: 5 :: Nil`.

Another way of creating a `List` or `Vector` with custom values is by using the `tabulate` method. It is used when expected List values can be deducted from their indices. It expects specifying the size of the array you create and a function of type `Int => A`, where `A` is the type of wanted list elements. This function is called for each index of the List being created and then the resulting value is stored at this index. For example, when you want to get a `List` of 100 first squares of natural numbers you  could write it as follows:

```scala
val hundredFirstSquares = List.tabulate(100)(x => x * x)
```

`range` function allows initialization of collections storing ranges of numbers. It receives two or three arguments. Its basic from requires passing `start` and `end` numbers and returns a collection that contains all the numbers in between - including the `start`, but excluding the `end`. For example if you wanted to create a `List` containing `1, 2, 3, 4` values you could call the `range` function in following way:

```scala
val rangeList = List.range(1, 5)
```

The second form of this function allows to pass a `step` parameter as well. It specifies the difference between two consecutive elements in the resulting array. For example, code below would result in a `List` containing `1, 3, 5, 7` values:

```scala
val rangedList = List.range(1, 9, 2)
```

There is an useful Scala function that can be used to achieve the same result but in a simpler way. You have to use the `to` method that is offered by integer types in Scala. There is one problem with this function - it returns `Seq` type that we didn't see it anywhere before. For now you can convert it to `List` or `Vector` by calling `toList` or `toVector` method on it, just like in this example:

```scala
val rangedSeq = 1 to 5
val rangedList = rangedSeq.toList
```

It allows specyfing the `step` size exactly like the `ranged` method. You have to use the `by` method to achieve this:

```scala
val rangedSeq = 1 to 9 by 2 // evaluates to [1, 3, 5, 7]
```

### Sets

When working with `Set` it is important to remember that it is unable to store duplicated values. For this reason, function such as `fill` wouldn't make sense for `Set` structure. However, functions `tabulate` and `range` work exactly the same for set and you can call them the same way you would do for the other collections:

```scala
val firstSquaresSet = Set.tabulate(100)(x => x * x)
val rangedSet = Set.range(1, 5)
```

If a call to `tabulate` method results in a multiple repeating values or if you just add an element that already is present in the `Set`, the value will be stored only once. If you think about it, that behaviour can be even useful in some cases.

## Conversions

If you ever come to a situation that requires you to change your `List` or `Vector` to a `Set`, you can do so by simply calling `toSet` method on them. Bear in mind that all the repeating values will be stored only once in the resulting `Set`.

```scala
val setFromList = list.toSet
```

You can do this the other way around by calling `toList` or `toVector` method on the `Set`:

```scala
val listFromSet = set.toList
val vectorFromSet = set.toVector
```

You can assume that methods for similar conversions are present on most of the collection types, as long as it makes sense to convert between them.

## Iterating over the collections

In computer programming the term `iteration` describes the process of repeating some given instruction or a set of instruction. Very often it refers to going over all the elements in a collection and performing an operation on each of them. You can think about it as accessing all the elements in the collection one by one and using each of them in your own defined operations. Scala defines mutiple of function to describe these `iterating` operations. The most basic of these functions is called `foreach` and receives a function as an argument. This function will be called on each element of the collection. It is often used for operations such as printing out all the values inside the `List` - the code below does exactly that.

```scala
List(1, 2, 3).foreach(value => println(value))
```

After executing this code you would see values `1`, `2`, and `3` appearing in subsequent lines in your terminal.

### Mapping

All of this gets much more interesting when you face a situation that requires you to alter contents of the collection. A method that is very similiar to `foreach`, but simultaneously modifies the values it iterates on, is called the `map`. It also requires passing a fuction that receives collection element as a argument, but also returns some value. This value is then stored in the place of the previous value - the one that was passed to the function as an argument. Consider the case when you need to add 1 to each element of the array. To do so you need to access each element, add one to it, and then store it in the place of the element that you operated on. In Scala it is as simple as executing the following code. Once again - remember that all these operations work on most of the Scala collections, including `Vector` and `Set`.

```scala
val list = List(1, 2, 3, 4)
val listPlusOne = list.map(value => value + 1)
```

As the result, `listPlusOne` consists of `2, 3, 4, 5` values.

### Filtering

Ok, but let's say you want to do something that changes the length of the collection, such as filtering the odd numbers out of the `List`. For this operation you can use a method called `filter`, that receives a function as an argument just like the `map`, but expects it to return a `boolean`. This boolean's value specifies whether a given value should be kept in the result list. So, for example, if you want to get only the even numbers out of the `List` you can do it as follows:

```scala
def isEven(number: Int) = number % 2 == 0

val list = List(1, 2, 3, 4)
val evenNumbers = list.filter(value => isEven(value)) // TODO: Should we just pass the function and skip param? What is more readable for a beginner?
```

### Folding

Folding is a name for the general concept of combining values of your collection together to form another value. You can think about it as the process rolling an actual piece of cloth - you take one end of the material and continuously combine it into a single roll. You do a similar thing with a `collection` when you want to sum all of its elements. You go over it while adding a new elements into the resulting value - this value is often called the `accumulator` and abbreviated as `acc`. `fold` function in scala performs this "rolling" process. It takes two carried arguments. The first one is the initial value of the `accumulator` - that is the value that you will start the folding with, and then combine it with subsequent elements. The second argument is the function that describes the way in which the folding will be performed - whether the accumulator will be summed with elements, multiplied, or maybe even something completely different and custom. For now we can just stick with taking the sum of all values in a `List`. The folding start with a zero at the beginning and then is increased by each element. Therefore, it can be written this way:

```scala
val list = List(1, 2, 3, 4)
val sum = list.fold(0)((acc, element) => element + acc)
```

It is very useful that the initial value of the accumulator can be set. If you wanted to use `0` as initial value for multiplying all elements in a collection you would just end up with a zero. Instead, you can set it to `1` and everything will work as expected. There is also another method that assumes that the first element in the collection should be the initial value of the accumulator. This function is called `reduce` and it does not require passing the first argument. However - remember that it will throw an exception when used on an empty array, as it won't be able to deduce what to return.

All the folding operations that were covered in this lesson only allow to operate on one type - the type of elements in the collection. However, what if you want to store different type of value in the accumulator? Example of this would be converting a `List` of integers into a `String`. To do so you need to introduce `directionality` in the folding method. Methods for directional folds are called `foldRight` and `foldLeft` and they specify *from* which direction you intend to perform the fold operation. To be specific: `foldRight` folds the collections starting from the *right*, going to the *left*. Default `fold` method internally calls the `foldLeft` method, therefore folds from *left* to the *right*. Having this possible ambiguity covered, let's focus on a piece of code that converts a `List` of ints to a `String` containing space-separated numbers:

```scala
def appendToString(acc: String, elem: Int) = 
    acc + " " + elem.toString

val list = 1 :: 2 :: 3 :: Nil
val asString = list.foldLeft("")(appendToString)
```

To keep the code cleaner we extracted the second `fold` method argument to a separate function. As a result, `asString` will be set to ` 1 2 3`. Inconveniently, the method appended space also before the first element. You can drop it by using `tail` method on String.

What if we decide to use the `foldRight` function? Let's check that!

```scala
def appendToString(elem: Int, acc: String) = elem.toString + " " + acc

val list = 1 :: 2 :: 3 :: Nil
val asString = list.foldRight("")(appendToString)
```

Notice the inverted order of arguments in the `appendToString` function. It is meant to better represent the direction of folding. In this case `asString` has a value of `1 2 3 ` after performing the fold. The only difference is the location of the unwanted space - in this case it landed at the end of the String. You may be confused by the result, but think about it for one moment. `foldRight` method takes elements from the right and, as written in our `appendToString`, function puts them at the beggining of the accumulator on each step. Us inverting the order of values in the `appendToString` method was all that was required to keep the order of values in the resulting String correct.

## Summary

There is no point trying to remember all the methods defined on the collection types. In fact, even the most experienced Scala developers would struggle with listing all of them perfectly. However, it is very helpful to remember what operations Scala collections offer in general and to understand the concepts on which they operate. If you ever find yourself struggling to perform some operation that you can't get your head around, try going back to the basic operations that you learned about in this lesson. And do not hesistate scrolling through the offical Scala documentation on collections.
