"""YAML 寄存器定义解析器"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


class RegisterAlignmentError(Exception):
    """寄存器地址未对齐异常"""


@dataclass
class Field:
    """寄存器字段定义"""

    name: str
    msb: int
    lsb: int
    description: str = ""
    reset: int = 0

    @property
    def width(self) -> int:
        return self.msb - self.lsb + 1

    @property
    def mask(self) -> int:
        return ((1 << self.width) - 1) << self.lsb

    @property
    def reset_hex(self) -> str:
        return f"0x{self.reset:X}"


@dataclass
class Register:
    """寄存器定义"""

    name: str
    offset: int
    access: str
    description: str = ""
    fields: list[Field] = field(default_factory=list)

    @property
    def offset_hex(self) -> str:
        return f"0x{self.offset:X}"


@dataclass
class Block:
    """IP Block 定义"""

    name: str
    base_address: int
    description: str = ""
    registers: list[Register] = field(default_factory=list)

    @property
    def base_address_hex(self) -> str:
        return f"0x{self.base_address:08X}"


def parse_hex(value: int | str) -> int:
    """解析十六进制或十进制值"""
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        value = value.strip()
        if value.lower().startswith("0x"):
            return int(value, 16)
        return int(value)
    raise ValueError(f"无法解析值: {value}")


def parse_bits(bits_spec: int | str) -> tuple[int, int]:
    """
    解析 bit 范围定义

    Args:
        bits_spec: bit 定义，如 "15:8" 或 "0" 或 3

    Returns:
        (msb, lsb) 元组
    """
    if isinstance(bits_spec, int):
        return bits_spec, bits_spec

    bits_str = str(bits_spec).strip()
    if ":" in bits_str:
        parts = bits_str.split(":")
        msb = int(parts[0])
        lsb = int(parts[1])
        return msb, lsb
    bit = int(bits_str)
    return bit, bit


def parse_field(field_data: dict[str, Any]) -> Field:
    """解析单个字段定义"""
    msb, lsb = parse_bits(field_data["bits"])
    reset_val = field_data.get("reset", 0)
    if isinstance(reset_val, str):
        reset_val = parse_hex(reset_val)
    return Field(
        name=field_data["name"],
        msb=msb,
        lsb=lsb,
        description=field_data.get("description", ""),
        reset=reset_val,
    )


def parse_register(reg_data: dict[str, Any]) -> Register:
    """解析单个寄存器定义"""
    offset = parse_hex(reg_data["offset"])

    # 检查 4 字节对齐
    if offset % 4 != 0:
        raise RegisterAlignmentError(
            f"寄存器 '{reg_data['name']}' 的 offset {offset:#x} "
            f"没有 4 字节对齐，你是不是又手滑了？"
        )

    fields = [parse_field(f) for f in reg_data.get("fields", [])]

    return Register(
        name=reg_data["name"],
        offset=offset,
        access=reg_data.get("access", "RW"),
        description=reg_data.get("description", ""),
        fields=fields,
    )


def parse_block(block_data: dict[str, Any]) -> Block:
    """解析 Block 定义"""
    registers = [parse_register(r) for r in block_data.get("registers", [])]

    return Block(
        name=block_data["name"],
        base_address=parse_hex(block_data.get("base_address", 0)),
        description=block_data.get("description", ""),
        registers=registers,
    )


def parse_yaml(file_path: Path) -> Block:
    """
    解析 YAML 寄存器定义文件

    Args:
        file_path: YAML 文件路径

    Returns:
        解析后的 Block 对象

    Raises:
        FileNotFoundError: 文件不存在
        RegisterAlignmentError: 寄存器地址未对齐
    """
    with open(file_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return parse_block(data["block"])
