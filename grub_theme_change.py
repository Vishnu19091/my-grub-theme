import os
import sys
import shutil
from pathlib import Path


THEMES_DIR = Path("./themes")               # Local themes folder
TARGET_DIR = Path("/boot/grub/themes")      # GRUB themes directory

GRUB_PATH=Path("/etc/default/grub")

THEMES=[d.name for d in THEMES_DIR.iterdir() if d.is_dir()]

def print_menu():
    print("Available Themes\n")
    for i,theme in enumerate(THEMES, start=1):
        print(f"{i}. {theme}")

def get_user_theme():
    try:
        choice = int(input("\nEnter option: "))
        if choice < 1 or choice > len(THEMES):
            raise ValueError
        return THEMES[choice - 1]
    except ValueError:
        print("❌ Invalid choice. Please enter a valid theme number.")
        sys.exit(1)

def generate_grub_config(theme_name:str)->str:
    return f"""
    # GRUB boot loader configuration

    GRUB_DEFAULT="saved"
    GRUB_DISTRIBUTOR="Arch"
    GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 quiet nvidia_drm.modeset=1"
    GRUB_CMDLINE_LINUX=""

    # Preload both GPT and MBR modules so that they are not missed
    GRUB_PRELOAD_MODULES="part_gpt part_msdos"

    # Uncomment to enable booting from LUKS encrypted devices
    #GRUB_ENABLE_CRYPTODISK="y"

    # Set to 'countdown' or 'hidden' to change timeout behavior,
    # press ESC key to display menu.

    # Uncomment to use basic console
    GRUB_TERMINAL_INPUT="console"

    # Uncomment to disable graphical terminal

    # The resolution used on graphical terminal
    # note that you can use only modes which your graphic card supports via VBE
    # you can see them in real GRUB with the command `videoinfo'

    # Uncomment to allow the kernel use the same resolution used by grub
    GRUB_GFXPAYLOAD_LINUX="keep"

    # Uncomment if you want GRUB to pass to the Linux kernel the old parameter
    # format "root=/dev/xxx" instead of "root=/dev/disk/by-uuid/xxx"
    #GRUB_DISABLE_LINUX_UUID="true"

    # Uncomment to disable generation of recovery mode menu entries
    GRUB_DISABLE_RECOVERY="true"

    # Uncomment and set to the desired menu colors.  Used by normal and wallpaper
    # modes only.  Entries specified as foreground/background.
    #GRUB_COLOR_NORMAL="light-blue/black"
    #GRUB_COLOR_HIGHLIGHT="light-cyan/blue"

    # Uncomment one of them for the gfx desired, a image background or a gfxtheme
    #GRUB_BACKGROUND="/path/to/wallpaper"

    # Uncomment to get a beep at GRUB start
    #GRUB_INIT_TUNE="480 440 1"

    # Uncomment to make GRUB remember the last selection. This requires
    # setting 'GRUB_DEFAULT=saved' above.
    GRUB_SAVEDEFAULT="true"

    # Uncomment to disable submenus in boot menu
    #GRUB_DISABLE_SUBMENU="y"

    # Probing for other operating systems is disabled for security reasons. Read
    # documentation on GRUB_DISABLE_OS_PROBER, if still want to enable this
    # functionality install os-prober and uncomment to detect and include other
    # operating systems.
    GRUB_DISABLE_OS_PROBER="false"
    GRUB_TIMEOUT_STYLE="menu"
    GRUB_TIMEOUT="60"
    GRUB_THEME="/boot/grub/themes/{theme_name}/theme.txt"
    GRUB_GFXMODE="auto"
    """.strip()

def write_config(content: str):
    try:
        with open(GRUB_PATH, "w") as grub:
            grub.write(content)
        print("\n✔ Theme updated successfully!\n\n")
    except PermissionError:
        print("❌ Permission denied. Run this script with sudo.")
        sys.exit(1)

def copy_theme(theme_name:str):
    source= THEMES_DIR / theme_name
    target= TARGET_DIR / theme_name

    if not source.exists():
        print(f"❌ Theme folder not found: {source}")
        sys.exit(1)

    # Create target directory if not exists
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    # Remove existing theme folder before copying
    if target.exists():
        print(f"⚠ Removing old theme folder: {target}")
        shutil.rmtree(target)

    print(f"Copying {source} → {target} ...")
    shutil.copytree(source, target)

    print("✔ Theme files copied.\n")

def main():
    print_menu()
    theme_name = get_user_theme()
    copy_theme(theme_name)
    content = generate_grub_config(theme_name)
    write_config(content)

if __name__ == "__main__":
    main()