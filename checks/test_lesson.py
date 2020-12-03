import glob
import json
import re

import commonmark
from envs import CONTENT_PATH
from pathlib import Path

CODE_SNIPPET_INDICATOR = "```"
QUESTION_SECTION_INDICATOR = "?---?"
topics_root = CONTENT_PATH + "/topics"


def test_lesson():
  files = f"{topics_root}/*/*.md"
  mds = glob.glob(files)
  for md in mds:
    try:
      lesson_text = Path(md).read_text()
      ast = commonmark.Parser().parse(lesson_text)
      json_objects = json.loads(commonmark.dumpJSON(ast))

      qsi_index = derive_question_section_indicator_index(md, json_objects)

      if qsi_index:
        question_section_content = json_objects[qsi_index + 1:]
        validate_question_section_content(md, question_section_content)
    except FileNotFoundError:
      assert False, f"Lesson file '{md}' not found"
    except KeyError as e:
      assert False, f"Lesson file '{md}' is malformed, cause: {repr(e)}"


def derive_question_section_indicator_index(md, json_objects):
  qsi_index = None
  is_qsi = lambda x: x["literal"] == QUESTION_SECTION_INDICATOR
  for i in range(len(json_objects)):
    partial_sum = sum(map(lambda x: 1 if is_qsi(x) else 0, filter(is_text, json_objects[i]["children"])))
    if partial_sum > 1 or (partial_sum == 1 and qsi_index):
      assert False, f"Multiple question section indicators ('?---?') found in file '{md}'"
    elif partial_sum == 1:
      qsi_index = i
  return qsi_index


def validate_question_section_content(md, content_objects):
  content_objects = list(map(remove_code_blocks, content_objects))
  content_objects = remove_empty_paragraphs(content_objects)
  validate_question_indicators(md, content_objects)
  question_answer_options_groups = derive_question_answer_options_groups(md, content_objects)
  for group in question_answer_options_groups:
    validate_question_answers(md, map(lambda i: content_objects[i], group))


def remove_code_blocks(content_object):
  is_not_code_block = lambda v: v["type"] != "code_block"
  return filter_object_recursively(content_object, is_not_code_block)


def remove_empty_paragraphs(content_objects):
  is_not_empty_node = lambda o: o["type"] != "paragraph" or (o["type"] == "paragraph" and o["children"])
  result = []
  for content_object in content_objects:
    result.append(filter_object_recursively(content_object, is_not_empty_node))
  return [r for r in result if is_not_empty_node(r)]


def filter_object_recursively(content_object, pred):
  if "children" in content_object.keys():
    proceeded_children = list(map(lambda x: filter_object_recursively(x, pred), content_object["children"]))
    content_object["children"] = [v for v in proceeded_children if pred(v)]
  return content_object


def validate_question_indicators(md, content_objects):
  for content_object in content_objects:
    if content_object["type"] == "heading":
      if any(map(lambda x: x["type"] == "heading", content_object["children"])):
        assert False, f"Invalid question indication (multiple '#') in lesson file '{md}'"


def derive_question_answer_options_groups(md, content_objects):
  def is_item_node(object):
    return len([i for i, v in enumerate(object["children"]) if
                "list_data" in v.keys() and v["list_data"]["type"] == "bullet"]) > 0

  def is_heading_node(object):
    return len([i for i, v in enumerate(object["children"]) if v["type"] == "heading"]) > 0

  is_valid_item_node = lambda x: is_item_node(x)
  heading_indices = [i for i, v in enumerate(content_objects) if is_heading_node(v)]
  headings_len = len(heading_indices)
  answer_options_groups = []
  for i in range(headings_len):
    beg = heading_indices[i] + 1
    end = heading_indices[i + 1] if i + 1 < headings_len else len(content_objects)
    item_indices = [i + beg for i, v in enumerate(content_objects[beg:end]) if is_valid_item_node(v)]

    if not item_indices:
      assert False, f"Found a question without answer options in lesson file '{md}'"

    answer_options_groups.append(item_indices)
  return answer_options_groups


def validate_question_answers(md, question_contents):
  get_bullet_char = lambda x: \
    list(map(lambda x: x["list_data"]["bullet_char"], filter(lambda x: x["type"] in ["item", "list"], x)))[0]
  write_text = lambda x: (get_bullet_char(x["children"]),
                          "".join(map(lambda x: x["literal"], filter(is_text, x["children"]))))
  answer_options_texts = list(map(lambda x: " ".join(list(x)), map(write_text, question_contents)))
  single_answer_options = parse_single_answer_options(answer_options_texts)
  multi_answer_options = parse_multi_answer_options(answer_options_texts)

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


def is_text(x):
  return x["type"] == "text"


def parse_single_answer_options(answer_options_texts):
  unchecked_options = list(filter(lambda x: re.match(r"^- \[ ]", x), answer_options_texts))
  checked_options = list(filter(lambda x: re.match(r"^- \[[xX]]", x), answer_options_texts))
  return AnswerOptions(unchecked_options, checked_options)


def parse_multi_answer_options(answer_options_texts):
  unchecked_options = list(filter(lambda x: re.match(r"^\* \[ ]", x), answer_options_texts))
  checked_options = list(filter(lambda x: re.match(r"^\* \[[xX]]", x), answer_options_texts))
  return AnswerOptions(unchecked_options, checked_options)


class AnswerOptions(object):
  def __init__(self, unchecked, checked):
    self.checked_count = len(checked)
    self.unchecked_count = len(unchecked)
    self.all_count = self.unchecked_count + self.checked_count
