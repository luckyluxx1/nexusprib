import math
import keyboard
import ctypes
import time
from memory import MemoryEngine  # Import from memory.py

class Features:
    def __init__(self, mem_engine):
        self.mem = mem_engine
        self.local = self.mem.get_localplayer()
    
    def speedwalk(self, enabled, speed):
        if enabled:
            local = self.mem.get_localplayer()
            if local:
                self.mem.write_float(local + self.mem.offsets["walkspeed"], speed)
    
    def fly(self, enabled):
        if enabled:
            local = self.mem.get_localplayer()
            if local:
                vel_y = self.mem.read_float(local + self.mem.offsets["velocity"] + 4)
                if keyboard.is_pressed('space'): vel_y = 50
                elif keyboard.is_pressed('shift'): vel_y = -50
                self.mem.write_float(local + self.mem.offsets["velocity"] + 4, vel_y)
    
    def aimbot(self, enabled, fov, smooth, bone="Head"):
        if not enabled: return
        players = self.mem.get_players()
        if not players: return
        
        matrix = [self.mem.read_float(self.mem.module_base + self.mem.offsets["viewmatrix"] + i*4) for i in range(16)]
        import pygame
        mouse_x, mouse_y = pygame.mouse.get_pos()
        closest_dist = fov
        closest = None
        
        for p in players:
            if p['team'] == self.mem.read_int(self.local + self.mem.offsets["team"]): continue
            head_pos = list(p['pos'])
            head_pos[1] += 1.8 if bone == "Head" else 0
            screen = world_to_screen(head_pos, matrix)  # Define below
            if not screen: continue
            dist_to_center = math.hypot(screen[0] - mouse_x, screen[1] - mouse_y)
            if dist_to_center < closest_dist:
                closest_dist = dist_to_center
                closest = screen
        
        if closest:
            target_x = mouse_x + (closest[0] - mouse_x) / smooth
            target_y = mouse_y + (closest[1] - mouse_y) / smooth
            ctypes.windll.user32.SetCursorPos(int(target_x), int(target_y))
    
    def triggerbot(self, enabled, delay):
        if not enabled: return
        # Simplified pixel check (implement full with PIL if needed)
        time.sleep(delay)
        # Fire if enemy in crosshair (placeholder - expand with screen capture)
    
    def autofarm(self, enabled):
        if enabled:
            # Da Hood: Tele to cash drops (CFrame write)
            pass  # Expand with known drop positions

def world_to_screen(pos, matrix):
    x, y, z = pos
    w = matrix[12] * x + matrix[13] * y + matrix[14] * z + matrix[15]
    if abs(w) < 0.001: return None
    sx = int(1920/2 + (matrix[0]*x + matrix[4]*y + matrix[8]*z + matrix[12]) / w * 1920/2)
    sy = int(1080/2 - (matrix[1]*x + matrix[5]*y + matrix[9]*z + matrix[13]) / w * 1080/2)
    return (sx, sy)