# Data modeling

## Introduction

_Data modeling_ refers to the process by which we design and implement new data types that capture 
details relevant to the business.

For example, a shopping application might need data types to model items, shopping carts, orders, 
users, and other entities, all of which have to be designed and implemented.

Scala provides two very succint and powerful features for data modeling:

1. _Case Classes_. Case classes let us model entities that can be constructed with a fixed number of 
fields. For example, a user account entity might have an email address field and a password hash 
field.
2. _Enums_. Enumerations let us model entities that can be constructed in a fixed number of 
different ways. For example, a payment method entity might support two ways to construct it: either 
using bank account details, or using credit card details.

Together, case classes and enums provide a comprehensive solution for data modeling: no matter what 
entity you need to model, you can use some combination of case classes and enums to model it.

## Case Classes

### Definition

Case class data types are introduced by using the key phrase `case class`. This key phrase is 
followed by two important details:

1. The name of the new data type. This name is used to create a new type in Scala's type system, and
to create a new object, referred to as the _companion object_ of the case class.
2. A list of all the fields required to construct objects of this type. This list is called the 
_case class constructor_.

The following example defines a simple case class called `Person` that can be constructed using two fields (`name` 
and `age`):

```
case class Person(name: String, age: Int)
```

### Construction

In order to construct an object of type `Person`, we can use the name of the data type, followed by 
a list of values, one value for each field.

In this example, we construct a "John Doe" who is 42 years of age, by supplying the `String` and 
`Int` necessary to construct a `Person`:

```
val johnDoe = Person("John Doe", 42)
```

The type of the `johnDoe` value (which is an object) is `Person`, as we can verify by inserting a 
type annotation:

```
val johnDoe: Person = Person("John Doe", 42)
```

### Field Access

All fields declared in the case class can be accessed using dot notation on any object of this type. 
For example, to access the `name` field, we can use the following notation:

```
val name = johnDoe.name
```

Similarly, to access the `age` field, we can use the following notation:

```
val age = johnDoe.age
```

Another way we can extract out the fields of case class objects is by performing _pattern matching_ 
on the objects.

In the following example, we extract and print out the name and age of the `johnDoe` object:

```
johnDoe match
  case Person(name, age) =>
    println(s"Name: ${name}")
    println(s"Age : ${age}")
```

In another variation, we can extract out the fields of a case class object by using _destructing 
assignment_:

```
val Person(name, age) = johnDoe

println(s"Name: ${name}")
println(s"Age : ${age}")
```

### Features of Case Classes

Case classes come equipped with features that make them very useful for modeling data. In 
particular, they come with default definitions for the following methods:

 - `hashCode`. This method computes a "hash code" for an object (a kind of integer "fingerprint" 
 that tries to guarantee that different objects have different hash codes), based on the hash codes 
 of the field values. Objects that are equal must have the same hash code.
 - `==`. This method (pronounced "equals") does an equality check between two objects, which 
 operates on the `equals` method of the field values.
 - `toString`. This method generates a string representation of an object, based on the `toString` 
 of the field values.

These definitions allow case class objects to be used safely in certain collections, such as sets 
and maps, which require useful definitions of hash code and equality.

In the following snippet of code, we add two identical `Person` objects into a set, and then print 
out both the size of the set, as well as the contents of the set:

```
val set = Set(Person("Sherlock Holmes", 37), Person("Sherlock Holmes", 37))

println(s"Size    : ${set.size.toString}")
println(s"Contents: ${set.toString}")
```

When `toString` is called on the set, it uses the `toString` method of the `Person` objects, whose 
default implementation is provided by Scala. Without this default implementation, the `Person` 
object would print out a meaningless string representation, without any information on the field values.

The Scala `Set` type uses the equality and hash code methods of objects. Without these default 
definitions, the above set would have a size of 2, and it would contain two objects, which, even 
though they would have the "same" values for their fields, would compare as different.

## Enums

### Definition

Enum data types are introduced by using the keyword `enum`. This keyword is followed by two details 
that define the enumeration type:

