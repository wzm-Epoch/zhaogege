"""Check repository documents and submission layout without running member code."""

from pathlib import Path
import os
import re
import sys
from urllib.parse import unquote, urlsplit

MAX_FILE_SIZE = 10 * 1024 * 1024
FORBIDDEN_DIRS = {"node_modules", ".venv", "venv", "__pycache__", ".pytest_cache", ".ipynb_checkpoints"}
TASK_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*\Z")
USERNAME = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?\Z")
LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^\s)]+)")


def prose_only(text):
    """Ignore fenced and inline code, where paths are usually examples."""
    lines = []
    fence_char = None
    fence_length = 0
    for line in text.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            fence = marker.group(1)
            if fence_char is None:
                fence_char, fence_length = fence[0], len(fence)
            elif fence[0] == fence_char and len(fence) >= fence_length and not line[marker.end():].strip():
                fence_char = None
            lines.append("")
        elif fence_char is None:
            lines.append(re.sub(r"(`+).*?\1", "", line))
        else:
            lines.append("")
    return "\n".join(lines)


def check_repository(root):
    root = Path(root).resolve()
    errors = []
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(name for name in dirs if name != ".git")
        current = Path(directory)
        for name in list(dirs):
            path = current / name
            if name in FORBIDDEN_DIRS or path.is_symlink():
                errors.append(f"{path.relative_to(root)}: 不应提交依赖、缓存或符号链接目录")
                dirs.remove(name)
        for name in sorted(files):
            path = current / name
            relative = path.relative_to(root)
            if path.is_symlink():
                errors.append(f"{relative}: 不应提交符号链接文件")
                continue
            if path.stat().st_size > MAX_FILE_SIZE:
                errors.append(f"{relative}: 单个文件超过 10 MiB，请改用外部链接")
                continue
            if path.suffix.lower() != ".md":
                continue
            try:
                content = path.read_text(encoding="utf-8-sig")
            except UnicodeError:
                errors.append(f"{relative}: Markdown 文件应使用 UTF-8 编码")
                continue
            for line_number, line in enumerate(prose_only(content).splitlines(), 1):
                for match in LINK.finditer(line):
                    target = match.group(1).strip("<>")
                    try:
                        url = urlsplit(target)
                    except ValueError:
                        errors.append(f"{relative}:{line_number}: 链接格式无效：{target}")
                        continue
                    if url.scheme or target.startswith(("//", "#")) or not url.path:
                        continue
                    destination = (path.parent / unquote(url.path)).resolve()
                    if not destination.is_relative_to(root) or not destination.exists():
                        errors.append(f"{relative}:{line_number}: 本地链接目标不存在或超出仓库：{target}")

    assignments = root / "assignments"
    if assignments.is_dir() and not assignments.is_symlink():
        for task in sorted(assignments.iterdir()):
            if not task.is_dir() or task.is_symlink():
                continue
            if not TASK_ID.fullmatch(task.name):
                errors.append(f"assignments/{task.name}: 作业编号只能使用英文字母、数字、短横线和下划线，且以字母或数字开头")
            for member in sorted(task.iterdir()):
                if member.is_file():
                    if member.name != "README.md":
                        errors.append(f"{member.relative_to(root)}: 成员文件应放到 GitHub用户名 子目录")
                    continue
                if member.is_symlink() or not member.is_dir():
                    continue
                if not USERNAME.fullmatch(member.name) or "--" in member.name:
                    errors.append(f"{member.relative_to(root)}: 个人目录应使用有效的 GitHub 用户名格式")
                readme = member / "README.md"
                if not readme.is_file() or readme.is_symlink():
                    errors.append(f"{member.relative_to(root)}: 缺少 README.md 作业说明")
                else:
                    try:
                        if not readme.read_text(encoding="utf-8-sig").strip():
                            errors.append(f"{readme.relative_to(root)}: 作业说明不能为空")
                    except UnicodeError:
                        pass  # Encoding failure already reported in the document scan.
    return errors


if __name__ == "__main__":
    problems = check_repository(Path(__file__).resolve().parents[1])
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}")
        sys.exit(1)
    print("检查通过：本地文档链接、作业目录及文件基础规范无误。")
