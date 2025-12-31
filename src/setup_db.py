import logging
from utils.logging_configuration import configure_logging
from sqlalchemy import create_engine
from inventory_system.models import Base
from constants import DB

configure_logging()
logger = logging.getLogger(__name__)

engine = create_engine(DB.URL)

Base.metadata.create_all(engine)

logger.info("Database schema successfully created.")