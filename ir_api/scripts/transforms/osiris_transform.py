"""
Module provides the OSIRISTransform class, an implementation of the Transform abstract base class for MARI instrument
scripts.
"""
import logging
from typing import List

from sqlalchemy import ColumnElement
from sqlalchemy.dialects.postgresql import JSONB

from ir_api.core.model import Reduction
from ir_api.scripts.pre_script import PreScript
from ir_api.scripts.transforms.transform import Transform

logger = logging.getLogger(__name__)


class OsirisTransform(Transform):
    """
    OsirisTransform applies modifications to MARI instrument scripts based on reduction input parameters in a Reduction
    entity.
    """

    # pylint: disable = line-too-long
    def apply(self, script: PreScript, reduction: Reduction) -> None:
        logger.info("Beginning Osiris transform for reduction %s...", reduction.id)
        lines = script.value.splitlines()
        # MyPY does not believe ColumnElement[JSONB] is indexable, despite JSONB implementing the Indexable mixin
        # If you get here in the future, try removing the type ignore and see if it passes with newer mypy
        reduction_mode = reduction.reduction_inputs["mode"]
        for index, line in enumerate(lines):
            if self._replace_input(line, lines, index, "input_runs", reduction.reduction_inputs["runno"]):  # type: ignore
                continue
            if self._replace_input(line, lines, index, "cycle", reduction.reduction_inputs["cycle_string"]):
                continue
            if self._replace_input(line, lines, index, "reflection", reduction.reduction_inputs["analyser"]):
                continue
            if self._replace_input(
                line,
                lines,
                index,
                "spectroscopy_reduction",
                str(reduction_mode == "both" or reduction_mode == "spectroscopy"),
            ):
                continue
            if self._replace_input(
                line,
                lines,
                index,
                "diffraction_reduction",
                str(reduction_mode == "both" or reduction_mode == "diffraction"),
            ):
                continue
        script.value = "\n".join(lines)
        logger.info("Transform complete for reduction %s", reduction.id)

    # pylint: enable = line-too-long
    @staticmethod
    def _replace_input(
        line: str, lines: List[str], index: int, line_start: str, replacement: ColumnElement["JSONB"] | str
    ) -> bool:
        if line.startswith(line_start):
            lines[index] = f"{line_start} = {replacement}"
            return True
        return False
