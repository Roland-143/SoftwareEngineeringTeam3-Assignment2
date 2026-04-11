"""MySQL database connection pool module."""

import mysql.connector
from mysql.connector import pooling

from app.config import Config

_pool = None


def _get_pool():
    """Lazily create and return a connection pool."""
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name="backend_pool",
            pool_size=5,
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
        )
    return _pool


def get_connection():
    """Return a connection from the pool.

    Usage::

        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT 1")
            rows = cursor.fetchall()
        finally:
            conn.close()   # returns to pool
    """
    return _get_pool().get_connection()
