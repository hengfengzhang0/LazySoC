"""SystemVerilog 代码生成器"""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from lazysoc.parser import Block


def get_template_dir() -> Path:
    """获取模板目录路径"""
    return Path(__file__).parent.parent / "templates"


def generate_sv_package(block: Block) -> str:
    """
    生成 SystemVerilog package

    Args:
        block: 解析后的 Block 对象

    Returns:
        生成的 SystemVerilog 代码
    """
    env = Environment(
        loader=FileSystemLoader(get_template_dir()),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("sv_package.sv.j2")
    return template.render(block=block)


def generate_sv_apb_slave(block: Block) -> str:
    """
    生成 APB4 Slave 模块

    Args:
        block: 解析后的 Block 对象

    Returns:
        生成的 APB4 Slave 模块代码
    """
    env = Environment(
        loader=FileSystemLoader(get_template_dir()),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("sv_apb_slave.sv.j2")
    return template.render(block=block)


def write_sv_package(block: Block, output_path: Path) -> None:
    """生成并写入 SystemVerilog package 文件"""
    content = generate_sv_package(block)
    output_path.write_text(content, encoding="utf-8")


def write_sv_apb_slave(block: Block, output_path: Path) -> None:
    """生成并写入 APB4 Slave 模块文件"""
    content = generate_sv_apb_slave(block)
    output_path.write_text(content, encoding="utf-8")
