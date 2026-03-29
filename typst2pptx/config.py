from pydantic import BaseModel, Field


class ConvertConfig(BaseModel):
    """
    Conversion configuration.

    Attributes:
        dpi (int): Render resolution for PDF-to-PNG conversion.
        typst_bin (str): Path or name of the typst executable.
    """

    dpi: int = Field(default=150, ge=72, le=600)
    typst_bin: str = Field(default="typst")
