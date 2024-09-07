import asyncio
import os
import time
import random
import pynput.keyboard
import pynput.mouse
from dotenv import load_dotenv, set_key
from uuid import UUID
from pynput.keyboard import Key
from pynput.mouse import Button
from twitchAPI.helper import first
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
from twitchAPI.pubsub  import PubSub

keyboard = pynput.keyboard.Controller()
mouse = pynput.mouse.Controller()
# TODO: Fixnout dotenv
def is_file_created(setting=0):
    name_file = os.getcwd() + "\\.env"
    isFileCreated = os.path.exists(name_file)

    if setting == 0:
        if isFileCreated == True:
            load_dotenv_file()
        else:
            open(name_file, "x")

            app_id_token = input("Application ID from twitch: ")
            set_key(name_file, "APP_ID", app_id_token)

            app_secret_token = input("Application secret from twitch: ")
            set_key(name_file, "APP_SECRET", app_secret_token)

            twtich_username = input("Input your login username: ")
            set_key(name_file, "USERNAME", twtich_username)

            is_file_created()
    if setting == 1:
            try:
                open(name_file, "x")
            except FileExistsError:
                print("File is exsting")
                pass

            app_id_token = input("Application ID from twitch: ")
            set_key(name_file, "APP_ID", app_id_token)

            app_secret_token = input("Application secret from twitch: ")
            set_key(name_file, "APP_SECRET", app_secret_token)

            is_file_created()


def load_dotenv_file():
    load_dotenv()
    APP_ID = os.getenv('APP_ID')
    APP_SECRET = os.getenv('APP_SECRET')
    TWITCH_USERNAME = os.getenv('USERNAME')
    
    loop = asyncio.get_event_loop()
    
    if loop.is_running():
        asyncio.ensure_future(twitch_auth(APP_ID, APP_SECRET, TWITCH_USERNAME))
    else:
        loop.run_until_complete(twitch_auth(APP_ID, APP_SECRET, TWITCH_USERNAME))

async def twitch_auth(app_id, app_secret, twitch_username):
    twitch = await Twitch(app_id,app_secret)   

    user = await first(twitch.get_users(logins=twitch_username))

    target_scope = [AuthScope.CHANNEL_MANAGE_REDEMPTIONS, AuthScope.CHANNEL_READ_REDEMPTIONS]
    
    auth = UserAuthenticator(twitch, target_scope, force_verify=False)
    token, refresh_token = await auth.authenticate()

    await twitch.set_user_authentication(token, target_scope, refresh_token)  

    await Main(user.id, twitch)

async def Press_key(key: str):
    print(f"Pressing {key}")
        
    keyboard.press(key)
    keyboard.release(key)

# TODO: Make this for every button
async def Press_key_repeat(key: str = "space", duration: float = 5):
    print("Pressing space")
    
    start_time = time.time()
    while time.time() - start_time < duration:
        keyboard.press(Key.space)
        time.sleep(0.2)
        keyboard.release(Key.space)

async def Press_key_user_input(redemption_info = "none", duration: float = 5):
    print("Pressing keys")

    f_keys = {
        'f1': Key.f1, 'f2': Key.f2, 'f3': Key.f3, 'f4': Key.f4,
        'f5': Key.f5, 'f6': Key.f6, 'f7': Key.f7, 'f8': Key.f8,'f9': Key.f9
    }

    user_input_red = redemption_info['user_input']
    key_to_press = str(user_input_red).lower()
    
    if key_to_press[:5] == "shift":
        print("Pressing shift")
        keyboard.press(Key.shift)
        time.sleep(duration)
        keyboard.release(Key.shift)
    
    elif key_to_press[:6] == "alt+f4" or key_to_press[:8] == "alt + f4":
        gamba = random.randint(1,100)
        print(gamba)
        if gamba <= 5:
            with keyboard.pressed(Key.alt):
                keyboard.press(Key.f4)
        else:
            keyboard.press(Key.alt)
    
    elif key_to_press[:4] == "ctrl" or key_to_press[:7] == "control":
        print("Pressing ctrl")
        keyboard.press(Key.ctrl)
        time.sleep(duration)
        keyboard.press(Key.ctrl)
    
    elif key_to_press[:3] == "alt":
        print("Pressing alt")
        keyboard.press(Key.alt)
        time.sleep(duration)
        keyboard.release(Key.alt)
    
    elif key_to_press[:3] == "esc" or key_to_press[:6] == "escape":
        print("Pressing ESC")
        keyboard.press(Key.esc)
        time.sleep(duration)
        keyboard.release(Key.esc)
    
    elif key_to_press[:3] == "tab":
        print("Pressing TAB")
        keyboard.press(Key.tab)
        time.sleep(duration)
        keyboard.release(Key.tab)
    
    elif key_to_press[:3] in f_keys:
        print("Pressing F1-F12")

        keyboard.press(f_keys[key_to_press[:3]])
        keyboard.release(f_keys[key_to_press[:3]])
    
    elif key_to_press[:1] == "w" or "s" or "d" or "a":
        print(key_to_press[:1])

        keyboard.press(key_to_press[:1])
        time.sleep(duration)
        keyboard.release(key_to_press[:1])
    
    else:
        keyboard.press(key_to_press[:1])
        keyboard.release(key_to_press[:1])

