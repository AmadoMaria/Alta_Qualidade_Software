"""
JSON File Repository Adapter
This implements the Repository port using JSON files as storage.
Each "table" gets its own JSON file.
"""

import json
import os
from typing import List, Optional, Dict, Any
from pathlib import Path
from repository import Repository


class JsonRepository(Repository):
    """
    Concrete implementation of Repository using JSON files.
    Each table/entity type has its own JSON file.
    This is the ADAPTER in hexagonal architecture.
    """

    def __init__(self, table_name: str, data_dir: str = "data"):
        """
        Initialize the JSON file repository.

        Args:
            table_name: Name of the table (will be used as filename)
            data_dir: Directory where JSON files are stored
        """
        self.table_name = table_name
        self.data_dir = Path(data_dir)
        self.file_path = self.data_dir / f"{table_name}.json"
        self._ensure_setup()

    def _ensure_setup(self) -> None:
        """Create the data directory and JSON file if they don't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._write_data([])

    def _read_data(self) -> List[Dict[str, Any]]:
        """Read all data from the JSON file."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_data(self, data: List[Dict[str, Any]]) -> bool:
        """Write all data to the JSON file."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error writing to file {self.file_path}: {e}")
            return False

    def save(self, entity_id: str, data: Dict[str, Any]) -> bool:
        """Save a new entity to the JSON file."""
        entities = self._read_data()

        # Check if entity already exists
        if any(e.get("id") == entity_id for e in entities):
            return False

        # Add id to data and append
        entity = {"id": entity_id, **data}
        entities.append(entity)

        return self._write_data(entities)

    def find_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve an entity by its ID."""
        entities = self._read_data()

        for entity in entities:
            if entity.get("id") == entity_id:
                return entity

        return None

    def find_all(self) -> List[Dict[str, Any]]:
        """Retrieve all entities."""
        return self._read_data()

    def update(self, entity_id: str, data: Dict[str, Any]) -> bool:
        """Update an existing entity."""
        entities = self._read_data()

        for i, entity in enumerate(entities):
            if entity.get("id") == entity_id:
                # Preserve the id and update other fields
                entities[i] = {"id": entity_id, **data}
                return self._write_data(entities)

        return False

    def delete(self, entity_id: str) -> bool:
        """Delete an entity from the repository."""
        entities = self._read_data()
        initial_length = len(entities)

        entities = [e for e in entities if e.get("id") != entity_id]

        if len(entities) < initial_length:
            return self._write_data(entities)

        return False

    def exists(self, entity_id: str) -> bool:
        """Check if an entity exists."""
        entities = self._read_data()
        return any(e.get("id") == entity_id for e in entities)
