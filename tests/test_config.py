import pytest
from pydantic import ValidationError

from typst2pptx.config import ConvertConfig


def test_defaults() -> None:
    config = ConvertConfig()
    assert config.dpi == 150
    assert config.typst_bin == "typst"


def test_dpi_boundary_min() -> None:
    config = ConvertConfig(dpi=72)
    assert config.dpi == 72


def test_dpi_boundary_max() -> None:
    config = ConvertConfig(dpi=600)
    assert config.dpi == 600


def test_dpi_below_min() -> None:
    with pytest.raises(ValidationError):
        ConvertConfig(dpi=71)


def test_dpi_above_max() -> None:
    with pytest.raises(ValidationError):
        ConvertConfig(dpi=601)


def test_custom_typst_bin() -> None:
    config = ConvertConfig(typst_bin="/usr/local/bin/typst")
    assert config.typst_bin == "/usr/local/bin/typst"
