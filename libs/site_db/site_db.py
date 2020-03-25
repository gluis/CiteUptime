"""
In-memroy DB of list following Singleton patttern
"""

from __future__ import annotations
from threading import Lock
from typing import Optional


class SiteDBMeta(type):
    """
    SiteDBMeta threadsafe implementation of SiteDB
    """

    _instance: Optional[SiteDB] = None
    _lock: Lock = Lock()
    """
    Lock obj used to sync threads during first access
    """

    def __call__(cls, *args, **kwargs):
        """
        First thread locks and the rest wait
        """
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class SiteDB(metaclass=SiteDBMeta):
    """
    SiteDB is a threadsafe, in-memory repository for all sites run.
    It holds all sites that have no errors.
    """

    def __init__(self) -> None:
        self.__sites = []

    def add_site(self, title):
        """
        Add site to db
        """
        self.__sites.append(title)

    def get_sites(self):
        """
        Return all sites from db
        """
        return self.__sites

    def remove_site(self, title):
        """
        Remove site from db
        """
        self.__sites.remove(title)
