import os
import shutil
import hashlib

class MatchDirectory:
    def __init__(self, _dir):
        object.__setattr__(self, '_dir', _dir)
        os.makedirs(_dir, exist_ok=True)
    
    def __getattribute__(self, name):
        if name == 'match_history':
            _dir = object.__getattribute__(self, '_dir')
            match_history_path = os.path.join(_dir, 'match_history')
            os.makedirs(match_history_path, exist_ok=True)
            return MatchHistoryProxy(match_history_path)
        return object.__getattribute__(self, name)
    
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
    
    def add_match(self, rofl_file_path):
        """Add match from .rofl file"""
        if not os.path.exists(rofl_file_path):
            raise FileNotFoundError(f"ROFL file not found: {rofl_file_path}")
        
        filename = os.path.basename(rofl_file_path)
        match_id = os.path.splitext(filename)[0]
        
        match_dir = os.path.join(
            object.__getattribute__(self, '_dir'),
            'match_history',
            match_id
        )
        
        rofl_dest = os.path.join(match_dir, filename)
        
        if os.path.exists(match_dir):
            if os.path.exists(rofl_dest):
                if self._hash_file(rofl_file_path) == self._hash_file(rofl_dest):
                    return match_id, "Match already exists and is identical"
                else:
                    raise ValueError(f"Match {match_id} exists but .rofl file differs")
            else:
                raise ValueError(f"Match directory {match_id} exists but .rofl file missing")
        
        os.makedirs(match_dir, exist_ok=True)
        shutil.copy2(rofl_file_path, rofl_dest)
        
        return match_id, "Match added successfully"
    
    @staticmethod
    def _hash_file(filepath):
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

class MatchHistoryProxy:
    def __init__(self, history_path):
        self.path = history_path
    
    def __getattr__(self, match_id):
        match_dir = os.path.join(self.path, str(match_id))
        os.makedirs(match_dir, exist_ok=True)
        return match_dir
    
    def __setattr__(self, name, value):
        if name == 'path':
            object.__setattr__(self, name, value)