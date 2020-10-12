from structure_loader import load_structure

STRUCTURE = load_structure()

def test_level_names():
  courses = STRUCTURE.courses
  for course in courses:
    for level in course.levels:
      assert level in ['beginner', 'intermediate', 'advanced'], f"Level {level} in course {course.id} must be either beginner, intermediate or advanced"
