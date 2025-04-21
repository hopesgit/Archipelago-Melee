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

_SUPPORTED_VERSIONS = ["0-02"]
# _SYMBOLS: Dict[str, Any] = {version: py_randomprime.symbols_for_version(version) for version in _SUPPORTED_VERSIONS}  # type: ignore
GAMES: Dict[str, Any] = {
    "0-02": {
        "game_id": b"GM8E01",
        "game_rev": 2,
        # "game_state_pointer": _SYMBOLS["0-02"]["g_GameState"],
        # "cstate_manager_global": _SYMBOLS["0-02"]["g_StateManager"],
        "cplayer_vtable": 0x803DA7A8,
    }
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

class MeleeAreas(Enum):
    """Game menus/areas with their corresponding IDs in memory"""

    Main_Menu = 00000000
    Vs_Mode = 00000000
    Singleplayer_Mode = 00000000
    End_of_Game = 332894565

def world_by_id(id: int) -> Optional[MeleeAreas]:
    for world in MeleeAreas:
        if world.value == id:
            return world
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
    current_game: Optional[str]
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

    def get_current_inventory(self) -> Dict[str, InventoryItemData]:
        MAX_VANILLA_ITEM_ID = 40
        inventory: Dict[str, InventoryItemData] = {}
        for item in item_table.values():
            i = self.get_item(item)
            if i is not None:
                if item.id <= MAX_VANILLA_ITEM_ID:
                    inventory[item.name] = i
        return inventory

    def get_alive(self) -> bool:
        player_state_pointer = self.__get_player_state_pointer()
        value = struct.unpack(
            ">I", self.dolphin_client.read_pointer(player_state_pointer, 0, 4)
        )[0]
        return bool(value & (1 << 31))

    def set_alive(self, alive: bool):
        player_state_pointer = self.__get_player_state_pointer()
        value = struct.unpack(
            ">I", self.dolphin_client.read_pointer(player_state_pointer, 0, 4)
        )[0]
        if alive:
            value |= 1 << 31
        else:
            value &= ~(1 << 31)
        self.dolphin_client.write_pointer(
            player_state_pointer, 0, struct.pack(">I", value)
        )

    def set_hardcore_mode(self, on: bool):
        value: 0
        if on:
            value = 0
        else: 
            value = 1
        self.dolphin_client.write_address(
            0x804D6D58, value 
        )
        # self.dolphin_client.

    def kill_player(self):
        ## current implementation idea:
        ## call function that triggers loss of a stock
        ## -> address 80033ce0
        ## write to register 3 the player number (should be 1?) (writing a 5 or higher crashes the game)
        ## -> maybe this should be written before trying to call the func at 80033ce0
        pass

    def get_current_level(self) -> Optional[MeleeAreas]:
        """Returns the world that the player is currently in"""
        if self.current_game is None:
            return None
        world_bytes = self.dolphin_client.read_pointer(
            0x8065CC14
            # GAMES[self.current_game]["game_state_pointer"], 0x84, struct.calcsize(">I")
        )
        if world_bytes is not None:
            logging.debug(f'Current menu is: {world_bytes}')
            world_asset_id = struct.unpack(">I", world_bytes)[0]
            return world_by_id(world_asset_id)
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
        """Initializes the connection to dolphin and verifies it is connected to Metroid Prime"""
        try:
            self.dolphin_client.connect()
            game_id = self.dolphin_client.read_address(GC_GAME_ID_ADDRESS, 6)
            try:
                game_rev: Optional[int] = self.dolphin_client.read_address(
                    GC_GAME_ID_ADDRESS, 2
                )[0]
                logging.debug(f"Game ID is: {game_rev}")
            except:
                game_rev = None
            # The first read of the address will be null if the client is faster than the emulator
            self.current_game = None
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
                    f"Connected to the wrong game ({game_id}, rev {game_rev}), please connect to Metroid Prime GC (Game ID starts with a GM8)"
                )
                self.game_id_error = game_id
                if game_rev:
                    self.game_rev_error = game_rev
            if self.current_game:
                self.logger.info("Metroid Prime Disc Version: " + self.current_game)
        except DolphinException:
            pass

    def disconnect_from_game(self):
        self.dolphin_client.disconnect()
        self.logger.info("Disconnected from Dolphin Emulator")

    def get_connection_state(self):
        try:
            connected = self.dolphin_client.is_connected()
            if not connected or self.current_game is None:
                return ConnectionState.DISCONNECTED.value
            elif self.is_in_playable_state():
                return ConnectionState.IN_GAME.value
            else:
                return ConnectionState.IN_MENU.value
        except DolphinException:
            return ConnectionState.DISCONNECTED.value

    def is_in_playable_state(self) -> bool:
        """Check if the player is in the actual game rather than the main menu"""
        return self.get_current_level() is not None and self.__is_player_table_ready()

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

    def __is_player_table_ready(self) -> bool:
        """Check if the player table is ready to be read from memory, indicating the game is in a playable state"""
        assert self.current_game
        player_table_bytes = self.dolphin_client.read_pointer(
            GAMES[self.current_game]["cstate_manager_global"] + 0x84C, 0, 4
        )
        if player_table_bytes is None:
            return False
        player_table = struct.unpack(">I", player_table_bytes)[0]
        if player_table == GAMES[self.current_game]["cplayer_vtable"]:
            return True
        else:
            return False

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