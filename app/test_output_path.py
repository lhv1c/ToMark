import os
import tempfile

from paths import next_selection, resolve_output_path


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


def test_next_selection():
    assert next_selection(1, 0) is None      # lista fica vazia
    assert next_selection(3, 0) == 0         # some o 1o: o proximo assume
    assert next_selection(3, 1) == 1
    assert next_selection(3, 2) == 1         # some o ultimo: volta um
    assert next_selection(2, 1) == 0


if __name__ == "__main__":
    test_no_conflict()
    test_one_conflict()
    test_multi_conflict()
    test_next_selection()
    print("ok")
