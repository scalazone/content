In the previous lessons we talked about methods that are called `foreach`, `map` and `filter`. In this lesson you will learn about a more convenient way to work with these functions. At first it may seem that the construct you are going to learn about only makes your code look cleaner. However, it is one of the most important and commonly used features in the functional programming.

## The for comprehension

If you learned any high level programming languages in the past you probably have seen the `for` loop in some form. It is used to `iterate` in its most general meaning. You can use it to go over the elements of a collection, just like we did with the `foreach` statement, or you can just repeat some operation a couple of times. In Scala, the `for` expression is inherently connected to `foreach`, `map`, and `filter` methods. Given any composition of these methods, you are able to rewrite it in terms of a `for comprehension`. So let's try to make a `for` that prints all the elements in a List.

```scala
val list = List(1, 2, 3)
for
  i <- list
do println(i)
```

A couple of lessons ago we wrote code that does exactly the same operation, but using the `foreach` method:

```scala
List(1, 2, 3).foreach(value => println(value))
```

During the execution of the two code samples above, they both boil down to the same operations. This `for comprehension`
is replaced with a single `foreach` call that looks exactly the same as the second code snippet.

Let's focus on the keywords that we used in this `for comprehension`. The first one that we haven't seen before is
the `for` itself. It marks the beginning of the `for` expression and can be read as `For each`. Then, in the next line,
there is a tabulated `i <- list` statement. It can be understood as `value "i" in the list`. Adding these two pieces
together we end up with `For each value "i" in the list` - you must admit that at this point the meaning of this
sentence is pretty clear. The last line says `do println(i)`. Now we can rewrite this whole expressing using the english
language: `For each value "i" in the list do println "i"`. And it is exactly what it does on execution.

## Filtering

But what if we wanted to print only the even numbers in the `List`? Doing so with the collection methods would require calling the `filter` first, and then doing `foreach` on the resulting `List`. Just like in the example below:

```scala
def isEven(number: Int) = number % 2 == 0
val list = List(1, 2, 3, 4)

list.filter(isEven).foreach(println) // Outputs 2 and 4
```

It is still readable, but not as clean as it were before. However, for this case we can also use the `for comprehension` by introducing a new simple feature:

```scala
def isEven(number: Int) = number % 2 == 0
val list = List(1, 2, 3, 4)

for
  i <- list if isEven(i)
do println(i)
```

As you can see, we added the `if` expression next to the `i <- list`. It makes sure that only the elements that pass the condition given with `isEven` get assigned to `i`. We can still easily translate it directly to the english language: `For each value "i" in the list that isEven do println "i"`. 

## Multiple levels of iteration

Consider following problem: `Given two lists, print all the possible pairs of values from these Lists`. We can just dive in this problem using the knowledge from previous lessons and use the `foreach` expression two times:

```scala
val firstList = List('A', 'B', 'C')
val secondList = List('X', 'y', 'Z')

firstList.foreach(first => secondList.foreach(second = println(first.toString + second)))
```

For each element in `firstList` we obtain elements from `secondList` one by one and print them out together. It works correctly - we end up with all the possible pairs of letters from these two lists. We had to call `toString` method on first letter to avoid adding these two characters as numeric values and getting sum of their ASCII codes. However, it may take a while to figure out what this line of code is supposed to do. Even if you try to introduce some line splits, for example before calling the `foreach` on the secondList, it does not help that much and gets only worse when we add, for example, a third collection to iterate on. Once again, it is where the `for comprehension` comes to save the day.

If we wanted to print out all the letters in the `firstList` we would do it as follows. We won't repeat the initialization of `firstList` and `secondList` in the following code samples, so just assume they have the same values as in the previous code snippet. 

```scala
for
  letter <- firstList
do println(letter)
```

This example is essentially the same as the first example of `for comprehension` in this lesson. But that is not what we
want to do. We want to combine the letters from `firstList` with the letters from `secondList`. To achieve this we do
the following:

```scala
for
  firstLetter  <- firstList
  secondLetter <- secondList
do println(firstLetter.toString + secondLetter)
```

All we had to do is just write one more line before the `do` expression. You can also notice that the arrows in the code
are aligned - it is not required, but is often done to increase readability of the code. For each value in `firstList`
it will go through all the elements in the `secondList`. This will, once again, execute in exactly the same way as the
code using two `foreach` methods, but it is much more readable now. We can even do one more thing to make it look
better. We can extract the combined letters to a separate constant:

```scala
for
  firstLetter  <- firstList
  secondLetter <- secondList
  twoLetters   = firstLetter.toString + secondLetter
do println(twoLetters)
```

Using `=` instead of `<-` allows you to introduce a new constant. It works exactly like setting a new val, but it can be
set inside a `for` expression, between the `arrow expressions`. It is often used to avoid duplicating pieces of code, or
to extract parts of complicated expressions to separate lines.

Now imagine a case where we want to use only the upper case letters from the `secondList`. If we used the `foreach`
methods and then used a `filter` atop of them it would make a complete mess in the code! Instead, we just use the `if`
exactly like we did it before:

```scala
for
  firstLetter  <- firstList
  secondLetter <- secondList if secondLetter.isUpper
  twoLetters   = firstLetter.toString + secondLetter
do println(twoLetters)
```

## Yielding

All the code we wrote so far was only supposed to print out values. These `for comprehensions` were performing specified operation with values, and then totally forgetting about them. There is another approach that allows to execute the `for comprehension` and extract the specified values out of it. It is done using the `yield` keyword. All we have to do to use it is just replace the `do` with `yield` and not print the value, but just reference it instead:

```scala
val combinations = for
  firstLetter  <- firstList
  secondLetter <- secondList
  twoLetters   = firstLetter.toString + secondLetter
yield twoLetters
```

As a result, we get a List of expected combinations. Instead of printing them out, we just saved them to the `combinations` list for later use. Type of the returned collection is specified by the first collection used in the `arrow expression` - in this case the `firstLetter <- firstList`. Therefore, considering `firstList` type is a `List`, `combinations` is also assigned with a `List`. If we were to use a `Set` in the first line instead, we would get a `Set` of Strings. Moreover, in most of the cases you can mix the collection and, for example, use a Set of second letters instead of `secondList`. As the `Set` is unordered, it would change the order of the elements in the resulting `List` to random, but it would work perfectly well.
