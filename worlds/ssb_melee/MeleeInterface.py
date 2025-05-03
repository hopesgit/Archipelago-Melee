import logging
from logging import Logger
import struct
from typing import Any, Dict, Optional, Union
from enum import Enum

from .DolphinClient import GC_GAME_ID_ADDRESS, DolphinClient, DolphinException
from .Items import (
    ItemData,
    item_table
)

### ssbmStringBytes = bytearray()
### ssbmStringBytes.extend( "Super Smash Bros. Melee" )

	###	dataBytes = bytearray.fromhex( self.data )
	###	if dataBytes[0x3B78FB:0x3B7912] == ssbmStringBytes: self.region = 'NTSC'; self.version = '1.02' # most common, so checking for it first
	###	elif dataBytes[0x3B6C1B:0x3B6C32] == ssbmStringBytes: self.region = 'NTSC'; self.version = '1.01'
	###	elif dataBytes[0x3B5A3B:0x3B5A52] == ssbmStringBytes: self.region = 'NTSC'; self.version = '1.00'
	###	elif dataBytes[0x3B75E3:0x3B75FA] == ssbmStringBytes: self.region = 'PAL'; self.version = '1.00'

_SUPPORTED_VERSIONS = ["0-02"]
GAMES: Dict[str, Any] = {
    "0-00": {
        "game_id": b"GALE01",
        "game_rev": "0-00",
        "revision_range": [0x3B5A3B, 0x3B5A52]
    },
    "0-01": {
        "game_id": b"GALE01",
        "game_rev": "0-01",
        "revision_range": [0x3B6C1B, 0x3B6C32]
    },
    "0-02": {
        "game_id": b"GALE01",
        "game_rev": "0-02",
        "revision_range": [0x3B78FB, 0x3B7912]
    },
    "PAL": {
        "game_id": b"GALP01",
        "game_rev": "PAL",
        "revision_range": [0x3B75E3, 0x3B75FA]
    },
}

def calculate_item_offset(item_id: int) -> int:
    return (0x24 + RTSL_VECTOR_OFFSET) + (item_id * ITEM_SIZE)

AREA_SIZE = 16
ITEM_SIZE = 0x8
RTSL_VECTOR_OFFSET = 0x4
WORLD_STATE_SIZE = 0x18

class ConnectionState(Enum):
    DISCONNECTED = 0
    IN_GAME = 1
    IN_MENU = 2
    MULTIPLE_DOLPHIN_INSTANCES = 3

