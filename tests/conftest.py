"""测试 fixtures"""

from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def sample_yaml_content() -> str:
    """返回示例 YAML 内容"""
    return """
block:
  name: TEST_BLOCK
  base_address: 0x10000000
  description: Test Block

  registers:
    - name: CONFIG_REG
      offset: 0x0
      access: RW
      description: Configuration Register
      fields:
        - name: enable
          bits: 0
          description: Enable bit
        - name: mode
          bits: "3:1"
          description: Mode selection

    - name: STATUS_REG
      offset: 0x4
      access: RO
      description: Status Register
      fields:
        - name: ready
          bits: 0
        - name: error_code
          bits: "15:8"
"""


@pytest.fixture
def temp_yaml_file(tmp_path: Path, sample_yaml_content: str) -> Generator[Path, None, None]:
    """创建临时 YAML 文件"""
    yaml_file = tmp_path / "test_regs.yaml"
    yaml_file.write_text(sample_yaml_content, encoding="utf-8")
    yield yaml_file


@pytest.fixture
def unaligned_yaml_content() -> str:
    """返回地址未对齐的 YAML 内容"""
    return """
block:
  name: BAD_BLOCK
  base_address: 0x0

  registers:
    - name: MISALIGNED_REG
      offset: 0x3
      access: RW
"""


@pytest.fixture
def temp_unaligned_yaml(tmp_path: Path, unaligned_yaml_content: str) -> Path:
    """创建地址未对齐的临时 YAML 文件"""
    yaml_file = tmp_path / "unaligned.yaml"
    yaml_file.write_text(unaligned_yaml_content, encoding="utf-8")
    return yaml_file
