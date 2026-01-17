"""LazySOC CLI 入口"""

from pathlib import Path

import click

from lazysoc.generators.c_gen import write_c_header
from lazysoc.generators.doc_gen import write_markdown
from lazysoc.generators.sv_gen import write_sv_apb_slave, write_sv_package
from lazysoc.parser import RegisterAlignmentError, parse_yaml


@click.group()
@click.version_option()
def cli() -> None:
    """LazySOC - SoC 寄存器生成工具"""


@cli.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(path_type=Path),
    default=Path("."),
    help="输出目录",
)
@click.option("--sv/--no-sv", default=True, help="生成 SystemVerilog package")
@click.option("--apb/--no-apb", default=True, help="生成 APB4 Slave 模块")
@click.option("--c/--no-c", default=True, help="生成 C Header")
@click.option("-d", "--doc/--no-doc", default=False, help="生成 Markdown 文档")
def generate(
    input_file: Path, output_dir: Path, sv: bool, apb: bool, c: bool, doc: bool
) -> None:
    """从 YAML 生成寄存器代码"""
    try:
        block = parse_yaml(input_file)
    except RegisterAlignmentError as e:
        raise click.ClickException(str(e)) from e

    output_dir.mkdir(parents=True, exist_ok=True)

    if sv:
        sv_path = output_dir / f"{block.name.lower()}_pkg.sv"
        write_sv_package(block, sv_path)
        click.echo(f"生成 SystemVerilog Package: {sv_path}")

    if apb:
        apb_path = output_dir / f"{block.name.lower()}_apb_slave.sv"
        write_sv_apb_slave(block, apb_path)
        click.echo(f"生成 APB4 Slave 模块: {apb_path}")

    if c:
        c_path = output_dir / f"{block.name.lower()}_regs.h"
        write_c_header(block, c_path)
        click.echo(f"生成 C Header: {c_path}")

    if doc:
        doc_path = output_dir / f"{block.name.lower()}_regs.md"
        write_markdown(block, doc_path)
        click.echo(f"生成 Markdown 文档: {doc_path}")


@cli.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
def validate(input_file: Path) -> None:
    """验证 YAML 定义文件"""
    try:
        block = parse_yaml(input_file)
        click.echo(f"✓ Block: {block.name}")
        click.echo(f"  Base Address: {block.base_address_hex}")
        click.echo(f"  Registers: {len(block.registers)}")
        for reg in block.registers:
            click.echo(f"    - {reg.name} @ {reg.offset_hex} ({reg.access})")
    except RegisterAlignmentError as e:
        raise click.ClickException(str(e)) from e


if __name__ == "__main__":
    cli()
