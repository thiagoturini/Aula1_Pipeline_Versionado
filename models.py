"""Modelos de dados para o pipeline de filmes."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Movie:
    """Representa um filme do TMDb com validações."""
    id: int
    title: str
    original_title: str
    release_date: str
    vote_average: float
    vote_count: int
    overview: str
    popularity: float
    adult: bool
    original_language: str
    budget: Optional[int] = None
    revenue: Optional[int] = None
    runtime: Optional[int] = None

    def __post_init__(self):
        """Validações após criação do objeto."""
        if self.id <= 0:
            raise ValueError(f"ID deve ser positivo: {self.id}")

        if not self.title or not self.title.strip():
            raise ValueError("Título não pode ser vazio")

        if not 0 <= self.vote_average <= 10:
            raise ValueError(f"Nota deve estar entre 0 e 10: {self.vote_average}")

        if self.vote_count < 0:
            raise ValueError(f"Contagem de votos não pode ser negativa: {self.vote_count}")

    @classmethod
    def from_json(cls, data: dict) -> 'Movie':
        """Cria um Movie a partir de um dicionário JSON."""
        return cls(
            id=data['id'],
            title=data['title'],
            original_title=data['original_title'],
            release_date=data['release_date'],
            vote_average=data['vote_average'],
            vote_count=data['vote_count'],
            overview=data.get('overview', ''),
            popularity=data['popularity'],
            adult=data['adult'],
            original_language=data['original_language'],
            budget=data.get('budget'),
            revenue=data.get('revenue'),
            runtime=data.get('runtime')
        )

    def get_year(self) -> Optional[int]:
        """Extrai o ano de lançamento."""
        if self.release_date:
            return int(self.release_date[:4])
        return None

    def is_profitable(self) -> bool:
        """Verifica se o filme foi lucrativo."""
        if self.budget and self.revenue:
            return self.revenue > self.budget
        return False

    def get_profit(self) -> Optional[int]:
        """Calcula o lucro do filme."""
        if self.budget and self.revenue:
            return self.revenue - self.budget
        return None

    def is_well_rated(self, threshold: float = 7.0) -> bool:
        """Verifica se o filme é bem avaliado."""
        return self.vote_average >= threshold