# TODO: rework areas
class MeleeAreas(Enum):
    """Game menus/areas with their corresponding IDs in memory"""
    # Melee's menu state is stored in a struct in 0x80479d30
    # state is as follows b'\x00\x00\x00\x00'
    # s1: current_major;
    # s2: pending_major;
    # s3: previous_major;
    # s4: current_minor;

    # all we care about is the current major and current minor, so check for those

    # 10240 don't know what this is yet
    Intro_Movie = [404226048, 404236288]
    Title_Screen = [256, 6144, 404226050]
    Demo_Battle = [404226049, 404226051]
    How_to_Play = 404226052 # this is only the title screen version, it uses the menu ids if called from the main menu
    Main_Menu = [
        16843520, 16847872, 16853760, 16846592, 16850944, 16851200,
        16851456, 16851712, 16852224, 16852480, 16849920, 16843264,
        16849664, 16845312, 16850688, 16846848, 16850176, 16853504,
        16854016, 16847616, 16847360
    ]
    # Classic
    Classic_CSS = 50528624
    Classic_Stage1_Intro = 50528512
    Classic_Stage1_Battle = 50528513
    Classic_Stage2_Intro = 50528520
    Classic_Stage2_Battle = 50528521
    Classic_Bonus_Targets_Intro = 50528528
    Classic_Bonus_Targets_Minigame = 50528529
    Classic_Stage4_Intro = 50528536
    Classic_Stage4_Battle = 50528537
    Classic_Stage5_Intro = 50528544
    Classic_Stage5_Battle = 50528545
    Classic_Bonus_Trophies_Intro = 50528552
    Classic_Bonus_Trophies_Minigame = 50528553
    Classic_Stage7_Intro = 50528560
    Classic_Stage7_Battle = 50528561
    Classic_Stage8_Intro = 50528568
    Classic_Stage8_Battle = 50528569
    Classic_Bonus_Maze_Intro = 50528576
    Classic_Bonus_Maze_Minigame = 50528577
    Classic_Stage10_Intro = 50528584
    Classic_Stage10_Battle = 50528585
    Classic_Final_Stage = 50528593
    Classic_Fighter_Trophy_Fall = 353698560
    Classic_Credits = 353698561
    Classic_Sizzle_Reel = 353698562
    Classic_Congratulations = 353698563

    # Adventure
    Adventure_CSS = 67371376
    Adventure_Stage1_Intro = 67371264
    Adventure_Stage1_Course = 67371265
    Adventure_Stage1_Luigi_Intro = 67371266
    Adventure_Stage1_Castle = 67371267
    Adventure_Stage2_Intro = 67371272
    Adventure_Stage2_Falls = 67371273
    Adventure_Stage2_Cabin = 67371274
    Adventure_Stage3_Maze_Intro = 67371280
    Adventure_Stage3_Maze = 67371281
    Adventure_Stage3_Temple = 67371282
    Adventure_Stage4_Brinstar = 67371289
    Adventure_Stage4_Explosion_Imminent = 67371290
    Adventure_Stage4_Escape = 67371291
    Adventure_Stage4_Explosion = 67371292
    Adventure_Stage5_Intro = 67371296
    Adventure_Stage5_Kirby = 67371297
    Adventure_Stage5_Hats_Intro = 67371298
    Adventure_Stage5_Hats = 67371299
    Adventure_Stage6_Intro = 67371304
    Adventure_Stage6_Fox = 67371305
    Adventure_Stage6_Arwings = 67371306
    Adventure_Stage6_Fox2 = 67371307
    Adventure_Stage7_Intro = 67371312
    Adventure_Stage7_Zaku = 67371313
    Adventure_Stage8_Crash = 67371320
    Adventure_Stage8_Intro = 67371321
    Adventure_Stage8_Race = 67371322
    Adventure_Stage8_Mute_City = 67371323
    Adventure_Stage9_Intro = 67371328
    Adventure_Stage9_Onett = 67371329
    Adventure_Stage10_Intro = 67371336
    Adventure_Stage10_Climb = 67371337
    Adventure_Stage11_Intro = 67371344
    Adventure_Stage11_Wireframes = 67371345
    Adventure_Stage11_Bros_Intro = 67371346
    Adventure_Stage11_Bros_Battle = 67371347
    Adventure_Stage12_Intro = 67371352
    Adventure_Stage12_Bowser = 67371353
    Adventure_Stage12_Trophy_Fall = 67371354
    Adventure_Stage12_Trophy_Rise = 67371355
    Adventure_Stage12_Giga = 67371356
    Adventure_Stage12_Trophy_Poof = 67371357
    Adventure_Fighter_Trophy_Fall = 370541568
    # 68551016 not sure which scene this could be
    Adventure_Credits = 370541569
    Adventure_Fighter_Sizzle_Reel = 370541570
    Adventure_Fighter_Congratulations = 370541571

    #All_Star_Mode
    All_Star_CSS = 84214128
    All_Star_Match = [84214016, 84214024, 84214032, 84214040, 84214048, 84214056, 84214064,
                      84214072, 84214080, 84214088, 84214096, 84214104, 84214112]
    All_Star_Lobby = [84214017, 84214025, 84214033, 84214041, 84214049, 84214057, 84214065,
                      84214073, 84214081, 84214089, 84214097, 84214105]
    All_Star_Fighter_Trophy_Fall = 85393768
    # 387384576 not sure which scene this could be
    All_Star_Credits = 387384577
    All_Star_Fighter_Sizzle_Reel = 387384578
    All_Star_Fighter_Congratulations = 387384579
    All_Star_Continue = 84214121

    Event_CSS = 724238592
    Event_Battle = 724238593
    Targets_CSS = 252641536
    Targets_Test = 252641537
    HomeRun_CSS = 538968320
    Multi_Man_10_CSS = 555811072
    Multi_Man_10_Battle = 555811073
    Multi_Man_100_CSS = 572653824
    Multi_Man_100_Battle = 572653825
    Multi_Man_3M_CSS = 589496576
    Multi_Man_3M_Battle = 589496577
    Multi_Man_15M_CSS = 606339328
    Multi_Man_15M_Battle = 606339329
    Multi_Man_Endless_CSS = 623182080
    Multi_Man_Endless_Battle = 623182081
    Multi_Man_Cruel_CSS = 640024832
    Multi_Man_Cruel_Battle = 640024833
    Training_Mode_CSS = 471597312
    Training_Mode_SSS = 471597313
    Training_Mode_Battle = 471597314
    # Vs Mode
    Vs_Melee_CSS = 33685760
    Vs_Melee_SSS = 33685761
    Vs_Melee_Battle = 33685762
    Vs_Melee_Results = 33685764
    Vs_Tournament_Prep = 454754560
    Vs_Tournament_Ladder = 454754561
    Vs_Tournament_SSS = 454754563
    Vs_Tournament_Battle = 454754564
    Vs_Tournament_Battle_Result = 454754566
    Vs_Special_Camera_MemCardWarning = 168427776
    Vs_Special_Camera_CSS = 168427777
    Vs_Special_Camera_SSS = [b'n', b'x02']
    Vs_Special_Camera_Battle = [b'n', b'x03']
    Vs_Special_Camera_Result = [b'n', b'x04']
    Vs_Special_Stamina_CSS = 522125568
    Vs_Special_Stamina_SSS = 522125569
    Vs_Special_Stamina_Battle = 522125570
    Vs_Special_Sudden_Death_CSS = 269484288
    Vs_Special_Sudden_Death_SSS = 269484289
    Vs_Special_Sudden_Death_Battle = 269484290
    Vs_Special_Sudden_Death_Result = 269484292
    Vs_Special_Giant_CSS = 505282816
    Vs_Special_Giant_SSS = 505282817
    Vs_Special_Giant_Battle = 505282818
    Vs_Special_Giant_Result = 505282820
    Vs_Special_Tiny_CSS = 488440064
    Vs_Special_Tiny_SSS = 488440065
    Vs_Special_Tiny_Battle = 488440066
    Vs_Special_Tiny_Result = 488440068
    Vs_Special_Invis_CSS = 286327040
    Vs_Special_Invis_SSS = 286327041
    Vs_Special_Invis_Battle = 286327042
    Vs_Special_Invis_Result = 286327044
    Vs_Special_FixedCam_CSS = 707395840
    Vs_Special_FixedCam_SSS = 707395841
    Vs_Special_FixedCam_Battle = 707395842
    Vs_Special_FixedCam_Result = 707395844
    Vs_Special_Button_CSS = 741081344
    Vs_Special_Button_SSS = 741081345
    Vs_Special_Button_Battle = 741081346
    Vs_Special_Button_Result = 741081348
    Vs_Special_Lightning_CSS = 320012544
    Vs_Special_Lightning_SSS = 320012545
    Vs_Special_Lightning_Battle = 320012546
    Vs_Special_Lightning_Result = 320012548
    Vs_Special_SloMo_CSS = 303169792
    Vs_Special_SloMo_SSS = 303169793
    Vs_Special_SloMo_Battle = 303169794
    Vs_Special_SloMo_Result = 303169796

    Challenger_Approaching = [336860416, 33685888]
    Fighter_Unlock_Duel_Young_Link = [336860417, 33685889]
    Fighter_or_Stage_Unlocked_Message = [33685952, 336860930]
    Trophy_Get = 336866050
    Thing_Unlocked = 336860674
    Continue = 67371369

    Trophies_Gallery = 185270528
    Trophies_Lottery = 202113280
    Trophies_Collection = 218956032


