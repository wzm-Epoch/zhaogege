"""Exercise valid submissions and common mistakes in disposable directories."""

import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("checker", Path(__file__).resolve().parents[1] / "scripts/check_repository.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class RepositoryChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def check(self):
        return checker.check_repository(self.root)

    def test_valid_submission_and_chinese_encoded_link(self):
        self.write("assignments/task-001/octocat/README.md", "# 作业\n![结果](%E7%BB%93%E6%9E%9C.png)\n")
        self.write("assignments/task-001/octocat/结果.png", "image fixture")
        self.assertEqual(self.check(), [])

    def test_broken_link_reports_line(self):
        self.write("README.md", "# 标题\n[缺失](missing.md)\n")
        self.assertTrue(any("README.md:2" in error for error in self.check()))

    def test_ignores_examples_and_remote_links(self):
        self.write("README.md", "`[示例](missing.md)`\n```md\n[x](missing.md)\n```\n~~~\n[x](missing.md)\n~~~\n[x](https://example.com)\n[x](#title)\n")
        self.assertEqual(self.check(), [])

    def test_link_cannot_escape_repository(self):
        self.write("README.md", "[外部](../outside.md)")
        self.assertTrue(any("超出仓库" in error for error in self.check()))

    def test_missing_or_empty_submission_readme(self):
        self.write("assignments/task-001/octocat/main.py", "print('hello')")
        self.assertTrue(any("缺少 README.md" in error for error in self.check()))
        self.write("assignments/task-001/octocat/README.md", " \n")
        self.assertTrue(any("不能为空" in error for error in self.check()))

    def test_invalid_task_member_and_loose_file(self):
        self.write("assignments/中文任务/bad--name/README.md", "# 作业")
        self.write("assignments/中文任务/main.py", "pass")
        errors = self.check()
        self.assertTrue(any("作业编号只能" in error for error in errors))
        self.assertTrue(any("用户名格式" in error for error in errors))
        self.assertTrue(any("成员文件应放到" in error for error in errors))

    def test_dependency_directory(self):
        self.write("node_modules/package/index.js", "")
        self.assertTrue(any("依赖、缓存" in error for error in self.check()))

    def test_large_file(self):
        path = self.write("large.bin", "")
        with path.open("wb") as stream:
            stream.truncate(checker.MAX_FILE_SIZE + 1)
        self.assertTrue(any("超过 10 MiB" in error for error in self.check()))

    def test_invalid_utf8(self):
        self.write("README.md", "").write_bytes(b"\xff")
        self.assertTrue(any("UTF-8" in error for error in self.check()))


if __name__ == "__main__":
    unittest.main()
