"""
Strict Asset Loader - NO FALLBACKS
"""

import os
import pygame
from settings import ASSET_PATHS


class AssetLoader:
    """Load assets ONLY from disk"""
    
    def __init__(self, base_path="."):
        """Initialize"""
        self.base_path = base_path
        self.image_cache = {}
        self.missing = []
        
        print("[ASSETS] Initializing Asset Loader...")
    
    def load_image(self, asset_key, scale=None):
        """Load image strictly"""
        if asset_key not in ASSET_PATHS:
            raise KeyError(f"[ERROR] Unknown asset: {asset_key}")
        
        if asset_key in self.image_cache:
            return self.image_cache[asset_key]
        
        rel_path = ASSET_PATHS[asset_key]
        full_path = os.path.normpath(os.path.join(self.base_path, rel_path))
        
        print(f"[LOAD] {asset_key}: {full_path}")
        
        if not os.path.exists(full_path):
            msg = f"\n{'='*70}\n[FATAL] ASSET NOT FOUND!\nKey: {asset_key}\nPath: {full_path}\n{'='*70}\n"
            print(msg)
            self.missing.append(asset_key)
            raise FileNotFoundError(msg)
        
        try:
            img = pygame.image.load(full_path).convert_alpha()
            if scale:
                img = pygame.transform.scale(img, scale)
            self.image_cache[asset_key] = img
            print(f"[✓] Loaded: {asset_key}")
            return img
        except pygame.error as e:
            msg = f"[ERROR] Could not load {full_path}: {e}"
            print(msg)
            raise RuntimeError(msg)
    
    def verify_all_assets(self):
        """Verify all assets exist"""
        print("\n[VERIFY] Checking all assets...")
        
        all_exist = True
        for key, path in ASSET_PATHS.items():
            full_path = os.path.normpath(os.path.join(self.base_path, path))
            exists = os.path.exists(full_path)
            status = "✓" if exists else "✗"
            print(f"  {status} {key}")
            if not exists:
                all_exist = False
        
        return all_exist