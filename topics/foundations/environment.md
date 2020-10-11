# Our Environment

Before we start programming in Scala, we will need a working environment in which we can write, edit, compile
and run Scala code.

We will assume that we are going to start with a working computer running either _Linux_, _Mac OS X_ or
_Windows_. The software development experience will be depend on the operating system we use, but once we have a
working setup, our day-to-day development will look very similar, whichever operating system we use, and however
our computer is configured.

The general process for developing Scala will typically involve the following:
- creating or editing plain text files containing Scala source code, stored on the computer's hard disk
- running the Scala compiler, either directly, or using a build tool to invoke it to convert source code into
  runnable binary code
- executing the binary code

We are working hard to make the setup process easier for everyone with a one-step installation, but in the
meantime, we will look at the steps that need to be done to get a computer ready to perform these everyday
tasks.

## Editing files

There are many applications which can be used to edit Scala source files, and while most users will choose an
integrated development environment (IDE) such as [Visual Studio Code](https://code.visualstudio.com/) or
[IntelliJ IDEA](https://www.jetbrains.com/idea/), the only essential requirement is that the
choice of editor should be able to edit text as _plain text_, and is not a _rich text_ editor.

This means that tools such as [Sublime Text](https://www.sublimetext.com/), [Atom](https://atom.io/) are
perfectly suitable, as are the terminal-based editors [Vim](https://www.vim.org/) and
[Emacs](https://www.gnu.org/software/emacs/), or even
[Notepad](https://www.microsoft.com/en-us/p/windows-notepad/9msmlrh6lzf3) on Windows, whereas a rich text editor
such as Microsoft Word would not be appropriate: Scala source code will be interpreted by the Scala compiler,
`scalac`, which means that additional text styling information—which is stored in proprietary formats alongside
the text in some file formats—can confuse the compiler because it does not know how to interpret it.

When we write a Scala source file, we should give it a name which ends with `.scala`, such as `defs.scala` or
`Server.scala`. The name should be short, descriptive, and will commonly match the name of a class or object
defined within it, though that is not a rule, and it's often convenient to put several definitions in the same
file.

Source files are normally stored within a directory called `src`, sometimes organized into a hierarchy to make
the files easier to manage. The directory structure for source files is a matter of personal preference.

We recommend using Visual Studio Code with the
[Metals](https://marketplace.visualstudio.com/items?itemName=scalameta.metals) and _Ferocity_ extensions for
developing Scala.

## The Terminal

Many operations involved with software development will require interaction with the computer through a
_terminal emulator_, or simply, a _terminal_. This is a piece of software which allows us to type commands, at a
_command prompt_, such as,
```sh
find src | grep scala
```
and have them interpreted by the _command shell_, or just _shell_, which can start and stop applications, and
control their input and output. This particular command will find all the files inside the folder called `src`
whose names contain the string, `scala`.

There are a variety of different shells available, though the most common are _bash_, _zsh_ and _fish_. These
(and others) may offer a variety of different features, but all are capable of executing all of the commands we
need to run in this course.

A computer can run many terminals at the same time, each with its own shell representing an interactive—and
independent—session between a human developer and the computer. A terminal is also commonly called the
_console_, particularly from a perspective where it is known without ambiguity _which_ terminal we refer to. For
example, when we run a Scala program inside a terminal, the terminal it runs in is usually called "the console",
because it cannot easily (and does not make sense to) interact with any other terminals that might be running
at the same time.

The programs we write in this course will all be run within a terminal, initiated by entering a command at the
command prompt, and started by the shell. Output from running the programs will be displayed in the terminal.

Every operating system provides terminal software which can be used for this purpose. (Sometimes this will be
called a _terminal emulator_, because it behaves like an old physical terminal which would have historically
connected to a mainframe computer system, despite being just software _emulating_ hardware.)

Mac OS X provides a default terminal simply called _Terminal_, whereas Windows has a built-in application called
_Command Prompt_, and offers a more modern terminal called _Windows Terminal_. Different distributions of Linux
will come bundled with different terminals, for example _Ubuntu_ provides _Gnome Terminal_. Other Linux
distributions may provide different terminals, any it may be necessary to check the documentation for a
particular distribution of Linux, though most Linux users will have already encountered a terminal through
everyday activities.

## Compiling Scala 3

The Scala compiler, `scalac`, is a program which can be run (or _executed_) from the terminal to convert source
code into _bytecode_, which can be run. This conversion process is called _compilation_, and in addition to
generating runnable bytecode, it will perform a number of checks on the source code to ensure that it makes
sense, and is self-consistent.

We generally say that the compiler is checking the _correctness_ of the code, though this term can be slightly
misleading: the concept of "correctness" is limited to what the compiler knows, and while it can check every
usage against every definition, it cannot check that every definition correctly corresponds to the design brief
or specification written in natural language that the compiler can't understand.

The compilation step is, however, very good at finding many kinds of accidental mistake that would be difficult
for a human to notice, and presenting these in a convenient list not only describing the problem, but directing
us to its location within the source code so we can fix it.

Not all programming languages require a compilation step: many allow source code to be run _directly_. This can
be a convenience in some cases, but code written in such languages invariably runs more slowly (which may not be
a serious problem), and will not discover correctness errors until the incorrect code is run. This compilation
step is hugely advantageous to Scala developers because it can catch the majority of common programming errors
before any code is even run. Conversely, that can give us a lot more confidence that when our code _compiles_
successfully, it will also _run_ successfully.

We can compile some simple Scala 3 code by running `scalac`, and passing it paths to source files as arguments,
like so:
```scala
scalac src/app.scala src/data.scala src/core.scala
```

This will either compile the files successfully and produce a number of `.class` files, containing bytecode, in
the current directory, or it will report one or more compile errors, without producing any output files.

The `scalac` command has a lot of options that may be specified when we invoke it on the terminal, and it can be
used for small projects, but it quickly becomes impractical for larger projects, and it's typical to use a
dedicated build tool to compile and run Scala code.

## Build tools

There are several build tools which work with Scala, and while full details of how each works is beyond the
scope of this tutorial, it is easy to get started compiling Scala with
[Fury](https://propensive.com/opensource/fury), [Mill](http://www.lihaoyi.com/mill/) or
[sbt](https://www.scala-sbt.org/1.x/docs/Basic-Def.html).

A build tool is a program, like `scalac`, but which performs a number of other high-level activities as well as
compilation. These include:
- orchestrating multi-stage compilations, where some parts of the software should be compiled _after_ others
- resolving and managing dependencies on other third-party libraries
- incremental compilation, for compiling only the parts of the source code which have changed since the previous
  compilation
- sharing and publishing software for so other developers can use it.

While using the `scalac` program can remove a lot of uncertainty about compilation—it does _nothing_ more than
converting source files into bytecode—it is not necessary to have it installed if we use Fury, Mill or sbt:
these build tools will include everything necessary to compile Scala source code themselves.

## Getting started

### Start a terminal

First, we will need a terminal.

#### Mac OS X

On Mac OS X, we simply need to find and launch the program called _Terminal_.

#### Windows

On Windows, we will need to install the _Windows Subsystem for Linux 2_ (WSL2). This provides an environment
that will behave like a Linux computer, despite running under Windows. 

The [installation instructions](https://docs.microsoft.com/en-us/windows/wsl/install-win10) on Microsoft's
website explain how to install WSL2. We need to make sure that WSL*2* is chosen and not WSL*1*. For the choice
of which distribution of Linux to install, Scala can be used with any of the options available in the Windows
Store, but _Ubuntu_ is a good choice. It is also recommended to install
[Windows Terminal](https://docs.microsoft.com/en-us/windows/terminal/get-started).

If everything worked correctly, we should be able to launch a new WSL2 terminal, and enter commands at the
prompt. Entering the command,
```sh
uname
```
should simply produce the output,
```sh
Linux
```
(even though we are using Windows!) so if the terminal reports an error that `uname` is not recognized, it
probably means that the terminal that is running is a "PowerShell" or "Command Prompt" terminal, and not a
_WSL2_ terminal.

#### Linux

Different distributions of Linux, such as _Ubuntu_, _Fedora_, _Arch_ or _NixOS_ can come with completely
different setups, with different software installed, and different graphical user interfaces. The terminal we
use will depend on our distribution of Linux, though thankfully, using the terminal is a common requirement for
many tasks on Linuk, so it should not be difficult to find.

A few common Linux terminals are:
- `xterm`
- URxvt
- Alacritty
- Konsole

and any one of these will be suitable for developing in Scala. However, in case of any doubt, documentation for
the particular distribution of Linux should provide information on finding the terminal.

### Install Fury

Fury offers one of the easiest ways to start programming in Scala. It can be installed from a terminal with the
command:
```sh
curl -Ls https://fury.build | sh
```

This will install Fury, and once we restart our terminal, it will be available to use. We can test this by
running the command,
```sh
fury about
```
which should print a message similar to this:
```sh
     _____
    / ___/__ __ ____ __ __
   / __/ / // // ._// // /
  /_/    \_._//_/  _\_. /
                   \___/

Fury build tool, version 0.18.9-11-gbcf2b631, built 13:16:09 5 October 2020
This software is provided under the Apache 2.0 License.
Fury depends on Bloop, Coursier, Git and Nailgun.
© Copyright 2018-20 Jon Pretty, Propensive OÜ.

See the Fury website at https://fury.build/, or follow @propensive on Twitter
for more information.

    CPUs: 8
  Memory: 44.2MB used, 195.8MB free, 240.0MB total, 3.5GB max


For help on using Fury, run: fury help
```

### Install Visual Studio Code and Metals

Follow the instructions to download and install [Visual Studio Code](https://code.visualstudio.com/download),
then install the [Metals](https://marketplace.visualstudio.com/items?itemName=scalameta.metals) plugin from the
VS Code Marketplace.

