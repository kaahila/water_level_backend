from sqlalchemy import create_engine, BigInteger, Column, Float, TIMESTAMP, Integer
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base


# Erstelle ein Base-Objekt zur Deklaration der Tabellenspalten
Base = declarative_base()

# Deklariere die Tabelle mit drei Spalten
class LF7(Base):
            __tablename__ = 'lf7'
            id = Column(BigInteger, primary_key=True)
            created_on = Column(TIMESTAMP)
            value = Column(Float)

class Database:
    def __init__(self, url):
        # Erstelle eine Engine zur Verbindung mit der PostgreSQL-Datenbank
        self.engine = create_engine(url)

        # Erstelle eine Session zur Interaktion mit der Datenbank
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        # Erstelle die Tabelle in der Datenbank, falls sie noch nicht existiert
        Base.metadata.create_all(self.engine)

    def add_record(self, value, created_on):
        # Füge einen neuen Datensatz hinzu
        new_record = LF7(value=value, created_on=datetime.now())
        self.session.add(new_record)
        self.session.commit()
        
    def get_latest_record(self):
        # Lese den neuesten Datensatz aus der Tabelle aus
        latest_record = self.session.query(LF7).order_by(LF7.id.desc()).first()
        record = {'id' : latest_record.id,
                  'created_on' : latest_record.created_on,
                  'value' : latest_record.value}
        return record
    
    def get_all_records(self, limit = 20):
        # Lese alle Datensätze aus der Tabelle aus
        all_records = self.session.query(LF7).order_by(LF7.id.desc()).limit(limit).all()
        records = []
        for record in all_records:
            records.append({'id' : record.id,
                    'created_on' : record.created_on,
                    'value' : record.value})
        records.reverse()
        return records
    
    def close_connection(self):
        # Schließe die Datenbankverbindung
        self.session.close()