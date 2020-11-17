from structure_loader import load_structure

STRUCTURE = load_structure()

def test_author_exists():
  author_ids = list(map(lambda author : author.id, STRUCTURE.authors))
  for topic in STRUCTURE.topics:
    for lesson in topic.lessons:
      for author_id in lesson.author_ids:
        assert author_id in author_ids, f"Lesson {lesson.topic_id}/{lesson.id} author {author_id} is not included in authors.json file"
