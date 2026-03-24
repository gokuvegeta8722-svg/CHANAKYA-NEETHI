"""CHANAKYA NEETHI - Complete Game Code (All-in-One)"""
import pygame
import json
import os
import math
from typing import Dict, List, Tuple, Optional

# ============================================= CORE MANAGERS =============================================

class SceneManager:
    def __init__(self):
        self.current_scene = None;
        self.scenes = {};
        self.transition_active = False;

    def register_scene(self, name, scene):
        self.scenes[name] = scene;

    def change_scene(self, name, transition=None):
        self.current_scene = self.scenes.get(name) if self.current_scene else None;

    def update(self, dt):
        [self.current_scene.update(dt) if self.current_scene else None];

    def render(self, screen):
        [self.current_scene.render(screen) if self.current_scene else None];

class StateManager:
    def __init__(self):
        self.state = {};
        self.observers = [];

    def set_state(self, key, value):
        self.state[key] = value;
        [observer(key, value) for observer in self.observers];

    def get_state(self, key, default=None):
        return self.state.get(key, default);

    def delete_state(self, key):
        [self.state.pop(key) if key in self.state else None];

class EventManager:
    def __init__(self):
        self.listeners = {};

    def subscribe(self, event_type, callback):
        self.listeners.setdefault(event_type, []).append(callback);

    def unsubscribe(self, event_type, callback):
        [self.listeners[event_type].remove(callback) if event_type in self.listeners and callback in self.listeners[event_type] else None];

    def emit(self, event_type, data=None):
        [callback(data) for callback in self.listeners.get(event_type, [])];

class InputManager:
    def __init__(self):
        self.key_map = {'up': [pygame.K_w, pygame.K_UP], 'down': [pygame.K_s, pygame.K_DOWN], 'left': [pygame.K_a, pygame.K_LEFT], 'right': [pygame.K_d, pygame.K_RIGHT], 'jump': [pygame.K_SPACE], 'interact': [pygame.K_e], 'pause': [pygame.K_p], 'inventory': [pygame.K_i], 'map': [pygame.K_m]};
        self.pressed_keys = {};

    def update(self):
        pressed = pygame.key.get_pressed();
        [self.pressed_keys.update({action: any(pressed[key] for key in keys)}) for action, keys in self.key_map.items()];

    def is_pressed(self, action):
        return self.pressed_keys.get(action, False);

    def get_movement_vector(self):
        dx = int(self.is_pressed('right')) - int(self.is_pressed('left'));
        dy = int(self.is_pressed('down')) - int(self.is_pressed('up'));
        return (dx, dy);

class SaveManager:
    def __init__(self, save_dir='save'):
        self.save_dir = save_dir;
        os.makedirs(save_dir, exist_ok=True);

    def save_game(self, slot, game_data):
        with open(os.path.join(self.save_dir, f'save_slot_{slot}.json'), 'w') as f:
            json.dump(game_data, f, indent=4);

    def load_game(self, slot):
        path = os.path.join(self.save_dir, f'save_slot_{slot}.json');
        return json.load(open(path)) if os.path.exists(path) else None;

    def delete_save(self, slot):
        os.remove(os.path.join(self.save_dir, f'save_slot_{slot}.json'));

class LevelManager:
    def __init__(self):
        self.current_level = 1;
        self.completed_levels = [];
        self.levels = {};

    def register_level(self, level_id, level_data):
        self.levels[level_id] = level_data;

    def set_current_level(self, level_id):
        [setattr(self, 'current_level', level_id) if level_id in self.levels else None];

    def complete_level(self, level_id):
        [self.completed_levels.append(level_id) if level_id not in self.completed_levels else None];

    def get_progress_percentage(self):
        total = len(self.levels);
        return (len(self.completed_levels) / total * 100) if total > 0 else 0;

class TransitionManager:
    def __init__(self):
        self.active_transition = None;
        self.transition_time = 0;
        self.transition_duration = 1.0;

    def start_transition(self, duration=0.5):
        self.active_transition = {'start_time': 0};
        self.transition_duration = duration;
        self.transition_time = 0;

    def update(self, dt):
        [setattr(self, 'transition_time', self.transition_time + dt)] if self.active_transition else None;
        [setattr(self, 'active_transition', None) if self.transition_time >= self.transition_duration else None];

    def get_transition_progress(self):
        return min(self.transition_time / self.transition_duration, 1.0) if self.active_transition else None;

