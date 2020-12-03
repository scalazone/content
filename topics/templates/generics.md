Some of the classes are general enough to be used with multiple types of values. Example of this could be the `List`
class - it does not hold multiple different implementations for storing integers, Strings and other types. All that has
to be done to make the `List` suit an arbitrary type is specifying it with the parameter between the square brackets.
This parameter is called a *type parameter* and the class that expects a type parametr is a *generic class*.

## Writing a generic class

So far we were only using generic classes that were already written in the standard library. Now, we can try and spend some time writing our own generic class - a Pair. Pair can hold two values at once - `right` and `left`. For now, let's implement it in a way that both values have to be of the same type. Without generics we could write the following using just the `Any` type:

```scala
class Pair(right: Any, left: Any)
```

Despite being able to store value of any kind, using Any type poses a major problem - you cannot retrieve any of these values with their actual type. To change that, we can introduce a type parameter `T`:

```scala
class Pair[T](right: T, left: T)
```

Now we can use it to both store values of any type and access them without a need of performing an unsafe downcast afterwards. For example, let's create a `Tuple` of ints and access one of its values:

```scala
val intPair = Pair[Int](1, 3)
val rightInt = intPair.right // rightInt type is Int
```

In fact we could skip the Int type parameter and write only `Pair(1, 3)` with the same result. Scala can  infer types of the type parameters automatically, given values of these types are present as constructor parameters.

## Multiple type parameters

Just like with the constructor parameters, we can introduce multiple type parameters. In our case it will allow us to use `Pair` with two different types, one for the right, and one for the left value. We just have to include it in the square brackets.

```scala
class Pair[A, B](right: A, left: B)
```

Now, we can create a Pair of, for example, a `String` and a `Double`:

```scala
val stringAndFloat = Pair("Abc", 0.21)
val right = stringAndFloat.right // a String
val left = stringAndFloat.left // an Int
```

Once again, we used Scala's automatic type inference to initialize the Pair with correct type parameters. Of course there is nothing stopping us from doing it explicitly and writing it as `Pair[String, Double]("Abc", 0.21)`.

## Using type parameters inside the class

Type parameters can be used in the whole class body, including functions. Therefore it is possible and common to create functions that use these passed types. Let's use this information that converts our `Pair` to a Scala's predefined tuple.

```scala
class Pair[A, B](right: A, left: B):
    def asTuple: (A, B) = (right, left)
```

After using it we can see that the types are all being preserved:

```scala
val pair = Pair(3, "Abc")
val tuple = pair.asTuple // tuple's type is (Int, String) 
```
