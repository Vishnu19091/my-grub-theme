# SCRIPT TO UPDATE GRUB THEME

sudo python3 ./grub_theme_change.py

echo -e "Theme changed in the configuration file"

sudo grub-mkconfig -o /boot/grub/grub.cfg