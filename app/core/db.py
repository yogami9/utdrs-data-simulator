from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    db_name: str = settings.MONGODB_DB_NAME

db = Database()

async def connect_to_mongo():
    """Connect to MongoDB database."""
    try:
        logger.info(f"Connecting to MongoDB at {settings.MONGODB_URI[:20]}...")
        db.client = AsyncIOMotorClient(settings.MONGODB_URI)
        # Validate connection
        await db.client.admin.command('ping')
        logger.info("Connected to MongoDB")
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error connecting to MongoDB: {str(e)}")
        raise

async def close_mongo_connection():
    """Close MongoDB connection."""
    if db.client:
        db.client.close()
        logger.info("Closed MongoDB connection")

def get_database():
    """Get database instance."""
    if db.client is None:
        logger.error("Database client is None, connection may have failed")
        raise ConnectionError("Database connection not established")
    return db.client[db.db_name]
