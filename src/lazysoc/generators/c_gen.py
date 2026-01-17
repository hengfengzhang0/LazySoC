"""C Header 代码生成器"""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from lazysoc.parser import Block


def get_template_dir() -> Path:
    """获取模板目录路径"""
    return Path(__file__).parent.parent / "templates"


def generate_c_header(block: Block) -> str:
    """
    生成 C Header 文件

    Args:
        block: 解析后的 Block 对象

    Returns:
        生成的 C Header 代码
    """
    env = Environment(
        loader=FileSystemLoader(get_template_dir()),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("c_header.h.j2")
    return template.render(block=block)


def write_c_header(block: Block, output_path: Path) -> None:
    """生成并写入 C Header 文件"""
    content = generate_c_header(block)
    output_path.write_text(content, encoding="utf-8")
