import asyncio
import json
import multiprocessing
import os
import subprocess
import traceback
from typing import List, Optional
import zipfile
from enum import Enum

import settings
from CommonClient import (
    ClientCommandProcessor, 
    CommonContext, 
    get_base_parser, 
    logger, 
    server_loop, 
    gui_enabled
)
from NetUtils import ClientStatus
import Utils
from .MeleeUtils import get_apworld_version
from .ClientReceiveItems import handle_receive_items
# from .Container import construct_hook_patch
from .DolphinClient import DolphinException, assert_no_running_dolphin, get_num_dolphin_instances
from .Locations import METROID_PRIME_LOCATION_BASE, locations
from .MeleeInterface import ConnectionState, InventoryItemData, MeleeAreas, MeleeInterface

status_messages = {
    0: "Connected to Melee",
    1: "Connected to game, waiting for game to start",
    2: "Unable to connect to the Dolphin instance, attempting to reconnect...",
    3: "Warning: Multiple Dolphin instances detected, client may not function correctly."
}

class MeleeCommandProcessor(ClientCommandProcessor):
    ctx: "MeleeContext"

    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    # TODO: rework this to use SSBM in-game notices
    def _cmd_test_hud(self, *args):
        """Send a message to the game interface."""
        self.ctx.notification_manager.queue_notification(' '.join(map(str, args)))

    def _cmd_status(self, *args):
        """Display the current Dolphin connection status."""
        logger.info(f"Connection status: {status_messages[self.ctx.connection_state]}")

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        if isinstance(self.ctx, MeleeContext):
            self.ctx.death_link_enabled = not self.ctx.death_link_enabled
            Utils.async_start(self.ctx.update_death_link(
                self.ctx.death_link_enabled), name="Update Deathlink")
            message = f"Deathlink {'enabled' if self.ctx.death_link_enabled else 'disabled'}"
            logger.info(message)
            self.ctx.notification_manager.queue_notification(message)

    def _cmd_hardcore_mode(self):
        """Toggles the in-game HUD. You can't be nervous about damage that you can't see, right?"""
        logger.info('Toggling HUD...')
        self.ctx.game_interface.set_hardcore_mode(not self.ctx.hardcore_mode)
        self.ctx.hardcore_mode = not self.ctx.hardcore_mode
        logger.info(f"HUD has been set to {'ON' if self.ctx.hardcore_mode else 'OFF'}.")


