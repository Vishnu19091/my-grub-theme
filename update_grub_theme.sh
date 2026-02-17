# SCRIPT TO UPDATE GRUB THEME

SCRIPT_DIR=$(dirname -- "$(readlink -f -- "$0")")
sudo python3 $SCRIPT_DIR/grub_theme_change.py

echo -e "Theme changed in the configuration file"

sudo grub-mkconfig -o /boot/grub/grub.cfg
