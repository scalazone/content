from structure import *
import os
import json
from pathlib import Path
from envs import CONTENT_PATH

def load_structure():
  courses = load_courses()
  levels = load_levels(courses)
  topics = load_topics()
  authors = load_authors()
  return Structure(courses, levels, topics, authors)

def load_courses():
  try:
    courses_index_json = Path(CONTENT_PATH + "/courses/index.json").read_text()
    courses_index = json.loads(courses_index_json)
    return [load_course(course_id) for course_id in courses_index['courses']]
  except FileNotFoundError:
    assert False, f"Courses index file not found"
  except KeyError as e:
    assert False, f"Courses index file is malformed, cause: {repr(e)}" 

def load_course(course_id: str):
  try:
    path = CONTENT_PATH + f"/courses/{course_id}/index.json"
    course_json = Path(path).read_text()
    course = json.loads(course_json)
    return Course(course_id, course['name'], course['levels'], course['image'], 
                  course['video'], course['desc'], course['language'], course['scope'])
  except FileNotFoundError:
    assert False, f"Index file not found for course {course_id}"
  except KeyError as e:
    assert False, f"Course {course_id} index is malformed, cause: {repr(e)}" 

def load_levels(courses: [Course]):
  return [load_level(course.id, level) for course in courses for level in course.levels ]

def load_level(course_id: str, level_id: str):
  try:
    path = CONTENT_PATH + f"/courses/{course_id}/{level_id}.json"
    level_json = Path(path).read_text()
    level = json.loads(level_json) 
    ranges = [TopicRange(range['topicId'], range['lessonStart'], range['lessonEnd']) for range in level['ranges']]
    return Level(level_id, course_id, level['name'], level['desc'], ranges)
  except FileNotFoundError:
    assert False, f"Level {level} file not found for course {course_id}"
  except KeyError as e:
    assert False, f"Level {level} file for course {course_id} is malformed, cause: {repr(e)}" 

def load_topics():
  try:  
    topics_index_json = Path(CONTENT_PATH + "/topics/index.json").read_text()
    topics_index = json.loads(topics_index_json)
    return [load_topic(topic_id) for topic_id in topics_index['topics']]
  except FileNotFoundError:
    assert False, f"Topics index file not found"
  except KeyError as e:
    assert False, f"Topics index is malformed, cause: {repr(e)}" 

def emptyIfNone(array):
  return [] if array == None else array

def load_topic(topic_id: str):
  try:
    path = CONTENT_PATH + f"/topics/{topic_id}/index.json"
    topic_json = Path(path).read_text()
    topic = json.loads(topic_json) 
    lessons = [Lesson(lesson['id'], topic_id, lesson['title'], lesson['authorId'], lesson['duration'], 
              [LessonPrereq(prereq['lessonId'], prereq['topicId']) for prereq in emptyIfNone(lesson.get('prerequisites'))]) 
              for lesson in topic['lessons']]
    return Topic(topic_id, topic['name'], topic['desc'], lessons)
  except FileNotFoundError:
    assert False, f"Topic {topic_id} index not found"
  except KeyError as e:
    assert False, f"Topic {topic_id} index is malformed, cause: {repr(e)}" 

def load_authors():
  try:
    path = CONTENT_PATH + "/authors.json"
    authors_json = Path(path).read_text()
    authors = json.loads(authors_json)
    return [Author(author['id'], author['name'], author['order'], author.get('twitter'), 
            author.get('github'), author['desc']) for author in authors]
  except FileNotFoundError:
    assert False, "authors.json file not found"
  except KeyError as e:
    assert False, f"Authors file is malformed, cause: {repr(e)}" 
