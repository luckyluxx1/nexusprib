import threading
import sys
from memory import MemoryEngine
from features import Features
from overlay import Overlay
from menu import NexusMenu
import keyboard

running = True

def main():
    mem = MemoryEngine()
    if not mem.attach():
        print("Run Roblox first!")
        sys.exit(1)
    
    features = Features(mem)
    overlay = Overlay(mem, features)
    
    def attach(): pass  # Update status
    def update(): mem.load_offsets()
    def panic(): global running; running = False
    
    menu = NexusMenu(attach, update, panic)
    
    threading.Thread(target=overlay.loop, daemon=True).start()
    
    def cheat_loop():
        while running:
            features.speedwalk(True, 50)  # From config
            features.aimbot(True, 90, 5)
            # All features...
            threading.Event().wait(0.01)
    
    threading.Thread(target=cheat_loop, daemon=True).start()
    
    keyboard.add_hotkey('insert', lambda: setattr(menu.root, 'attributes', ('-alpha', 0.0 if menu.root.attributes('-alpha') else 1.0)))
    keyboard.add_hotkey('end', lambda: setattr(sys, 'exit', sys.exit))
    
    menu.run()

if __name__ == "__main__":
    main()