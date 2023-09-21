from app.app import main
from app.core.database.connection import run_db
from app.models import Message
import asyncio

if __name__ == "__main__":
    run_db()
    asyncio.run(main())