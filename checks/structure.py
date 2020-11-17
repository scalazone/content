from dataclasses import dataclass

@dataclass
class Course:
  id: str
  name: str
  levels: [str]
  image: str
  video: str
  desc: str
  language: str
  scope: [str]

@dataclass
class TopicRange:
  topic_id: str
  lesson_start: str
  lesson_end: str

@dataclass
class Level:
  level: str
  course_id: str
  name: str
  desc: str
  ranges: [TopicRange]

@dataclass
class Lesson:
  id: str
  topic_id: str
  title: str
  author_ids: [str]
  duration: int
  prereqs: [str]

@dataclass
class LessonPrereq:
  lesson_id: str
  topic_id: str

@dataclass
class Topic:
  id: str
  name: str
  desc: str
  lessons: [Lesson]

@dataclass
class Author:
  id: str
  name: str
  order: int
  twitter: str
  github: str
  desc: str

@dataclass
class Structure:
  courses: [Course]
  levels: [Level]
  topics: [Topic]
  authors: [Author]
