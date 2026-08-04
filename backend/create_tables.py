from app.db.base import Base
from app.db.session import engine
from app.models.company import Company

Base.metadata.create_all(bind=engine)

print("Tables created successfully")