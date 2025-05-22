from motor.motor_asyncio import AsyncIOMotorClient
import certifi

# Use certifi for secure CA bundle
MONGO_URI = "your-mongo-uri"

client = AsyncIOMotorClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["your-db-name"]