def screen_by_id(id: bytes) -> Optional[MeleeAreas]:
    print(f'screen_by_id id: {id}')
    if str(id)[:2] == "16":
        return MeleeAreas.Main_Menu
    for world in MeleeAreas:
        if world.value == id and type(world.value) == int:
            return world
        try:
            if id in world.value:
                return world
        except TypeError:
            continue
    return None

class Area:
    layerCount: int
    startNameIdx: int
    layerBitsLo: int
    layerBitsHi: int

    def __init__(
        self, startNameIdx: int, layerCount: int, layerBitsHi: int, layerBitsLo: int
    ) -> None:
        self.layerCount = layerCount
        self.startNameIdx = startNameIdx
        self.layerBitsHi = layerBitsHi
        self.layerBitsLo = layerBitsLo

    def __str__(self):
        return f"LayerCount: {self.layerCount}, LayerStartIndex: {self.startNameIdx}, LayerBitsHi: {self.layerBitsHi}, LayerBitsLo: {self.layerBitsLo}"

class InventoryItemData(ItemData):
    """Class used to track the player's current items and their quantities"""

    current_amount: int
    current_capacity: int

    def __init__(
        self, item_data: ItemData, current_amount: int, current_capacity: int
    ) -> None:
        super().__init__(
            item_data.name,
            item_data.id,
            item_data.classification,
            item_data.max_capacity,
        )
        self.current_amount = current_amount
        self.current_capacity = current_capacity


