from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.immutable_runtime import ImmutableEvent, FinancialSnapshot
from app.events.bus import event_bus
from datetime import datetime, timezone
import json

class ImmutableFinancialRuntime:
    def __init__(self, db: Session):
        self.db = db

    def record_event(self, event_type: str, payload: dict):
        """Records an immutable event in the blockchain-like ledger"""
        # Get last event for chaining
        last_event = self.db.query(ImmutableEvent).order_by(ImmutableEvent.sequence.desc()).first()
        
        sequence = (last_event.sequence + 1) if last_event else 0
        prev_hash = last_event.current_hash if last_event else None
        
        new_event = ImmutableEvent(
            event_type=event_type,
            payload=payload,
            previous_hash=prev_hash,
            sequence=sequence,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        )
        new_event.current_hash = new_event.calculate_hash()
        
        self.db.add(new_event)
        self.db.commit()
        self.db.refresh(new_event)
        
        # Notify event bus
        event_bus.publish(f"immutable.{event_type}", {
            "id": new_event.id,
            "sequence": new_event.sequence,
            "hash": new_event.current_hash
        })
        
        return new_event

    def find_event(self, event_type: str, field: str, value: str):
        """Recupera um evento persistido pelo campo identificado do payload."""
        events = self.db.query(ImmutableEvent).filter(ImmutableEvent.event_type == event_type).all()
        return next((event for event in events if event.payload.get(field) == value), None)

    def replay(self, start_sequence: int = 0, end_sequence: int = None):
        """Replays events to reconstruct state"""
        query = self.db.query(ImmutableEvent).filter(ImmutableEvent.sequence >= start_sequence)
        if end_sequence is not None:
            query = query.filter(ImmutableEvent.sequence <= end_sequence)
        
        events = query.order_by(ImmutableEvent.sequence.asc()).all()
        
        # Verify integrity during replay
        expected_prev_hash = None if start_sequence == 0 else \
            self.db.query(ImmutableEvent).filter(ImmutableEvent.sequence == start_sequence - 1).first().current_hash
            
        for event in events:
            if event.previous_hash != expected_prev_hash:
                raise ValueError(f"Integrity breach at sequence {event.sequence}")
            
            # Recalculate hash to verify
            if event.current_hash != event.calculate_hash():
                raise ValueError(f"Hash mismatch at sequence {event.sequence}")
                
            expected_prev_hash = event.current_hash
            
        return events

    def create_snapshot(self):
        """Creates a snapshot of the current state based on replayed events"""
        last_event = self.db.query(ImmutableEvent).order_by(ImmutableEvent.sequence.desc()).first()
        if not last_event:
            return None
            
        # Example state: sum of all transaction amounts (simplified)
        # In a real scenario, this would be the balance of all wallets
        snapshot = FinancialSnapshot(
            last_event_sequence=last_event.sequence,
            state_data={"reconstruction": "active"}, # Placeholder for complex state
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(snapshot)
        self.db.commit()
        return snapshot
