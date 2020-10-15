# ScalaZONE Content
This repository contains the content of the [ScalaZONE website](https://scala.zone). It stores both lesson text and course structure. Everyone is welcome to make PRs with suggestions [TODO contributing.md]

## Deployment triggers
 - Every commit to the `develop` branch updates the content on the development environment.
 - Every commit to the `stage` branch updates the content on the staging environment.
 - Every commit to the `master` branch updates the content on the production environment. [TODO: Rename master]
Only the production environment is accessible to the public. [TODO: add access for other people?]

## Structure overview

### Courses

Courses are the top-level entity in the ScalaZONE material structure. Their structure is stored in the [courses](/courses) directory. The [courses/index.json](/courses/index.json) file stores a list with all available courses. For each course there is a directory named after the course id that contains the course structure. Basic course data is stored in the `index.json` file in this directory. Here is the `Course` JSON type structure:

| Field name | Type            | Description                                                                            |
|------------|-----------------|----------------------------------------------------------------------------------------|
| `name`     | String          | Name of the course that is visible on the website                                      |
| `levels`   | List of strings | List of available levels of the course. Levels are described in the next paragraph     |
| `image`    | String          | Path to the image for the course; it has to refer to an image inside this repository   |
| `video`    | String          | Video link that is displayed on the course overview page                               |
| `desc`     | String          | Description of the course                                                              |
| `scope`    | List of strings | Scope of the course; these are presented in the bullet list on the course overview page|

### Course Levels

Course levels are parts of the course that are suited for users starting with different ability levels. There are three levels that are possible to add to a course:
 - Beginner
 - Intermediate
 - Advanced
To add a level to a course, it must be present in the `levels` field in the course's index.json file. Level can be configured using `<level>.json` file in the course directory, where `<level>` is either `beginner`, `intermediate` or `advanced`. Here is the `Level` JSON structure:

| Field name | Type                       | Description                                                |
|------------|----------------------------|------------------------------------------------------------|
| `name`     | String                     | Name of the course level that is visible on the level page |
| `desc`     | String                     | Description of the course level                            |
| `ranges`   | List of TopicRange objects | Defines lessons and topics that are present in the level   |

And the `TopicRange` type has the following structure in json:

| Field name    | Type   | Description                                               |
|---------------|--------|-----------------------------------------------------------|
| `topicId`     | String | Id of the topic                                           |
| `lessonStart` | String | Id of the first lesson of the topic included in the level |
| `lessonEnd`   | String | Id of the last lesson of the topic included in the topic  |

Topic ranges define what topics and lessons are present in a course level. By specifying this, we are able to use only a slice of a topic for a particular course level. These slices may, however, overlap between level, so that a particular lesson may appear in more than one level.

### Topics

Topics are ordered collections of lessons. Their index is stored in the [topics/index.json] file. The structure of a single topic is defined in the `index.json` file inside the specific directory named after the topic in the `topics` directory. This `index.json` file has following JSON structure:

| Field name | Type           | Description                                      |
|------------|----------------|--------------------------------------------------|
| `name`     | String         | Name of the topic that is visible on the website |
| `desc`     | String         | Description of the topic                         |
| `lessons`  | List of Lesson | Lessons that this topic consists of              |

The `Lesson` JSON type structure:

| Field name      | Type            | Description                                                  |
|-----------------|------------------|-------------------------------------------------------------|
| `id`            | String          | Id of the lessons                                            |
| `title`         | String          | Title of the lesson; the name that is visible on the website |
| `authorId`      | String          | Id of the lesson's author                                    |
| `duration`      | Int             | Expected duration of lesson completion in minutes            |
| `prerequisites` | List of String  | Ids of lessons that are prerequisites of this lesson         |

### Lessons

A lesson's content files are present in the topics directory, within a directory specific to the lesson's topic. The content file must be named after the lesson id and have a `.md` file extension. This file defines the text and questions that user sees after entering the lesson page. 
You can use most of the markdown features inside of it, including tables, images and a special syntax for videos.

#### Video syntax
To embed a video inside a lesson you can use the following syntax:

```md
[![alt text](alt image link)](embeddable video link)
```

#### Questions section

The first part of every lesson's markdown file is the lesson's content: the text that is visible on the lessons page, and is meant to explain a concept specific to this lesson. After this first part, it is possible to include questions testing the user's understanding at the end of the lesson. To do so, first introduce the questions section separator: `?---?` and write your questions after it. At this moment there are two types of questions: _single answer questions_ (using radio buttons) and _multiple answer questions_ (using checkboxes). Every question begins with a single-hash markdown header, for example:

```md
# What is 1+1?
```

It is possible to include code blocks, tables and other markdown elements that are not children of the header element, but they must follow the header element.

After the question text, you must provide the question's answer choices, by specifying an unordered markdown list. It can be defined either using dashes (`-`) or asterisks (`*`). However, the character you choose determines the type of the question. Dashes are used for single answer questions and asterisks for multiple answer questions. To indicate whether the answer is correct you should use the markdown checkboxes that follow the list character. Two examples below exemplify this behaviour:

Single answer question:
~~~md
# What is the result of expression below?

```
2+2
```

 - [ ] 3
 - [X] 4
 - [ ] 7
~~~

Multiple answer question:
~~~md
# What is the result of expression below?

```
2+2
```

 * [ ] 3
 * [X] 4
 * [ ] 7
 * [X] Four
~~~

To summarize, let's look on a sample lesson containing some mock content and two questions:

~~~md
# Arithmetic

## Addition

To add two numbers ...

## Substraction

...

?---?

# What is the result of the expression, `2+2`?

 - [ ] 3
 - [X] 4
 - [ ] 7

# What is the result of expression below?

```
2+2
```

 * [ ] 3
 * [X] 4
 * [ ] 7
 * [X] Four

```
~~~

### Authors

Courses' authors are defined in the [authors.json](/authors.json) file. This file contains a list of `Author` objects. The `Author` JSON object has following structure:

| Field name | Type             | Description                                 |
|------------|------------------|---------------------------------------------|
| `id`       | String           | Id of the author                            |
| `name`     | String           | Name that is presented on the website       |
| `order`    | Int              | The order of the author in the authors list |
| `twitter`  | String, Optional | Link to the author's twitter page           |
| `github`   | String, Optional | Link to the author's github page            |
| `desc`     | String           | Description of the author                   |