class MeleeInterface:
    """Interface sitting in front of the DolphinClient to provide higher level functions for interacting with Melee"""

    dolphin_client: DolphinClient
    connection_status: str
    logger: Logger
    _previous_message_size: int = 0
    game_id_error: Optional[str] = None
    game_rev_error: int
    current_game: Optional[str]= None
    relay_trackers: Optional[Dict[Any, Any]]

    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self.dolphin_client = DolphinClient(logger)

    def give_item_to_player(
        self,
        item_id: int,
        new_amount: int,
        new_capacity: int,
        ignore_capacity: bool = False,
    ):
        """Gives the player an item with the specified amount and capacity"""
        if ignore_capacity:
            self.dolphin_client.write_pointer(
                self.__get_player_state_pointer(),
                calculate_item_offset(item_id),
                struct.pack(">I", new_amount),
            )
        else:
            self.dolphin_client.write_pointer(
                self.__get_player_state_pointer(),
                calculate_item_offset(item_id),
                struct.pack(">II", new_amount, new_capacity),
            )

    def check_for_new_locations(self):
        pass

    def get_item(self, item_data: Union[ItemData, int]) -> Optional[InventoryItemData]:
        if isinstance(item_data, int):
            for item in item_table.values():
                if item.id == item_data:
                    return self.get_item(item)
        return None

    def get_player1_state(self):
        from .MemoryLocations import MEMORY
        stocks =  self.dolphin_client.read_address(0x801a583c + MEMORY["meleestruct"][0x801a583c]["p1_stocks"], 1)
        logging.info(f"p1 stocks: {stocks}")
        return stocks


    def get_current_inventory(self) -> Dict[str, InventoryItemData]:
        MAX_VANILLA_ITEM_ID = 40
        inventory: Dict[str, InventoryItemData] = {}
        for item in item_table.values():
            i = self.get_item(item)
            if i is not None:
                if item.id <= MAX_VANILLA_ITEM_ID:
                    inventory[item.name] = i
        return inventory


    def set_hardcore_mode(self, on: bool):
        value: 0
        if on:
            value = 0
        else: 
            value = 1
        self.dolphin_client.write_address(
            0x804D6D58, value 
        )


    # TODO: kill player
    def kill_player(self):
        ## current implementation idea:
        ## call function that triggers loss of a stock
        ## -> address 80033ce0
        ## write to register 3 the player number (should be 1?) (writing a 5 or higher crashes the game)
        ## -> maybe this should be written before trying to call the func at 80033ce0
        pass

    def get_current_menu(self) -> Optional[MeleeAreas]:
        """Returns the screen that the player is currently in"""
        if self.current_game is None:
            return None
        screen_bytes = self.dolphin_client.read_address(
            0x80479d30, 4
        )
        if screen_bytes is not None:
            screen_asset_id = struct.unpack(">I", screen_bytes)[0]
            return screen_by_id(screen_asset_id)
        return None


    def get_current_health(self) -> float:
        result = self.dolphin_client.read_pointer(
            self.__get_player_state_pointer(), 0xC, 4
        )
        return struct.unpack(">f", result)[0]

    def set_current_health(self, new_health_amount: float):
        self.dolphin_client.write_pointer(
            self.__get_player_state_pointer(), 0xC, struct.pack(">f", new_health_amount)
        )
        return self.get_current_health()

    def get_last_received_index(self) -> Optional[int]:
        """Gets the index of the last item received. This is stored as the current amount for the power suit"""
        return 2
        inventory_item = self.get_item(item_table[SuitUpgrade.Power_Suit.value])
        if inventory_item is not None:
            return inventory_item.current_amount
        return None

    def set_last_received_index(self, index: int):
        """Sets the received index to the index of the last item received. This is stored as the max amount for the power suit"""
        return 2
        inventory_item = self.get_item(item_table[SuitUpgrade.Power_Suit.value])
        if inventory_item is not None:
            inventory_item.current_amount = index
            self.give_item_to_player(
                inventory_item.id,
                inventory_item.current_amount,
                inventory_item.current_capacity,
            )

    def connect_to_game(self):
        """Initializes the connection to Dolphin and verifies it is connected to Melee"""
        try:
            self.dolphin_client.connect()
            game_id = self.dolphin_client.read_address(GC_GAME_ID_ADDRESS, 6)
            try:
                for version in GAMES:
                    brange = GAMES[version]["revision_range"]
                    offset = brange[1] - brange[0]
                    rev_bytes = self.dolphin_client.read_address(brange[0], offset)
                    rev_range = struct.unpack(">c", rev_bytes)
                    self.logger.info(f"revision check {version} : bytes = {rev_range}")
                    if "Super Smash Bros. Melee" in rev_range:
                        game_rev = GAMES[version]["game_rev"]
                # game_rev: Optional[int] = self.dolphin_client.read_address(
                #     GC_GAME_ID_ADDRESS, 2
                # )[0]
                logging.debug(f"Revision is: {game_rev}")
            except:
                game_rev = "0-02" # None
            # The first read of the address will be null if the client is faster than the emulator
            #self.current_game = None
            for version in _SUPPORTED_VERSIONS:
                if (
                    game_id == GAMES[version]["game_id"]
                    and game_rev == GAMES[version]["game_rev"]
                ):
                    self.current_game = version
                    break
            if (
                self.current_game is None
                and self.game_id_error != game_id
                and game_id != b"\x00\x00\x00\x00\x00\x00"
            ):
                self.logger.info(
                    f"Connected to the wrong game ({game_id}, rev {game_rev}), please connect to Super Smash Bros Melee GC (Game ID starts with a GAL)"
                )
                self.game_id_error = game_id
                if game_rev:
                    self.game_rev_error = game_rev
            if self.current_game:
                self.logger.info("Super Smash Bros Melee Revision: " + self.current_game)
        except DolphinException:
            pass

    def disconnect_from_game(self):
        self.dolphin_client.disconnect()
        self.logger.info("Disconnected from Dolphin Emulator")

    def get_connection_state(self):
        try:
            connected = self.dolphin_client.is_connected()
            #self.logger.info(f'get_connection_status connection is: {connected}')
            #self.logger.info(f'get_connection_status current_game is: {self.current_game}')
            if not connected or self.current_game is None:
                return ConnectionState.DISCONNECTED.value
            else:
                return ConnectionState.IN_MENU.value
        except DolphinException:
            return ConnectionState.DISCONNECTED.value


    # TODO: rework to use special messages in-game
    # def send_hud_message(self, message: str) -> bool:
    #     message = f"&just=center;{message}"
    #     if not self.current_game:
    #         return False

    #     if self.current_game == "jpn":
    #         message = f"&push;&font=C29C51F1;{message}&pop;"
    #     current_value = self.dolphin_client.read_address(
    #         GAMES[self.current_game]["HUD_TRIGGER_ADDRESS"], 1
    #     )
    #     if current_value == b"\x01":
    #         return False
    #     self._save_message_to_memory(message)
    #     self.dolphin_client.write_address(
    #         GAMES[self.current_game]["HUD_TRIGGER_ADDRESS"], b"\x01"
    #     )
    #     return True

    # def _save_message_to_memory(self, message: str):
    #     encoded_message = message.encode("utf-16_be")[:HUD_MAX_MESSAGE_SIZE]

    #     if len(encoded_message) == self._previous_message_size:
    #         encoded_message += b"\x00 "  # Add a space to the end of the message to force the game to update the message if it is the same size

    #     self._previous_message_size = len(encoded_message)

    #     encoded_message += (
    #         b"\x00\x00"  # Game expects a null terminator at the end of the message
    #     )

    #     if len(encoded_message) & 3:
    #         # Ensure the size is a multiple of 4
    #         num_to_align = (len(encoded_message) | 3) - len(encoded_message) + 1
    #         encoded_message += b"\x00" * num_to_align

    #     assert self.current_game
    #     self.dolphin_client.write_address(
    #         GAMES[self.current_game]["HUD_MESSAGE_ADDRESS"], encoded_message
    #     )

    def __get_player_state_pointer(self):
        assert self.current_game
        return int.from_bytes(
            self.dolphin_client.read_address(
                GAMES[self.current_game]["cstate_manager_global"] + 0x8B8, 4
            ),
            "big",
        )

    def __get_world_layer_state_pointer(self):
        assert self.current_game
        return int.from_bytes(
            self.dolphin_client.read_address(
                GAMES[self.current_game]["cstate_manager_global"] + 0x8C8, 4
            ),
            "big",
        )

    def __get_vector_item_offset(self):
        # Calculate the address of the Area at index area_idx
        vector_offset = 4
        vector_item_ptr = 0x0 + vector_offset
        return vector_item_ptr

    def __get_area_address(self, area_index: int):
        """Gets the address of an area from the world layer state areas vector"""
        vector_bytes = self.dolphin_client.read_pointer(
            self.__get_world_layer_state_pointer(), self.__get_vector_item_offset(), 12
        )  # 0x4 is count, 0x8 is max, 0xC is start address of the items in the vector
        # Unpack the bytes into the fields of the Area
        _count, _max, start_address = struct.unpack(">iiI", vector_bytes)
        return start_address + AREA_SIZE * area_index

    def __get_area(self, area_index: int) -> Area:
        """Loads an area at the given index for the level the player is currently in"""
        address = self.__get_area_address(area_index)
        item_bytes = self.dolphin_client.read_address(address, AREA_SIZE)
        return Area(*struct.unpack(">IIII", item_bytes))

    def set_layer_active(self, area_index: int, layer_id: int, active: bool):
        area = self.__get_area(area_index)
        if active:
            flag = 1 << layer_id
            area.layerBitsLo = area.layerBitsLo | flag
            area.layerBitsHi = area.layerBitsHi | (flag >> 0x1F)
        else:
            flag = ~(1 << layer_id)
            area.layerBitsLo = area.layerBitsLo & flag
            area.layerBitsHi = area.layerBitsHi & (flag >> 0x1F)

        new_bytes = struct.pack(
            ">IIII",
            area.startNameIdx,
            area.layerCount,
            area.layerBitsHi,
            area.layerBitsLo,
        )

        self.dolphin_client.write_address(
            self.__get_area_address(area_index), new_bytes
        )

    # probably not going to need this
    def reset_relay_tracker_cache(self):
        self.relay_trackers = None

    def update_relay_tracker_cache(self):
        if self.relay_trackers is None:
            self.relay_trackers = {}
            # getting vector<g_GameState.x88_worldStates>
            assert self.current_game
            world_state_array = struct.unpack(
                ">I",
                self.dolphin_client.read_pointer(
                    GAMES[self.current_game]["game_state_pointer"],
                    0x94,
                    struct.calcsize(">I"),
                ),
            )[0]
            world_states = [world_state_array + i * WORLD_STATE_SIZE for i in range(7)]
            for world_state in world_states:
                # getting WorldState.x0_mlvlId
                mlvl = struct.unpack(
                    ">I",
                    self.dolphin_client.read_address(
                        world_state, struct.calcsize(">I")
                    ),
                )[0]
                self.relay_trackers[f"{mlvl:X}"] = {
                    # getting WorldState.x8_mailbox.x0_relays
                    # which is an array of memory relays active in the selected world
                    "address": struct.unpack(
                        ">I",
                        self.dolphin_client.read_pointer(
                            world_state + 8, 0, struct.calcsize(">I")
                        ),
                    )[0],
                    "count": 0,
                    "memory_relays": [],
                }
        for _, relay_tracker in self.relay_trackers.items():
            # getting WorldState.x8_mailbox.x0_relays.size()
            relay_tracker["count"] = struct.unpack(
                ">I",
                self.dolphin_client.read_address(
                    relay_tracker["address"], struct.calcsize(">I")
                ),
            )[0]
            # getting WorldState.x8_mailbox.x0_relays content
            relay_tracker["memory_relays"] = struct.unpack(
                ">" + ("I" * relay_tracker["count"]),
                self.dolphin_client.read_address(
                    relay_tracker["address"] + 4,
                    relay_tracker["count"] * struct.calcsize(">I"),
                ),
            )
            # remove layer specific stuff from object id
            relay_tracker["memory_relays"] = [
                mr & 0x00FFFFFF for mr in relay_tracker["memory_relays"]
            ]

    def is_memory_relay_active(self, mlvl: str, idx: int) -> bool:
        if self.relay_trackers is None:
            return False

        relay_tracker = self.relay_trackers[mlvl]
        for i in range(relay_tracker["count"]):
            if relay_tracker["memory_relays"][i] == idx:
                return True

        return False