from typing import Optional, List, Dict, Tuple
from enum import Enum
from pydantic import BaseModel, Field

class Role(str, Enum):
    TOP = "TOP"
    JUNGLE = "JUNGLE"
    MIDDLE = "MIDDLE"
    BOTTOM = "BOTTOM"
    SUPPORT = "SUPPORT"

class Lane(str, Enum):
    TOP = "TOP"
    JUNGLE = "JUNGLE"
    MID = "MID"
    BOT = "BOT"

class ObjectiveType(str, Enum):
    DRAGON = "dragon"
    BARON = "baron"
    TOWER = "tower"
    INHIBITOR = "inhibitor"

class WardType(str, Enum):
    CONTROL = "control"
    TRINKET = "trinket"
    ITEM = "item"

class TeamFightOutcome(str, Enum):
    WON = "won"
    LOST = "lost"
    EVEN = "even"

class MomentType(str, Enum):
    SHUTDOWN_KILL = "shutdown_kill"
    OBJECTIVE_SWING = "objective_swing"
    INITIATION_WIN = "initiation_win"
    VISION_CONTROL = "vision_control"

class ImpactLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# Position data
class Position(BaseModel):
    x: float
    y: float

# Champion stats snapshot
class ChampionStats(BaseModel):
    health: float
    health_regen: float
    mana: float
    mana_regen: float
    armor: float
    spellblock: float
    attack_damage: float
    attack_speed: float
    attack_range: float
    move_speed: float

class Ability(BaseModel):
    id: str
    name: str
    description: str
    cooldown: List[float]
    cost: List[float]

class ChampionSnapshot(BaseModel):
    champion_id: int
    name: str
    version: str
    base_stats: ChampionStats
    abilities: List[Ability]

# Progression data
class ItemProgression(BaseModel):
    timestamp: int
    item_id: int
    item_name: str
    total_gold: int

class AbilityLevelUp(BaseModel):
    timestamp: int
    ability: str  # Q, W, E, R
    level: int

class SpellCast(BaseModel):
    timestamp: int
    ability: str
    target_type: str  # 'champion', 'minion', 'tower', etc.
    hit: bool
    damage: Optional[int] = None

# Statistics snapshots
class GoldSnapshot(BaseModel):
    timestamp: int
    team1_gold: int
    team2_gold: int
    differential: int

class XPSnapshot(BaseModel):
    timestamp: int
    team1_xp: int
    team2_xp: int

class CSSnapshot(BaseModel):
    timestamp: int
    participant_id: int
    cs: int
    cs_per_minute: float

class VisionSnapshot(BaseModel):
    timestamp: int
    participant_id: int
    score: int

class ObjectiveTimeline(BaseModel):
    timestamp: int
    team_id: int
    towers_destroyed: int
    inhibitors_destroyed: int

# Kill participants
class KillParticipant(BaseModel):
    participant_id: int
    summoner_name: str

class KillEvent(BaseModel):
    timestamp: int
    killer_id: int
    victim_id: int
    bounty: int
    assists: List[int]

# Positioning/movement metrics
class PositioningMetrics(BaseModel):
    average_distance_to_team: float
    distance_from_enemy_team: float
    positioning_score: float
    overextension_events: int

class KDAContext(BaseModel):
    timestamp: int
    kill_id: Optional[int] = None
    death_id: Optional[int] = None
    assist_kill_ids: List[int] = Field(default_factory=list)
    context: str  # e.g., "teamfight_win", "solo_kill", "executed"

class TeamFightRole(BaseModel):
    fight_id: int
    timestamp: int
    role: str  # 'initiator', 'followup', 'cleanup', 'peel'
    damage_dealt: int
    damage_taken: int
    cc_dealt: int

class WardingMetrics(BaseModel):
    wards_placed: int
    wards_destroyed: int
    wards_active_time: float
    vision_coverage_percentage: float
    deepward_efficiency: float

# Vision & movement analysis
class VisionHeatmap(BaseModel):
    team_id: int
    grid: Dict[str, int]  # spatial map of vision
    total_coverage: float

class WardCoverage(BaseModel):
    participant_id: int
    coverage_map: Dict[str, bool]
    gaps: List[Position]

class UnseenKillEvent(BaseModel):
    timestamp: int
    killer_id: int
    victim_id: int
    killer_distance_to_victim: float

class VisionDenialEvent(BaseModel):
    timestamp: int
    team_id: int
    area: Position
    duration: int

class PathedMovement(BaseModel):
    participant_id: int
    path: List[Tuple[int, Position]]  # (timestamp, position)
    average_speed: float
    total_distance: float

class RotationMetric(BaseModel):
    participant_id: int
    timestamp: int
    from_lane: Lane
    to_lane: Lane
    efficiency_score: float

