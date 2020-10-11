# The Java Virtual Machine

Scala code runs inside the _Java Virtual Machine_, or _JVM_. The JVM is designed to look like a "machine" while
we are writing code to run on it, but it is not actually a machine in the traditional sense, as the different
parts of the JVM do not necessarily correspond directly to real, physical hardware. It is an abstraction.

The benefit of this abstraction is that it allows code to run predictably on different hardware and different
operating systems, without requiring us to write different versions of our software for different systems.
Instead, we write our code once, and different implementations of the JVM for different operating systems and
processor architectures translate our code into native code when we run it.

The goal of the JVM, often described as "write once, run anywhere," remains imperfect for more complex software,
as some operating systems are so fundamentally different in certain ways that the JVM cannot provide a unified
abstraction for them. For example, Windows uses the backslash (`\`) character to split file paths, whereas Linux
and Mac OS use the slash (`/`) character. The way we manipulate a String which represents a file path will need
to be different for Windows and Linux or Mac OS, though libraries can help to hide the differences.

But to the extent that the JVM is capable of providing a consistent virtual representation of a machine, it is
extremely useful to save us having to consider many of the subtle differences that exist between different
computer systems.

When we talk about "The JVM" we usually mean one of two things. Either we are referring to the design and
architecture of the virtual machine, or we are talking about a particular _instance_ of a JVM that is running
our code; because a JVM is just a program that runs on a computer. We can launch it, and it will run for some
time, and then (maybe) it will finish, much like a web browser, for example. We can have more than one JVM
running on the same computer at the same time. From the point of view of the operating system which hosts the
JVM, it is a normal program which runs alongside other programs, but for a program running _within_ the JVM, it
has no awareness that it is anything less than a complete "machine". This is similar in some ways to how
[Docker](https://docker.com/) works.

It is called the _Java_ Virtual Machine because it was designed primarily for running code written with the
[Java](https://www.oracle.com/java/technologies/) programming language. The architecture of the virtual machine
was designed to naturally accommodate many of the features of Java, but nothing about the JVM specification
precludes other languages from running on it, and even interacting with code written in other JVM languages,
such as Java, [Kotlin](https://kotlinlang.org/) and [Groovy](https://groovy-lang.org/).

## Java Bytecode

It is possible for the JVM to host code written in different languages only because they all use the same
low-level intermediate language to represent code: _Java Bytecode_. Every JVM language uses a compiler, like
`javac` or `scalac`, to transform the human-readable source code into Java Bytecode, sequences of instructions
which perform CPU and memory operations, to interact with the virtual machine. The process of transformation of
source code into bytecode is called _compilation_.

All valid Scala source code can be compiled to Java bytecode instructions. There are 202 valid instructions,
which means that a single byte of 256 possible values can represent any instruction, and a sequence of bytes
can represent a sequence of instructions, which can also take parameters in the form of additional bytes. As
every modern computer architecture is optimized for operations on byte-sized data, this makes it compact and
efficient for reading, writing, distribution and also execution.

The instructions that bytecode represents include operations such as arithmetic and logical operations on
numbers and primitive types, conversions between them, construction and manipulation of objects, invocation of
methods, loading and storing of data in memory, control flow operations and instructions to manipulation the
execution stack, the data structure which keeps track of _where_ execution is happening in a running program. We
will learn more about the stack later.

Some of these, such as subtraction of two integers, can be seen to correspond directly to our Scala source code,
while others, such as transferring control to a different part of the program, may only be indirectly related
to our source code. Thankfully, we rarely need to understand all the details of Java bytecode, or how source
code translates to it. But we should remember that ultimately, everything we write in Scala will be converted
to a lower-level, more restricted set of commands, which operate in a virtual machine in which many of the
concepts that are important in Scala are no longer modeled directly.

Java bytecode is organized into many _classfiles_, each of serves as a blueprint for constructing new type of
object. All executable bytecode must belong to a class or object, so all the code we compile from Scala source
code will go into one classfile or another.

The `javap` tool, which is bundled with the Java Development Kit (JDK) allows us to inspect the bytecode for any
class, in a format which is low-level, but still readable. Here is an example of the bytecode for a simple
"Hello, World!" application written in Java:

```jvm
0: getstatic      #2  // Field java/lang/System.out:Ljava/io/PrintStream;
3: ldc            #3  // String Hello, World!
5: invokevirtual  #4  // Method java/io/PrintStream.println:(Ljava/lang/String;)V
8: return
```

We won't try to understand this fully, but will at least look at how to read this output. The numbers at the
start of each line indicate the byte offset of each instruction. So they start at zero, and are incremental,
but not necessarily monotonic, as some instructions take one or more additional bytes for their parameters. The
instructions themselves, `getstatic`, `ldc`, `invokevirtual` and `return` perform operations, with indices to
elements in the _constant pool_, a part of a classfile containing fixed values like strings and method
references. At the end of each line, `javap` will lookup these references and show them to us.

This particular bytecode can be interpreted as follows:
 - `getstatic #2` puts a reference to the value specified at constant pool index 2, `java.lang.System.out` which
   is a `java.io.PrintStream` onto the stack
 - `ldc #3` loads the constant at index 3, `"Hello, World!"`, onto the stack
 - `invokevirtual #4` calls the method `java.io.PrintStream#println(_: java.lang.String): Unit` (whose
   parameters are already on the stack)
 - `return` terminates the method

This sequence of commands will cause the words `Hello, World!` to be printed as output when the method is invoked.

And that invocation happens because when the JVM is launched, we must specify, as a parameter, the classfile to
run. Every time we launch a new JVM, we must specify the name of a class as the "entry point" to an application.
The JVM will expect to find a method called `main` in the class, but in Scala, we can just write a top-level
method (with any name) and annotate it with the `@main` annotation, like this,
```scala
package helloworld

@main
def run(): Unit = println("Hello, World!")
```
and Scala will generate a classfile called `helloworld/run.class`, corresponding to the class, `helloworld.run`,
which will contain a `main` method which will be invoked when we launch a new JVM.

We can achieve that with Fury by running,
```sh
fury module update --type app --main helloworld.run
fury
```
or directly using the `scala` command,
```sh
scala -classpath <classpath> helloworld.run
```
where `<classpath>` is the directory containing the compiled application.

Although a full understanding of Java bytecode is not necessary to write good Scala code, at the very least we
should always remember that it is ultimately what our source code will become, and there will be times when the
limitations of bytecode have an impact on the way we write Scala, particularly when we care about its
performance.

?---?

# True or false? The Java Virtual Machine is an ordinary program the runs on a computer system.
- [X] True
- [ ] False

# True or false? All JVM instructions are one byte long (excluding parameters).
- [X] True
- [ ] False

# True or false? Java bytecode instructions map directly to Scala keywords.
- [ ] True
- [X] False

# True or false? A Java classfile contains only Java bytecode.
- [ ] True
- [X] False

# True or false? Compilation is the process by which Scala source code is converted into bytecode.
- [X] True
- [ ] False