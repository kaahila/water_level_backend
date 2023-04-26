from .database import Base, SessionLocal, engine
from .models import *
# Add the following function call somewhere initial: Base.metadata.create_all(bind=engine)

