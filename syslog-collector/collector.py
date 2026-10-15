import asyncio
import sqlite3
import json
from datetime import datetime


DB_PATH = "syslog.db"


def init_db():
    conn