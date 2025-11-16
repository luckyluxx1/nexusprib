import pymem
import json
import requests
from pathlib import Path

GITHUB_RAW = "https://raw.githubusercontent.com/luckyluxx1/nexusprib/main/"

class MemoryEngine:
    def __init__(self, process_name="RobloxPlayerBeta.exe"):
        self.pm = None
        self.module_base = 0
        self.offsets = self.load_offsets()
        self.process_name = process_name
    
    def load_offsets(self):
        offsets_path = Path("offsets.json")
        if offsets_path.exists():
            with open(offsets_path, 'r') as f:
                return json.load(f)
        
        # Auto-pull from GitHub
        try:
            resp = requests.get(f"{GITHUB_RAW}offsets.json", timeout=10)
            offsets = resp.json()
            with open(offsets_path, 'w') as f:
                json.dump(offsets, f, indent=2)
            print("✅ Offsets auto-updated from GitHub")
            return offsets
        except:
            print("⚠️ Using default offsets - manual update needed")
            return {
                "localplayer": 0x118, "playerlist": 0x2A0, "viewmatrix": 0x9A8B7C6,
                "health": 0x18C, "team": 0x1D8, "pos": 0x12C, "name": 0x108,
                "walkspeed": 0x3A0, "jumppower": 0x1A8, "velocity": 0x150
            }
    
    def attach(self):
        try:
            self.pm = pymem.Pymem(self.process_name)
            self.module_base = pymem.process.module_from_name(self.pm.process_handle, self.process_name).lpBaseOfDll
            return True
        except:
            return False
    
    def read_vec3(self, addr):
        return (self.pm.read_float(addr), self.pm.read_float(addr + 4), self.pm.read_float(addr + 8))
    
    def read_float(self, addr): return self.pm.read_float(addr)
    def read_int(self, addr): return self.pm.read_int(addr)
    def read_string(self, addr, length=32): return self.pm.read_string(addr, length).strip('\x00')
    
    def write_float(self, addr, val): self.pm.write_float(addr, val)
    
    def get_localplayer(self): return self.pm.read_longlong(self.module_base + self.offsets["localplayer"])
    
    def get_players(self):
        players = []
        local = self.get_localplayer()
        if not local: return players
        local_team = self.read_int(local + self.offsets["team"])
        local_pos = self.read_vec3(local + self.offsets["pos"])
        
        for i in range(64):
            try:
                paddr = self.pm.read_longlong(self.module_base + self.offsets["playerlist"] + i * 0x8)
                if not paddr or paddr == local: continue
                health = self.read_float(paddr + self.offsets["health"])
                if health <= 0 or health > 200: continue
                team = self.read_int(paddr + self.offsets["team"])
                pos = self.read_vec3(paddr + self.offsets["pos"])
                dist = math.dist(local_pos, pos)
                name = self.read_string(paddr + self.offsets["name"])
                players.append({"addr": paddr, "pos": pos, "health": health, "team": team, "name": name, "dist": dist})
            except: continue
        return players