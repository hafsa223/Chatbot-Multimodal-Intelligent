import uuid
from datetime import datetime

class SessionManager:
    def __init__(self):
        self.sessions = {}
        
    def create_session(self):
        """Create a new session and return the session ID"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "created_at": datetime.now(),
            "last_active": datetime.now(),
            "history": []
        }
        return session_id
        
    def get_session(self, session_id):
        """Get session data for a given session ID"""
        if session_id in self.sessions:
            self.sessions[session_id]["last_active"] = datetime.now()
            return self.sessions[session_id]
        return None
        
    def add_to_history(self, session_id, message):
        """Add a message to the session history"""
        if session_id in self.sessions:
            self.sessions[session_id]["history"].append({
                "timestamp": datetime.now(),
                "message": message
            })
            self.sessions[session_id]["last_active"] = datetime.now()
            
    def clear_history(self, session_id):
        """Clear the history for a given session"""
        if session_id in self.sessions:
            self.sessions[session_id]["history"] = []
            self.sessions[session_id]["last_active"] = datetime.now()
    
    def get_latest_file(self, session_id):
        """Retourne le dernier fichier PDF uploadé dans cette session"""
        if session_id in self.sessions:
            history = self.sessions[session_id]["history"]
            for item in reversed(history):  # On regarde depuis le plus récent
                if isinstance(item, dict) and "file" in item and item["file"].name.endswith(".pdf"):
                    return item["file"]
        return None