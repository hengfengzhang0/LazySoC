"""parser 模块测试"""

from pathlib import Path

import pytest

from lazysoc.parser import (
    Block,
    Field,
    Register,
    RegisterAlignmentError,
    parse_bits,
    parse_hex,
    parse_yaml,
)


class TestParseHex:
    """parse_hex 函数测试"""

    def test_parse_int(self) -> None:
        assert parse_hex(255) == 255

    def test_parse_hex_string(self) -> None:
        assert parse_hex("0x100") == 256

    def test_parse_hex_uppercase(self) -> None:
        assert parse_hex("0xFF") == 255

    def test_parse_decimal_string(self) -> None:
        assert parse_hex("100") == 100


class TestParseBits:
    """parse_bits 函数测试"""

    def test_single_bit_int(self) -> None:
        assert parse_bits(0) == (0, 0)

    def test_single_bit_string(self) -> None:
        assert parse_bits("5") == (5, 5)

    def test_bit_range(self) -> None:
        assert parse_bits("15:8") == (15, 8)

    def test_bit_range_with_spaces(self) -> None:
        assert parse_bits(" 7:0 ") == (7, 0)


class TestField:
    """Field dataclass 测试"""

    def test_field_width_single_bit(self) -> None:
        field = Field(name="test", msb=0, lsb=0)
        assert field.width == 1

    def test_field_width_multi_bit(self) -> None:
        field = Field(name="test", msb=7, lsb=0)
        assert field.width == 8

    def test_field_mask(self) -> None:
        field = Field(name="test", msb=3, lsb=1)
        assert field.mask == 0b1110  # bits 3:1


class TestParseYaml:
    """YAML 解析测试"""

    def test_parse_block_name(self, temp_yaml_file: Path) -> None:
        block = parse_yaml(temp_yaml_file)
        assert block.name == "TEST_BLOCK"

    def test_parse_base_address(self, temp_yaml_file: Path) -> None:
        block = parse_yaml(temp_yaml_file)
        assert block.base_address == 0x10000000

    def test_parse_registers_count(self, temp_yaml_file: Path) -> None:
        block = parse_yaml(temp_yaml_file)
        assert len(block.registers) == 2

    def test_parse_register_offset(self, temp_yaml_file: Path) -> None:
        block = parse_yaml(temp_yaml_file)
        assert block.registers[0].offset == 0x0
        assert block.registers[1].offset == 0x4

    def test_parse_register_access(self, temp_yaml_file: Path) -> None:
        block = parse_yaml(temp_yaml_file)
        assert block.registers[0].access == "RW"
        assert block.registers[1].access == "RO"

    def test_parse_fields(self, temp_yaml_file: Path) -> None:
        block = parse_yaml(temp_yaml_file)
        config_reg = block.registers[0]
        assert len(config_reg.fields) == 2
        assert config_reg.fields[0].name == "enable"
        assert config_reg.fields[1].name == "mode"

    def test_parse_field_bits(self, temp_yaml_file: Path) -> None:
        block = parse_yaml(temp_yaml_file)
        mode_field = block.registers[0].fields[1]
        assert mode_field.msb == 3
        assert mode_field.lsb == 1


class TestRegisterAlignment:
    """寄存器对齐检查测试"""

    def test_unaligned_offset_raises_exception(self, temp_unaligned_yaml: Path) -> None:
        with pytest.raises(RegisterAlignmentError) as exc_info:
            parse_yaml(temp_unaligned_yaml)
        assert "MISALIGNED_REG" in str(exc_info.value)
        assert "0x3" in str(exc_info.value)


class TestBlockProperties:
    """Block 属性测试"""

    def test_base_address_hex_format(self, temp_yaml_file: Path) -> None:
        block = parse_yaml(temp_yaml_file)
        assert block.base_address_hex == "0x10000000"


class TestRegisterProperties:
    """Register 属性测试"""

    def test_offset_hex_format(self, temp_yaml_file: Path) -> None:
        block = parse_yaml(temp_yaml_file)
        assert block.registers[0].offset_hex == "0x0"
        assert block.registers[1].offset_hex == "0x4"
