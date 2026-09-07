from pydantic import BaseModel, Field

from .enum_defs import DifferenceAttribute, DifferenceMethod


class DifferenceCalculation(BaseModel):
    attribute: DifferenceAttribute = Field(
        description="Property for which difference values are calculated"
    )
    methods: list[DifferenceMethod] = Field(
        description="Difference calculations to apply to the selected property"
    )
