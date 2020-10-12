from structure_loader import load_structure

STRUCTURE = load_structure()
LEVELS = STRUCTURE.levels

def test_topic_ranges_exist():
  topic_ids = [topic.id for topic in STRUCTURE.topics]
  for level in LEVELS:
    for topic_range in level.ranges:
      topic_id = topic_range.topic_id
      assert topic_range.topic_id in topic_ids, f"Topic with id {topic_id} doesn't exist (referenced in {level.course_id}/{level.level} level)"


def test_topic_ranges_lessons_exist():
  try:
    for level in LEVELS:
      for topic_range in level.ranges:
        topic = [topic for topic in STRUCTURE.topics if topic.id == topic_range.topic_id][0]
        lesson_ids = [lesson.id for lesson in topic.lessons]
        assert topic_range.lesson_start in lesson_ids,  (f"Lesson with id {topic_range.lesson_start} doesn't exist in topic {topic.id}" 
        f" (referenced in {level.course_id}/{level.level} topic range)")
        assert topic_range.lesson_end in lesson_ids,  (f"Lesson with id {topic_range.lesson_end} doesn't exist in topic {topic.id}" 
        f" (referenced in {level.course_id}/{level.level} topic range)")
  except IndexError:
    assert False, "Topic missing, detailed message in another test"

def test_ranges_order():
  try:
    for level in LEVELS:
      for topic_range in level.ranges:
        topic = [topic for topic in STRUCTURE.topics if topic.id == topic_range.topic_id][0]
        lesson_ids = [lesson.id for lesson in topic.lessons]
        start_index = lesson_ids.index(topic_range.lesson_start)
        end_index = lesson_ids.index(topic_range.lesson_end)
        assert start_index <= end_index, "Start lesson index must be less than or equal to end lesson index"
  except IndexError:
    assert False, "Topic missing, detailed message in another test"
