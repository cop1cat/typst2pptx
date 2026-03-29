from pydantic import BaseModel, Field


class ConvertConfig(BaseModel):
    """
    Конфигурация конвертации.

    Attributes:
        dpi (int): Разрешение рендера страниц PDF в PNG.
        typst_bin (str): Путь или имя исполняемого файла typst.
    """

    dpi: int = Field(default=150, ge=72, le=600)
    typst_bin: str = Field(default="typst")
