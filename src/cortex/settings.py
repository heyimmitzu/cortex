"""Loads config/config.yaml into a typed settings object.

Usage:
    from cortex.settings import get_settings
    settings = get_settings()
    settings.llm.structuring_model
"""

from pathlib import Path

import yaml
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"


class PathsConfig(BaseModel):
    model_dir: str
    data_dir: str
    raw_captures_dir: str
    lancedb_dir: str


class LLMConfig(BaseModel):
    structuring_model: str
    answer_model: str
    n_ctx: int
    n_threads: int


class EmbeddingConfig(BaseModel):
    model_name: str


class RerankerConfig(BaseModel):
    model_name: str


class RetrievalConfig(BaseModel):
    top_k_retrieve: int
    top_k_rerank: int


class LanceDBConfig(BaseModel):
    table_name: str


class Settings(BaseModel):
    paths: PathsConfig
    llm: LLMConfig
    embedding: EmbeddingConfig
    reranker: RerankerConfig
    retrieval: RetrievalConfig
    lancedb: LanceDBConfig

    @property
    def model_path(self) -> Path:
        return PROJECT_ROOT / self.paths.model_dir / self.llm.structuring_model


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        with open(CONFIG_PATH) as f:
            raw = yaml.safe_load(f)
        _settings = Settings(**raw)
    return _settings
