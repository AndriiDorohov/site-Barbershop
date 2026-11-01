"""Detect malformed HTML nesting before browser rendering masks the problem.

Browsers try to recover from mismatched closing tags. This can silently move
elements in the DOM and break styling even when basic end-to-end tests pass.
"""

from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent
VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


class StrictNestingParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID_ELEMENTS:
            self.stack.append((tag, self.getpos()))

    def handle_startendtag(self, tag, attrs):
        # Self-closing tags never enter the open-element stack.
        pass

    def handle_endtag(self, tag):
        if tag in VOID_ELEMENTS:
            self.errors.append(f"Unexpected closing void tag </{tag}> at {self.getpos()}")
            return
        if not self.stack:
            self.errors.append(f"Extra closing </{tag}> at {self.getpos()}")
            return
        open_tag, position = self.stack[-1]
        if open_tag != tag:
            self.errors.append(
                f"Mismatched </{tag}> at {self.getpos()}; "
                f"expected </{open_tag}> opened at {position}"
            )
        else:
            self.stack.pop()


class HTMLStructureTests(unittest.TestCase):
    def test_index_has_matching_tags(self):
        parser = StrictNestingParser()
        parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
        parser.close()
        unclosed = [f"<{tag}> at {pos}" for tag, pos in parser.stack]
        self.assertEqual(parser.errors, [], "\n".join(parser.errors))
        self.assertEqual(unclosed, [], "Unclosed tags: " + ", ".join(unclosed))


if __name__ == "__main__":
    unittest.main()