class MeleeContext(CommonContext):
    current_menu_id = 0
    previous_level_id = 0
    is_pending_death_link_reset = False
    command_processor = MeleeCommandProcessor
    game_interface: MeleeInterface
    #notification_manager: NotificationManager
    game = "Super Smash Bros Melee"
    items_handling = 0b111
    dolphin_sync_task = None
    connection_state = ConnectionState.DISCONNECTED.value
    slot_data: dict[str, Utils.Any] = None
    death_link_enabled = False
    previous_location_str: str = ""
    slot_name: Optional[str] = None
    last_error_message: Optional[str] = None
    apssbm_file: Optional[str] = None
    hardcore_mode = False

    def __init__(self, server_address, password, apssbm_file=None):
        super().__init__(server_address, password)
        self.game_interface = MeleeInterface(logger)
        # self.notification_manager = NotificationManager(HUD_MESSAGE_DURATION, self.game_interface.send_hud_message)
        self.apssbm_file = apssbm_file

    def on_deathlink(self, data: Utils.Dict[str, Utils.Any]) -> None:
        super().on_deathlink(data)
        self.game_interface.set_alive(False)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(MeleeContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            if "death_link" in args["slot_data"]:
                self.death_link_enabled = bool(args["slot_data"]["death_link"])
                Utils.async_start(self.update_death_link(
                    bool(args["slot_data"]["death_link"])))

    def run_gui(self):
        from kvui import GameManager

        class MeleeManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Super Smash Bros Melee Client"

        self.ui = MeleeManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def update_connection_status(ctx: MeleeContext, status):
    if ctx.connection_state == status:
        return
    else:
        #logger.info(status_messages[status])
        logger.info(status_messages)
        if get_num_dolphin_instances() > 1:
            logger.info(status_messages[ConnectionState.MULTIPLE_DOLPHIN_INSTANCES.value])
        ctx.connection_state = status


async def dolphin_sync_task(ctx: MeleeContext):
    try:
        # This will not work if the client is running from source
        version = get_apworld_version()
        logger.info(f"Using Melee apworld version: {version}")
    except:
        pass

    if ctx.apssbm_file:
        Utils.async_start(patch_and_run_game(ctx.apssbm_file))

    logger.info("Starting Dolphin Connector, attempting to connect to emulator...")

    while not ctx.exit_event.is_set():
        try:
            connection_state = ctx.game_interface.get_connection_state()
            update_connection_status(ctx, connection_state)
            if connection_state == ConnectionState.IN_MENU.value:
                await handle_check_goal_complete(ctx)  # It will say the player is in menu sometimes
            if connection_state == ConnectionState.IN_GAME.value:
                await _handle_game_ready(ctx)
            else:
                await _handle_game_not_ready(ctx)
                await asyncio.sleep(1)
        except Exception as e:
            if isinstance(e, DolphinException):
                logger.error(str(e))
            else:
                logger.error(traceback.format_exc())
            await asyncio.sleep(3)
            continue


def __int_to_reversed_bits(value: int, bit_length: int) -> str:
    """
    Converts an integer to a binary string of a specified length and reverses it.

    :param value: The integer to convert.
    :param bit_length: The length of the resulting binary string.
    :return: A reversed binary string representation of the integer.
    """
    binary_string = format(value, f'0{bit_length}b')
    return binary_string[::-1]


# async def handle_checked_location(ctx: MeleeContext, current_inventory: dict[str, InventoryItemData]):
#     """Checks for active memory relays in each world"""
#     checked_locations = []
#     i = 0
#     for mlvl, memory_relay in PICKUP_LOCATIONS:
#         if ctx.game_interface.is_memory_relay_active(f'{mlvl.value:X}', memory_relay):
#             checked_locations.append(METROID_PRIME_LOCATION_BASE + i)
#         i += 1
#     await ctx.send_msgs([{"cmd": "LocationChecks", "locations": checked_locations}])


async def handle_check_goal_complete(ctx: MeleeContext):
    if ctx.game_interface.current_game is not None:
        current_level = ctx.game_interface.get_current_level()
        if current_level == MeleeAreas.End_of_Game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ## TODO: add call to force credits after goal achieved


async def handle_check_deathlink(ctx: MeleeContext):
    health = ctx.game_interface.get_current_health()
    if health <= 0 and ctx.is_pending_death_link_reset == False:
        await ctx.send_death(ctx.player_names[ctx.slot] + " lost a stock.")
        ctx.is_pending_death_link_reset = True
    elif health > 0 and ctx.is_pending_death_link_reset == True:
        ctx.is_pending_death_link_reset = False


async def _handle_game_ready(ctx: MeleeContext):
    if ctx.server:
        ctx.last_error_message = None
        if not ctx.slot:
            await asyncio.sleep(1)
            return
        ctx.game_interface.update_relay_tracker_cache()
        current_inventory = ctx.game_interface.get_current_inventory()
        await handle_receive_items(ctx, current_inventory)
        ctx.notification_manager.handle_notifications()
        # await handle_checked_location(ctx, current_inventory)
        await handle_check_goal_complete(ctx)

        if ctx.death_link_enabled:
            await handle_check_deathlink(ctx)
        await asyncio.sleep(0.5)
    else:
        message = "Waiting for player to connect to server"
        if ctx.last_error_message is not message:
            logger.info("Waiting for player to connect to server")
            ctx.last_error_message = message
        await asyncio.sleep(1)


async def _handle_game_not_ready(ctx: MeleeContext):
    """If the game is not connected or not in a playable state, this will attempt to retry connecting to the game."""
    ctx.game_interface.reset_relay_tracker_cache()
    if ctx.connection_state == ConnectionState.DISCONNECTED:
        ctx.game_interface.connect_to_game()
    elif ctx.connection_state == ConnectionState.IN_MENU:
        await asyncio.sleep(3)


async def run_game(romfile):
    # auto_start = settings.Settings.get(key="ssbmelee_options").rom_start == True
    auto_start = settings.get_settings()["ssb_melee_options"].get("rom_start", True)
    # auto_start = Utils.get_options()["ssbmelee_options"].get("rom_start", True)

    if auto_start is True and assert_no_running_dolphin():
        import webbrowser
        webbrowser.open(romfile)
    elif os.path.isfile(auto_start) and assert_no_running_dolphin():
        subprocess.Popen([auto_start, romfile],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# GALE01 is US/KOR/JP versions
# TODO: find Revision byte
# GALP01 is EU version
def get_version_from_iso(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Couldn't get version for iso at {path}!")
    with open(path, "rb") as f:
        game_id = f.read(6).decode("utf-8")
        f.read(1)
        game_rev = f.read(1)[0]
        if game_id[:6] != "GALE01":
            raise Exception("This is not Super Smash Bros Melee")
        match game_id[3]:
            case "E":
                return "0-02"
            case "P":
                raise Exception(f"Melee PAL is currently unsupported.")


def get_options_from_apssbm(apssbm_file: str) -> dict:
    with zipfile.ZipFile(apssbm_file) as zip_file:
        with zip_file.open("options.json") as file:
            options_json = file.read().decode("utf-8")
            options_json = json.loads(options_json)
    return options_json

def get_randomizer_config_from_apssbm(apssbm_file: str) -> dict:
    with zipfile.ZipFile(apssbm_file) as zip_file:
        with zip_file.open("config.json") as file:
            config_json = file.read().decode("utf-8")
            config_json = json.loads(config_json)
    return config_json

async def patch_and_run_game(apssbm_file: str):
    return
    apssbm_file = os.path.abspath(apssbm_file)
    input_iso_path = Utils.get_options()["metroidprime_options"]["rom_file"]
    game_version = get_version_from_iso(input_iso_path)
    base_name = os.path.splitext(apssbm_file)[0]
    output_path = base_name + '.iso'

    if not os.path.exists(output_path):
        if not zipfile.is_zipfile(apssbm_file):
            raise Exception(f"Invalid apssbm file: {apssbm_file}")

        config_json = get_randomizer_config_from_apssbm(apssbm_file)
        options_json = get_options_from_apssbm(apssbm_file)

        try:
            config_json["gameConfig"]["updateHintStateReplacement"] = construct_hook_patch(game_version, build_progressive_beam_patch)
            notifier = py_randomprime.ProgressNotifier(
                lambda progress, message: print("Generating ISO: ", progress, message))
            logger.info("--------------")
            logger.info(f"Input ISO Path: {input_iso_path}")
            logger.info(f"Output ISO Path: {output_path}")
            disc_version = py_randomprime.rust.get_iso_mp1_version(os.fspath(input_iso_path))
            config_json = make_version_specific_changes(config_json, disc_version)
            logger.info(f"Disc Version: {disc_version}")
            logger.info("Patching ISO...")
            py_randomprime.patch_iso(input_iso_path, output_path, config_json, notifier)
            logger.info("Patching Complete")

        except BaseException as e:
            logger.error(f"Failed to patch ISO: {e}")
            # Delete the output file if it exists since it will be corrupted
            if os.path.exists(output_path):
                os.remove(output_path)

            raise RuntimeError(f"Failed to patch ISO: {e}")
        logger.info("--------------")

    Utils.async_start(run_game(output_path))


def launch():
    Utils.init_logging("Melee Client")

    async def main():
        multiprocessing.freeze_support()
        logger.info("main")
        parser = get_base_parser()
        parser.add_argument('apssbm_file', default="", type=str, nargs="?",
                            help='Path to an apssbm file.')
        args = parser.parse_args()

        ctx = MeleeContext(args.connect, args.password, args.apssbm_file)

        if args.apssbm_file:
            slot = get_options_from_apssbm(args.apssbm_file)["player_name"]
            if slot:
                ctx.auth = slot

        logger.info("Connecting to server...")
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        logger.info("Running game...")
        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="Dolphin Sync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await asyncio.sleep(3)
            await ctx.dolphin_sync_task

    import colorama

    colorama.init()

    asyncio.run(main())
    colorama.deinit()

def main(connect: Optional[str] = None, password: Optional[str] = None) -> None:
    """
    Run the main async loop for the Melee Client.

    :param connect: Address of the Archipelago server.
    :param password: Password for server authentication.
    """
    Utils.init_logging("Super Smash Bros Melee Client")

    async def _main(connect: Optional[str], password: Optional[str]) -> None:
        ctx = MeleeContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")

        await ctx.exit_event.wait()
        # Wake the sync task, if it is currently sleeping, so it can start shutting down when it sees that the
        # exit_event is set.
        ctx.watcher_event.set()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await ctx.dolphin_sync_task

    import colorama

    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()


if __name__ == '__main__':
    launch()
