from app.app import main
from app.core.database.connection import run_db
import asyncio

if __name__ == "__main__":
    run_db()
    asyncio.run(main())