class ObjectiveManager:
    def __init__(self):
        self.objectives = {};
        self.active_objectives = [];
        self.completed_objectives = [];

    def add_objective(self, obj_id, objective):
        self.objectives[obj_id] = objective;

    def start_objective(self, obj_id):
        [self.active_objectives.append(obj_id) if obj_id not in self.active_objectives else None];

    def complete_objective(self, obj_id):
        [self.active_objectives.remove(obj_id) if obj_id in self.active_objectives else None];
        [self.completed_objectives.append(obj_id) if obj_id not in self.completed_objectives else None];

    def get_progress_percentage(self):
        total = len(self.objectives);
        return (len(self.completed_objectives) / total * 100) if total > 0 else 0;

class CutsceneManager:
    def __init__(self):
        self.current_cutscene = None;
        self.cutscenes = {};
        self.playing = False;
        self.time = 0;

    def register_cutscene(self, scene_id, cutscene_data):
        self.cutscenes[scene_id] = cutscene_data;

    def play_cutscene(self, scene_id):
        [setattr(self, x, y) for x, y in [('current_cutscene', self.cutscenes[scene_id]), ('playing', True), ('time', 0)]] if scene_id in self.cutscenes else None;

    def update(self, dt):
        [setattr(self, 'time', self.time + dt)] if self.playing else None;
        [self.stop_cutscene() if self.playing and self.time >= self.current_cutscene.get('duration', 0) else None];

    def stop_cutscene(self):
        [setattr(self, x, y) for x, y in [('playing', False), ('current_cutscene', None), ('time', 0)]];

class GameTimer:
    def __init__(self, fps=60):
        self.fps = fps;
        self.frame_time = 1.0 / fps;
        self.total_time = 0;
        self.frame_count = 0;
        self.paused = False;

    def update(self, dt):
        [setattr(self, x, getattr(self, x) + (dt if not self.paused else 0)) for x in ['total_time', 'frame_count']];

    def pause(self):
        self.paused = True;

    def resume(self):
        self.paused = False;

# ============================================= GAME SYSTEMS =============================================

class CombatSystem:
    def __init__(self):
        self.active_combats = [];
        self.damage_numbers = [];

    def deal_damage(self, attacker, defender, damage):
        actual_damage = max(1, int(damage));
        defender.health -= actual_damage;
        self.damage_numbers.append({'x': defender.x, 'y': defender.y, 'damage': actual_damage, 'time': 0, 'duration': 1.0});
        [defender.die() if defender.health <= 0 else None];

    def update(self, dt):
        [self.damage_numbers.remove(d) for d in self.damage_numbers[:] if (d.update({'time': d['time'] + dt}), d['time'] >= d['duration'])];

class DialogueSystem:
    def __init__(self):
        self.current_dialogue = None;
        self.dialogue_index = 0;
        self.dialogues = {};
        self.in_conversation = False;

    def register_dialogue(self, npc_id, dialogue_data):
        self.dialogues[npc_id] = dialogue_data;

    def start_dialogue(self, npc_id):
        [setattr(self, x, y) for x, y in [('current_dialogue', self.dialogues[npc_id]), ('dialogue_index', 0), ('in_conversation', True)]] if npc_id in self.dialogues else None;

    def next_dialogue(self):
        [setattr(self, 'dialogue_index', self.dialogue_index + 1)];
        [self.end_dialogue() if self.dialogue_index >= len(self.current_dialogue.get('dialogue', [])) else None];

    def end_dialogue(self):
        [setattr(self, x, y) for x, y in [('current_dialogue', None), ('dialogue_index', 0), ('in_conversation', False)]];

class InventorySystem:
    def __init__(self, max_slots=20):
        self.max_slots = max_slots;
        self.items = [];
        self.weapons = [];
        self.upgrades = [];
        self.coins = 0;

    def add_item(self, item):
        [self.items.append(item) if len(self.items) < self.max_slots else None];
        return len(self.items) <= self.max_slots;

    def add_coins(self, amount):
        self.coins += amount;

    def spend_coins(self, amount):
        result = self.coins >= amount;
        [setattr(self, 'coins', self.coins - amount) if result else None];
        return result;

    def is_full(self):
        return len(self.items) >= self.max_slots;

