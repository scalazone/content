from structure_loader import load_structure

STRUCTURE = load_structure()

def test_lesson_unique():
  for topic in STRUCTURE.topics:
    lessons = [lesson.id for lesson in topic.lessons]
    # it's n^2 but we won't be having more than 20 lessons in topic at this moment
    duplicates = list({lesson for lesson in lessons if lessons.count(lesson) > 1}) 
    for duplicate in duplicates:
      assert False, f"Lesson {duplicate} is duplicated in topic {topic.id}"

def to_level_ordinal(level: str):
  return {
    'beginner': 0,
    'intermediate': 1,
    'advanced': 2
  }.get(level)


def test_prerequisites():
  lesson_and_topic_to_lowest_level_ordinal = {}
  course_to_lesson_and_topic_id = {}
  lesson_and_topic_to_course = {}
  for course in STRUCTURE.courses:
    course_lesson_ids = []
    course_levels = filter(lambda level: level.course_id == course.id, STRUCTURE.levels)

    for level in course_levels:
      level_ordinal = to_level_ordinal(level.level)

      for topic_range in level.ranges:
        topic = [topic for topic in STRUCTURE.topics if topic.id == topic_range.topic_id][0]
        topic_lesson_ids = [lesson.id for lesson in topic.lessons]
        start_index = topic_lesson_ids.index(topic_range.lesson_start)
        end_index = topic_lesson_ids.index(topic_range.lesson_end) + 1
        range_lessons = topic_lesson_ids[start_index:end_index]
        range_lessons_with_topic = map(lambda l_id: (l_id, topic.id), range_lessons)
        course_lesson_ids.extend(range_lessons_with_topic)

        for lesson_id in range_lessons:
          current_lesson_level = lesson_and_topic_to_lowest_level_ordinal.get((lesson_id, topic.id))
          if current_lesson_level == None or current_lesson_level > level_ordinal:
            lesson_and_topic_to_lowest_level_ordinal[(lesson_id, topic.id)] = level_ordinal
          lesson_and_topic_to_course[(lesson_id, topic.id)] = course.id

    if course_to_lesson_and_topic_id.get(course.id) == None:
      course_to_lesson_and_topic_id[course.id] = course_lesson_ids
    else:
      course_to_lesson_and_topic_id[course.id].extends(course_lesson_ids)

  for topic in STRUCTURE.topics:
    for lesson in topic.lessons:
      if lesson.prereqs != None:
        for prereq in lesson.prereqs:
          prereq_doesnt_exists_msg = f"Lesson's {topic.id}/{lesson.id} preqrequiste {prereq.topic_id}/{prereq.lesson_id} doesn't exist"
          assert (prereq.lesson_id, prereq.topic_id) in lesson_and_topic_to_course.keys(), prereq_doesnt_exists_msg
          same_course_failed_msg = f"Lesson's {topic.id}/{lesson.id} preqrequiste {prereq.topic_id}/{prereq.lesson_id} doesn't exist at the lesson's course"
          assert lesson_and_topic_to_course[(lesson.id, topic.id)] == lesson_and_topic_to_course[(prereq.lesson_id, prereq.topic_id)], same_course_failed_msg
          lower_ordinal_failed_msg = f"Lesson's {topic.id}/{lesson.id} preqrequiste {prereq.topic_id}/{prereq.lesson_id} is on higher level that the {topic.id}/{lesson.id}"
          assert lesson_and_topic_to_lowest_level_ordinal[(lesson.id, topic.id)] >= lesson_and_topic_to_lowest_level_ordinal[(prereq.lesson_id, prereq.topic_id)], lower_ordinal_failed_msg
            
      