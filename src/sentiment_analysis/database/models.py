"""
Modelos ORM do banco de dados.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AnalysisResult(Base):
    """
    Tabela para armazenar resultados de análises.

    Armazena cada análise realizada para histórico e estatísticas.
    """

    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    sentiment = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)
    scores = Column(JSON, default=dict)
    model_name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<AnalysisResult(id={self.id}, sentiment={self.sentiment}, confidence={self.confidence:.2f})>"