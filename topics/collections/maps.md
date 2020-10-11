# Maps

Everyone who ever used a language dictionary or a phone book has come to contact with a real-life example of a data structure that is called a `Map` or a `Dictionary` in programming. In case of the `List` and `Vector`, the values are accessible by indices that are integers and intuitively represent the "location" of the elements. `Map` is a collection where these `indices` get a much broader nature. They can be of any type you want them to. These new `indicies` are called the `keys` - because you use them to access `values` in your `Map`. For example, you could create a `Map` with the phone numbers of your friends. To get a phone number out you would need to enter a name of your friend. So let's visualize this example with a table:

| Name  | Phone number |
|-------|--------------|
| Adam  | 564 333 215  |
| Emma  | 522 264 788  |
| Harry | 578 855 362  |
| Alice | 631 845 045  |

If you want to know a Adam's number you just look at the left column, find Adam's row and read the number on the right. `Map` works exactly the same way. So let's rewrite this structure to the Scala code:

```scala
val phoneNumbers = Map(
    "Adam"  -> "564 333 215",
    "Emma"  -> "522 264 788",
    "Harry" -> "578 855 362",
    "Alice" -> "631 845 045"
)
```

Just like with the table, keys are on the left side and point to the values on the right. If you want to access any of the elements in the `Map` you can do it in two ways. The first one is by calling the `get` method on a `Map` and it is considered to be a good pratice to do it that way. It returns an `Option` type that is `Some` containing the value if the key was found, and `None` if it was not found. Below you can see the example of this.

```scala
val adamNumber = phoneNumbers.get("Adam") // equals to Some(...)
val none = phoneNumbers.get("Pablo") // equals to None
```

Another way of accessing Map's element is by calling the `Map` as you would call a function - and indirectly calling the `apply` method on it. The significant difference between this method and calling `get` method is that this method throws a `NoSuchElementException` when element can not be found. It is considered a bad pratice to call a method that throws an exception when there is an alternative that handles the problem in more convenient and meaningful way - in this case it is calling the `get` method and dealing with possilbility of receiving a `None` from it.

## Modyfing the Map

### Adding the elements

To add a new key-value element to a Map you can use a `+` operator. As a side note - remember that immutability is the default behaviour of Scala collections and modyfing is in fact creating a new, modified `Map` and returning it. Syntax for adding a new elements to Map is straightforward as you can see in example below.

```scala
val updatedNumbers = phoneNumbers + ("John" -> "755 224 143)
```

### Removing an element

`-` operator allows the removal of elements from the `Map`. Elements are removed by key, so removing phone number to `Harry` could be written in the Scala code as follows:

```scala
val withoutHarry = phoneNumbers - "Harry"
```

### Joining Maps

If you have two Maps and you want to join them together you can use `++` operator. Remember that they are required to have conforming types of keys and values. 

```scala
val anotherPhoneNumbers = Map(
    "Jackson" -> "782 432 858",
    "Evelyn" -> "684 363 431"
)

val joinedMaps = phoneNumbers ++ anotherPhoneNumbers
```

If two joined Maps share some keys but store different values for them, all these values will be overwritten by values from the map on the right side of the `++` operator. 