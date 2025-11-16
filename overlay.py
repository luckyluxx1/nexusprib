import pygame
import win32gui
import win32con
from memory import MemoryEngine
from features import Features

def world_to_screen(pos, matrix):  # Duplicate for independence
    # Same as above
    pass

class Overlay:
    def __init__(self, mem_engine, features):
        self.mem = mem_engine
        self.features = features
        self.screen_size = (1920, 1080)
        self.surface = None
        self.running = True
    
    def create(self):
        hwnd = win32gui.FindWindow(None, "Roblox")
        if hwnd:
            rect = win32gui.GetWindowRect(hwnd)
            self.screen_size = (rect[2] - rect[0], rect[3] - rect[1])
        
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size, pygame.NOFRAME)
        pygame.display.set_caption("NexusOverlay")
        hwnd = pygame.display.get_wm_info()['window']
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST)
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)
    
    def render(self):
        self.surface.fill((0, 0, 0, 0))
        players = self.mem.get_players()
        if not players: return
        
        matrix = [self.mem.read_float(self.mem.module_base + self.mem.offsets["viewmatrix"] + i*4) for i in range(16)]
        center_x, center_y = self.screen_size[0]//2, self.screen_size[1]//2
        font = pygame.font.SysFont('arial', 16)
        local_team = self.mem.read_int(self.mem.get_localplayer() + self.mem.offsets["team"])
        
        # FOV Circle & Crosshair (from config)
        pygame.draw.circle(self.surface, (255,255,255,100), (center_x, center_y), 50, 2)  # FOV
        pygame.draw.line(self.surface, (255,255,255), (center_x-10, center_y), (center_x+10, center_y), 2)
        pygame.draw.line(self.surface, (255,255,255), (center_x, center_y-10), (center_x, center_y+10), 2)
        
        for p in players:
            if p['team'] == local_team: continue
            feet = world_to_screen(p['pos'], matrix)
            head = world_to_screen((p['pos'][0], p['pos'][1]+1.8, p['pos'][2]), matrix)
            if not feet or not head: continue
            
            h = feet[1] - head[1]
            w = h / 2
            box_rect = (feet[0]-w/2, head[1], w, h)
            
            pygame.draw.rect(self.surface, (255,0,0,200), box_rect, 2)
            text = font.render(f"{p['name']} [{int(p['health'])}HP {int(p['dist'])}m]", True, (255,255,255))
            self.surface.blit(text, (feet[0]-50, head[1]-20))
        
        self.screen.blit(self.surface, (0,0))
        pygame.display.flip()
    
    def loop(self):
        clock = pygame.time.Clock()
        self.create()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
            self.render()
            clock.tick(60)
        pygame.quit()