class PositionPhaseData(BaseModel):
    phase: str  # 'early', 'mid', 'late'
    participant_id: int
    average_position: Position
    distance_from_base: float

class MovementAnalysis(BaseModel):
    player_pathing: List[PathedMovement]
    rotation_efficiency: List[RotationMetric]
    positioning_by_phase: List[PositionPhaseData]
    total_distance_traveled: float

# Vision analysis
class VisionAnalysis(BaseModel):
    team_vision_control: List[VisionHeatmap]
    player_ward_coverage: List[WardCoverage]
    unseen_kills: List[UnseenKillEvent]
    vision_denial_events: List[VisionDenialEvent]

# Objectives & replay data
class ObjectiveEvent(BaseModel):
    timestamp: int
    type: ObjectiveType
    team_id: int
    kills: List[KillParticipant]
    gold: int
    position: Optional[Position] = None

class WardPlacementData(BaseModel):
    participant_id: int
    timestamp: int
    position: Position
    type: WardType
    duration: int
    purpose: Optional[str] = None  # 'vision', 'safety', 'objective_tracking'

class ParticipantRole(BaseModel):
    participant_id: int
    role: str  # 'initiator', 'damage', 'peel', 'cleanup'

class TeamFightAnalysis(BaseModel):
    timestamp: int
    duration: int
    location: Position
    team_id: int
    participants: List[ParticipantRole]
    kills: List[KillEvent]
    outcome: TeamFightOutcome
    net_gold: int
    objective_secured: Optional[str] = None

class MatchStats(BaseModel):
    total_kills: int
    total_gold: int
    average_level_by_minute: Dict[int, float]
    gold_differential: List[GoldSnapshot]
    xp_differential: List[XPSnapshot]
    cs_timeline: List[CSSnapshot]
    vision_score: List[VisionSnapshot]
    objective_control: List[ObjectiveTimeline]

# Key insights
class KeyMoment(BaseModel):
    timestamp: int
    type: MomentType
    description: str
    impact: ImpactLevel
    participant_id: Optional[int] = None

class WinCondition(BaseModel):
    primary: str
    secondary: List[str]
    team_id: int
    execution_score: int  # 0-100

# Objective data
class DragonKill(BaseModel):
    timestamp: int
    team_id: int
    type: str
    participant: Optional[KillParticipant] = None

class BaronKill(BaseModel):
    timestamp: int
    team_id: int
    participant: Optional[KillParticipant] = None

class RiftHeraldKill(BaseModel):
    timestamp: int
    team_id: int
    participant: Optional[KillParticipant] = None

class Objectives(BaseModel):
    towers: int
    inhibitors: int
    dragons: List[DragonKill]
    barons: List[BaronKill]
    rift_heralds: List[RiftHeraldKill]

class Team(BaseModel):
    team_id: int
    win: bool
    kills: int
    gold: int
    objectives: Objectives

# Main participant object
class Participant(BaseModel):
    participant_id: int
    puuid: str
    summoner_name: str
    team_id: int
    
    # Champion and role
    champion_id: int
    champion_data: ChampionSnapshot
    role: Role
    lane: Lane
    
    # Game performance
    kills: int
    deaths: int
    assists: int
    cs: int
    gold: int
    level: int
    
    # Item progression
    item_build: List[ItemProgression]
    final_items: List[int]
    
    # Ability data
    ability_level_ups: List[AbilityLevelUp]
    spell_casts: List[SpellCast]
    
    # Metrics
    positioning: PositioningMetrics
    kda: List[KDAContext]
    team_fight_participation: List[TeamFightRole]
    warding_score: WardingMetrics
    skillshot_accuracy: Optional[float] = None

# Main Match object
class Match(BaseModel):
    # Riot API metadata
    match_id: str
    game_creation: int
    game_duration: int
    game_version: str
    
    # Persistence tracking
    stored_at: int
    expires_at: int
    
    # Teams and participants
    teams: List[Team]
    participants: List[Participant]
    
    # Processed statistics
    stats: MatchStats
    timeline: List[Dict]  # Generic timeline events
    
    # CV-processed data
    vision_data: VisionAnalysis
    player_movement: MovementAnalysis
    
    # Replay-derived data
    objective_timings: List[ObjectiveEvent]
    ward_placement: List[WardPlacementData]
    team_fighting: List[TeamFightAnalysis]
    
    # Insights
    key_moments: List[KeyMoment]
    win_conditions: List[WinCondition]

# Database storage model
class StoredMatch(Match):
    id: str = Field(alias="_id")
    
    search_indexes: Dict = Field(default_factory=lambda: {
        "summoner_puuids": [],
        "champion_ids": [],
        "tags": []
    })
    
    last_retrieved: int
    access_count: int