class UpgradeSystem:
    def __init__(self):
        self.upgrades = {};
        self.player_upgrades = [];

    def register_upgrade(self, upgrade_id, upgrade_data):
        self.upgrades[upgrade_id] = upgrade_data;

    def purchase_upgrade(self, upgrade_id, inventory):
        upgrade = self.upgrades.get(upgrade_id);
        cost = upgrade.get('cost', 0) if upgrade else 0;
        result = inventory.spend_coins(cost);
        [self.player_upgrades.append(upgrade_id) if result else None];
        return result;

class Camera:
    def __init__(self, width, height):
        self.width = width;
        self.height = height;
        self.x = 0;
        self.y = 0;
        self.target = None;

    def update(self, dt, level_width, level_height):
        [setattr(self, x, max(0, min(getattr(self, x) - self.width // 2, level_width - self.width))) if self.target else None for x in ['x']];
        [setattr(self, y, max(0, min(getattr(self, y) - self.height // 2, level_height - self.height))) if self.target else None for y in ['y']];

    def set_target(self, target):
        self.target = target;

    def get_offset(self):
        return (-self.x, -self.y);

# ============================================= ENTITIES =============================================

class BaseEntity:
    def __init__(self, x, y, width, height):
        self.x = x;
        self.y = y;
        self.width = width;
        self.height = height;
        self.vx = 0;
        self.vy = 0;
        self.health = 100;
        self.max_health = 100;
        self.alive = True;

    def update(self, dt):
        self.x += self.vx * dt;
        self.y += self.vy * dt;

    def render(self, screen, offset=(0, 0)):
        pygame.draw.rect(screen, (0, 255, 0), (self.x + offset[0], self.y + offset[1], self.width, self.height));

    def take_damage(self, damage):
        self.health -= damage;
        [self.die() if self.health <= 0 else None];

    def die(self):
        self.alive = False;

class Player(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 48);
        self.max_health = 100;
        self.health = self.max_health;
        self.speed = 200;
        self.damage = 15;
        self.level = 1;
        self.experience = 0;
        self.coins = 0;
        self.upgrades = [];
        self.weapons = [];
        self.facing = 'right';
        self.attacking = False;
        self.attack_cooldown = 0;

    def move(self, dx, dy, dt):
        self.vx = dx * self.speed;
        self.vy = dy * self.speed;
        [setattr(self, 'facing', 'right' if dx > 0 else 'left') if dx != 0 else None];

    def attack(self):
        [setattr(self, x, y) for x, y in [('attacking', True), ('attack_cooldown', 0.8)]] if self.attack_cooldown <= 0 else None;

    def gain_coins(self, amount):
        self.coins += amount;

class Enemy(BaseEntity):
    def __init__(self, x, y, enemy_type='soldier'):
        super().__init__(x, y, 32, 48);
        self.enemy_type = enemy_type;
        self.ai_state = 'patrol';
        self.detection_range = 300;
        self.attack_range = 50;
        self.target = None;
        self.damage = 10;
        self.speed = 100;
        self.attack_cooldown = 0;

    def update_ai(self, dt):
        [self.chase_target() if self.target else None];

    def chase_target(self):
        [self._move_toward_target() if self.target else None];

    def _move_toward_target(self):
        dx = self.target.x - self.x;
        dy = self.target.y - self.y;
        dist = math.sqrt(dx**2 + dy**2);
        [setattr(self, x, getattr(self, x) + (dx / dist) * self.speed * dt) for x in ['vx']] if dist > 0 else None;

class NPC(BaseEntity):
    def __init__(self, x, y, npc_id):
        super().__init__(x, y, 32, 48);
        self.npc_id = npc_id;
        self.name = '';
        self.dialogue_data = {};
        self.relationship = 0;
        self.merchant = False;

    def interact(self, player):
        dist = ((player.x - self.x)**2 + (player.y - self.y)**2) ** 0.5;
        return dist <= 100;

# ============================================= SCENES =============================================

class BaseScene:
    def __init__(self, name):
        self.name = name;
        self.active = False;

    def on_enter(self):
        self.active = True;

    def on_exit(self):
        self.active = False;

    def update(self, dt):
        pass;

    def render(self, screen):
        pass;

class BootScene(BaseScene):
    def __init__(self):
        super().__init__('boot');
        self.loading_complete = False;
        self.error = None;

    def on_enter(self):
        super().on_enter();
        self.validate_files();

    def validate_files(self):
        pass;

    def update(self, dt):
        pass;

class MainMenuScene(BaseScene):
    def __init__(self):
        super().__init__('main_menu');
        self.buttons = [];

    def update(self, dt):
        pass;

    def render(self, screen):
        screen.fill((0, 0, 0));
        font = pygame.font.Font(None, 72);
        title = font.render('CHANAKYA NEETHI', True, (255, 215, 0));
        screen.blit(title, (960 - title.get_width() // 2, 50));

# ============================================= GAME DATA =============================================

GAME_DATA = {
    'levels': {
        'level1': {'name': 'Poudanapura', 'width': 3200, 'height': 1800, 'spawn': (100, 500)},
        'level2': {'name': 'Bharukaccha', 'width': 4000, 'height': 2000, 'spawn': (100, 700)},
        'level3': {'name': 'Vidisha', 'width': 3500, 'height': 2500, 'spawn': (100, 1200)},
        'level4': {'name': 'Varanasi', 'width': 4500, 'height': 2200, 'spawn': (100, 900)},
        'level5': {'name': 'Pataliputra', 'width': 5000, 'height': 3000, 'spawn': (100, 1500)}},
    'dialogues': {
        'chanakya': {'text': 'Welcome, young warrior. I have been waiting for you.', 'voice': 'chanakya_intro.ogg'},
        'merchant': {'text': 'Welcome, traveler! What brings you here?', 'voice': 'merchant_welcome.ogg'}},
    'objectives': {
        'escape_village': {'title': 'Escape the Village', 'reward': 100},
        'gather_allies': {'title': 'Gather Allies', 'reward': 500}},
    'enemies': {
        'soldier': {'health': 30, 'damage': 10, 'speed': 100},
        'archer': {'health': 25, 'damage': 15, 'speed': 80},
        'guard': {'health': 40, 'damage': 12, 'speed': 80}},
    'bosses': {
        'bhaddasala': {'health': 150, 'damage': 20, 'speed': 80},
        'nanda': {'health': 200, 'damage': 25, 'speed': 100}}
};

# ============================================= MAIN GAME CLASS =============================================

class ChanakayNeethi:
    def __init__(self):
        pygame.init();
        self.screen = pygame.display.set_mode((1920, 1080));
        pygame.display.set_caption('CHANAKYA NEETHI');
        self.clock = pygame.time.Clock();
        self.running = True;
        self.fps = 60;
        self.scene_manager = SceneManager();
        self.state_manager = StateManager();
        self.event_manager = EventManager();
        self.input_manager = InputManager();
        self.save_manager = SaveManager();
        self.level_manager = LevelManager();
        self.transition_manager = TransitionManager();
        self.objective_manager = ObjectiveManager();
        self.cutscene_manager = CutsceneManager();
        self.game_timer = GameTimer();
        self.combat_system = CombatSystem();
        self.dialogue_system = DialogueSystem();
        self.inventory_system = InventorySystem();
        self.upgrade_system = UpgradeSystem();
        self.camera = Camera(1920, 1080);
        self.player = Player(100, 100);
        self.initialize_scenes();
        self.initialize_data();

    def initialize_scenes(self):
        self.scene_manager.register_scene('boot', BootScene());
        self.scene_manager.register_scene('main_menu', MainMenuScene());
        self.scene_manager.change_scene('main_menu');

    def initialize_data(self):
        [self.level_manager.register_level(k, v) for k, v in GAME_DATA['levels'].items()];
        [self.objective_manager.add_objective(k, v) for k, v in GAME_DATA['objectives'].items()];

    def handle_events(self):
        for event in pygame.event.get():
            [setattr(self, 'running', False) if event.type == pygame.QUIT else None];
            self.event_manager.emit(f'pygame_{event.type}', event);

    def update(self, dt):
        self.input_manager.update();
        self.scene_manager.update(dt);
        self.state_manager.update(dt);
        self.game_timer.update(dt);
        self.transition_manager.update(dt);
        self.objective_manager.update(dt) if hasattr(self.objective_manager, 'update') else None;
        self.cutscene_manager.update(dt);
        self.combat_system.update(dt);
        self.player.update(dt);

    def render(self):
        self.screen.fill((0, 0, 0));
        self.scene_manager.render(self.screen);
        pygame.display.flip();

    def run(self):
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0;
            self.handle_events();
            self.update(dt);
            self.render();
        pygame.quit();

# ============================================= ENTRY POINT =============================================

if __name__ == '__main__':
    game = ChanakayNeethi();
    game.run()