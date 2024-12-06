from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class SQLRequest:
    context: str
    prompt: str

@dataclass
class SQLResponse:
    generated_sql: str
    results: List[Dict[str, Any]]
    error: Optional[str] = None