async def Typing(redepmtio_info):
        user_input_red = redepmtio_info['user_input']
        by_user = redepmtio_info['user']['display_name']
        
        print("Píšu")

        keyboard.press("t")
        keyboard.release("t")
        
        time.sleep(0.2)
        
        keyboard.type(user_input_red)
        keyboard.type(f" (Napsal {by_user})")

async def Spin_me(duration: float = 5):
    print("Spining")
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        mouse.move(100, 0)
        time.sleep(0.01)

async def Mouse_button(button:int = 1, clicks:int = 1):
    print(f"Pressing mouse button chocie {button}")
    
    if button == 1:
        mouse.click(Button.left, clicks)
    elif button == 2:
        mouse.click(Button.right, clicks)
    elif button == 3:
        mouse.click(Button.middle, clicks)

async def Reward_logic_example(uuid: UUID, data: dict) -> None:
    redepmtion = data['data']['redemption']
    title = redepmtion['reward']

    if title['title'] == "space":
        await Press_key_repeat("space", 5)

    elif title['title'] == "press key":
        await Press_key("q")

    elif title['title'] == "spin me":
        await Spin_me(5)

    elif title['title'] == "click mouse":
        await Mouse_button(1, 1)
    
    elif title['title'] == "typing user input":
        await Typing(redepmtion)

    elif title['title'] == "keyboard user input":
        await Press_key_user_input(redepmtion, 5)

async def Example_rewards(userid, twitch_tokens):
    reward_price = 50
    cooldown = 2
    
    space = await twitch_tokens.create_custom_reward(userid, "space", reward_price, "space description", True, "#06D001",  is_global_cooldown_enabled = True, global_cooldown_seconds = cooldown)
    press_key = await twitch_tokens.create_custom_reward(userid, "press key", reward_price, "press key description", True, "#06D001",  is_global_cooldown_enabled = True, global_cooldown_seconds = cooldown)
    spin_me = await twitch_tokens.create_custom_reward(userid, "spin me", reward_price, "spin me description", True, "#06D001",  is_global_cooldown_enabled = True, global_cooldown_seconds = cooldown)
    click_mouse = await twitch_tokens.create_custom_reward(userid, "click mouse", reward_price, "click mouse description", True, "#06D001",  is_global_cooldown_enabled = True, global_cooldown_seconds = cooldown)
    typing = await twitch_tokens.create_custom_reward(userid, "typing user input", reward_price, "typing with user input description", True, "#06D001", True, is_global_cooldown_enabled = True, global_cooldown_seconds = cooldown)
    keyboard_user_input = await twitch_tokens.create_custom_reward(userid, "keyboard user input", reward_price, "keyboard with user input description", True, "#06D001", True, is_global_cooldown_enabled = True, global_cooldown_seconds = cooldown)

    pubsub = PubSub(twitch_tokens)
    pubsub.start()

    uuid = await pubsub.listen_channel_points(userid, Reward_logic_example)

    print("Rewards are active")
    print("Type anything to trun off rewards")

    # Quit systém
    input()
    
    print("Are you sure Y/N")
    
    while True:
        userInput = input()

        if userInput == "Y":
            pubsub.stop()
            await quit_sys(userid, twitch_tokens)

async def quit_sys(userid, twitch_tokens):
    get_rewards = await twitch_tokens.get_custom_reward(userid, only_manageable_rewards=True)
            
    for reward in get_rewards:
            print("Reward deleted")
            await twitch_tokens.delete_custom_reward(userid, reward.id)
    await Main(userid, twitch_tokens)

async def Main(userid, twitch_tokens):
    print("TakeOverGames")

    print("1 - Manual Auth")
    print("2 - Settings")
    print("3 - Example_rewards")
    print("99 - Quit")

    userInput = int(input())

    if userInput == 1:
        await twitch_auth()
    elif userInput == 2:
        is_file_created(setting=1)
    elif userInput == 3:
        await Example_rewards(userid, twitch_tokens)
    elif userInput == 99:
        quit(0)
    else:
        os.system("cls")
        await Main(userid, twitch_tokens)

if __name__ == '__main__':
    is_file_created()