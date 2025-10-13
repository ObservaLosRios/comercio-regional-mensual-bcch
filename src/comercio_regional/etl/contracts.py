"""Domain contracts defining the ETL component interfaces."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Protocol

from pandas import DataFrame


class SupportsPrepare(Protocol):
    """Protocol for collaborating objects that need a preparation step."""

    def prepare(self) -> None:
        """Perform pre-run preparation tasks."""


class Extractor(ABC):
    """Contract for data extractors."""

    @abstractmethod
    def extract(self) -> DataFrame:
        """Extract raw data and return it as a DataFrame."""


class Transformer(ABC):
    """Contract for data transformation components."""

    @abstractmethod
    def transform(self, data: DataFrame) -> DataFrame:
        """Transform the provided DataFrame and return the result."""


class Loader(ABC):
    """Contract for data loaders."""

    @abstractmethod
    def load(self, data: DataFrame) -> None:
        """Persist the provided DataFrame to the target destination."""


class PipelineStep(Protocol):
    """A protocol representing any callable pipeline step."""

    def __call__(self, data: DataFrame) -> DataFrame:
        """Execute the pipeline step and return the transformed data."""


class Pipeline(ABC):
    """Contract for ETL pipelines."""

    @abstractmethod
    def run(self) -> None:
        """Execute the pipeline end-to-end."""

    @abstractmethod
    def steps(self) -> Iterable[PipelineStep]:
        """Return the transformation steps in execution order."""
