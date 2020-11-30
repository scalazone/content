import glob
import re

from envs import CONTENT_PATH
from pathlib import Path

CODE_SNIPPET_INDICATOR = "```"
QUESTION_SECTION_INDICATOR = "?---?"
topcis_root = CONTENT_PATH + "/topics"


def test_lesson():
  files = f"{topcis_root}/*/*.md"
  mds = glob.glob(files)
  for md in mds:
    try:
      lesson_text = Path(md).read_text()
      question_section_index = lesson_text.find(QUESTION_SECTION_INDICATOR)
      if question_section_index != -1:
        question_section_content = lesson_text[question_section_index + len(QUESTION_SECTION_INDICATOR):]
        validate_question_section_content(md, question_section_content)
    except FileNotFoundError:
      assert False, f"Lesson file '{md}' not found"
    except KeyError as e:
      assert False, f"Lesson file '{md}' is malformed, cause: {repr(e)}"


def validate_question_section_content(md, content):
  unsnippified_content = remove_code_snippets(md, content)
  sanitized_content = sanitize(unsnippified_content)
  validate_question_indicators(md, sanitized_content)
  question_contents = re.split(r"\n#", "\n" + sanitized_content)
  if len(sanitized_content) > 1:
    for question_content in question_contents[1:]:
      validate_question_answers(md, question_content)


def remove_code_snippets(md, content):
  code_snippet_indicator_indices = [m.start() for m in re.finditer(CODE_SNIPPET_INDICATOR, content)]
  if len(code_snippet_indicator_indices) % 2 == 1:
    assert False, f"Unmatched code snippet indicator ('```') in lesson file '{md}'"
  begs = [0] + list(map(lambda x: x + len(CODE_SNIPPET_INDICATOR), code_snippet_indicator_indices[1::2]))
  ends = code_snippet_indicator_indices[::2] + [len(content)]
  content_ranges = list(zip(begs, ends))
  unsnippified_content = "".join([content[a:b] for a, b in content_ranges])
  return unsnippified_content


def sanitize(unsnippified_content):
  lines = unsnippified_content.split("\n")
  no_empty_lines = filter(lambda x: not re.match(r"^\s*$", x), lines)
  stripped = map(lambda x: x.strip(), no_empty_lines)
  return "\n".join(stripped)


def validate_question_indicators(md, content):
  invalid_question_indicators = [m.start() for m in re.finditer(r"#{2,}", content)]
  if invalid_question_indicators:
    assert False, f"Invalid question indication (multiple '#') in lesson file '{md}'"


def validate_question_answers(md, question_content):
  question_content_lines = question_content.split("\n")
  single_answer_options = parse_single_answer_options(question_content_lines)
  multi_answer_options = parse_multi_answer_options(question_content_lines)

  if single_answer_options.all_count > 0 and multi_answer_options.all_count > 0:
    assert False, f"Found both single- and multi- answer options in the question, file '{md}'"

  if single_answer_options.all_count == 0 and multi_answer_options.all_count == 0:
    assert False, f"Found no answer options in the question, file '{md}'"

  if single_answer_options.checked_count > 1:
    assert False, f"Multiple answers checked in the single answer question, file '{md}'"
  elif single_answer_options.all_count > 0 and single_answer_options.checked_count == 0:
    assert False, f"No answer checked in the single answer question, file '{md}'"

  if multi_answer_options.all_count > 0 and multi_answer_options.checked_count == 0:
    assert False, f"No answer checked in the multi answer question found, file '{md}'"


def parse_single_answer_options(question_lines):
  unchecked_options = list(filter(lambda x: re.match(r"^- \[ ]", x), question_lines))
  checked_options = list(filter(lambda x: re.match(r"^- \[[xX]]", x), question_lines))
  return AnswerOptions(unchecked_options, checked_options)


def parse_multi_answer_options(question_lines):
  unchecked_options = list(filter(lambda x: re.match(r"^\* \[ ]", x), question_lines))
  checked_options = list(filter(lambda x: re.match(r"^\* \[[xX]]", x), question_lines))
  return AnswerOptions(unchecked_options, checked_options)


class AnswerOptions(object):
  def __init__(self, unchecked, checked):
    self.checked_count = len(checked)
    self.unchecked_count = len(unchecked)
    self.all_count = self.unchecked_count + self.checked_count
