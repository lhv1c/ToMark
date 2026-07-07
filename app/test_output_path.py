import os
import tempfile

from paths import resolve_output_path


def test_no_conflict():
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "doc.pdf")
        open(src, "w").close()
        assert resolve_output_path(src) == os.path.join(d, "doc.md")


def test_one_conflict():
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "doc.pdf")
        open(src, "w").close()
        open(os.path.join(d, "doc.md"), "w").close()
        assert resolve_output_path(src) == os.path.join(d, "doc (1).md")


def test_multi_conflict():
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "doc.pdf")
        open(src, "w").close()
        open(os.path.join(d, "doc.md"), "w").close()
        open(os.path.join(d, "doc (1).md"), "w").close()
        assert resolve_output_path(src) == os.path.join(d, "doc (2).md")


if __name__ == "__main__":
    test_no_conflict()
    test_one_conflict()
    test_multi_conflict()
    print("ok")
