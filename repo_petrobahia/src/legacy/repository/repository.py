"""
Repository Port (Interface)
This defines the contract for data persistence operations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


class Repository(ABC):
    """
    Abstract base class defining the repository interface.
    This is the PORT in hexagonal architecture.
    """

    @abstractmethod
    def save(self, entity_id: str, data: Dict[str, Any]) -> bool:
        """
        Save an entity to the repository.

        Args:
            entity_id: Unique identifier for the entity
            data: Dictionary containing entity data

        Returns:
            bool: True if save was successful, False otherwise
        """
        pass

    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an entity by its ID.

        Args:
            entity_id: Unique identifier for the entity

        Returns:
            Optional[Dict]: Entity data if found, None otherwise
        """
        pass

    @abstractmethod
    def find_all(self) -> List[Dict[str, Any]]:
        """
        Retrieve all entities from the repository.

        Returns:
            List[Dict]: List of all entities
        """
        pass

    @abstractmethod
    def update(self, entity_id: str, data: Dict[str, Any]) -> bool:
        """
        Update an existing entity.

        Args:
            entity_id: Unique identifier for the entity
            data: Dictionary containing updated entity data

        Returns:
            bool: True if update was successful, False otherwise
        """
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """
        Delete an entity from the repository.

        Args:
            entity_id: Unique identifier for the entity

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        pass

    @abstractmethod
    def exists(self, entity_id: str) -> bool:
        """
        Check if an entity exists in the repository.

        Args:
            entity_id: Unique identifier for the entity

        Returns:
            bool: True if entity exists, False otherwise
        """
        pass