1. The name of the new data type. This name is used to create a new type in Scala's type system, and
to create a new object, referred to as the _companion object_ of the enum.
2. One or more different constructors for the enum. These are referred to as the _cases_ of the 
enum, and they define _case classes_.

The following example defines an enum called `PaymentMethod` that can be constructed in two 
different ways:

```
enum PaymentMethod:
  case BankAccount(number: BigInt, swiftCode: String)
  case CreditCard(number: String, securityCode: Short, expMonth: Short, expYear: Short)
```

### Construction

In order to construct a `PaymentMethod`, we have two choices:

1. We can use the `BankAccount` constructor, which is stored inside the `PaymentMethod` companion 
object. This constructor allows us to create a `PaymentMethod` that holds bank account details.
representing a bank account.
2. We can use the `CreditCard` constructor, which is stored inside the `PaymentMethod` companion 
object. This constructor allows us to create a `PaymentMethod` that holds credit card details.

These are the only two ways to construct a `PaymentMethod`. Importantly, this implies if we have 
some value of type `PaymentMethod`, it is either a bank account, or a credit card&mdash;there are 
no other possibilities.

In the following snippet, we construct a payment method which is a bank account:

```
val payMethod1 = PaymentMethod.BankAccount(2397876232, "XKJFS232")
```

In the following snippet, we create another payment method which is a credit card:

```
val payMethod2 = PaymentMethod.CreditCard("2397876232", 232, 1, 12)
```

Both of these values have type `PaymentMethod`, as we can verify by inserting a type annotation:

```
val payMethod1: PaymentMethod = PaymentMethod.BankAccount(2397876232, "XKJFS232")
val payMethod2: PaymentMethod = PaymentMethod.CreditCard("2397876232", 232, 1, 12)
```

### Case Access

Accessing information from an enum value is more complicated than for a case class, because the 
enum value could have been constructed in completely different ways.

For example, if we have a value of type `PaymentMethod`, we do not know that it has a security code,
because that field only makes sense for `CreditCard` payment methods.

So in order to access information in an enum value, we must use _pattern matching_, which will both
tell us which case it is, and allow us to extract information from that case.

In the following snippet, we pattern match on `payMethod1`, and print out a message based on which
case we discover it to be:

```
payMethod1 match 
  case PaymentMethod.BankAccount(num, code) => 
    println(s"Number: ${num}")
    println(s"Swift:  ${code}")

  case PaymentMethod.CreditCard(_, _, _, _) =>
    println(s"Not expected!")
```

Of course, the first pattern match must be successful, because `payMethod1` was constructed using
the `BankAccount` constructor. However, because the `payMethod1` value has type `PaymentMethod`,
and because not every `PaymentMethod` was constructed using `BankAccount` (some values, like 
`payMethod2`, were constructed using `CreditCard`), we have to handle both cases.

### Features of Enums

Because the cases of an enum are in fact case classes, this means enum types come with default 
definitions for `hashCode`, `==`, and `toString`.

As for case classes, these default definitions allow enum objects to be used safely in certain 
collections, such as sets and maps, which require useful definitions of hash code and equality.

?---?
# Select which Scala 3 language features are designed for data modeling.

* [ ] Abstract Classes
* [X] Case Classes
* [X] Enums
* [ ] Givens
* [ ] Traits

# What will the following code snippet print out?

```
case class Person(name: String, age: Int)

println(Person("Mary Jane", 42) == Person("Mary Jane", 42))
```

 - [ ] `false`
 - [X] `true`

# What is the following assignment called?

```
val Person(name, age) = Person("John Doe", 42)
```

 - [ ] Annealing assignment
 - [X] Destructuring assignment
 - [ ] Pattern extraction assignment
 - [ ] Pattern matching assignment

# Choose the correct statement about the following code:

```
enum Color:
  case Red 
  case Green
  case Blue
  case Cutom(red: Int, green: Int, blue: Int)
```

 - [ ] Enums have no constructors
 - [ ] There are infinitely many constructors for the `Color` data type
 - [*] There are 4 constructors for the `Color` data type