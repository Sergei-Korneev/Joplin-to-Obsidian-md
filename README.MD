# Конвертер мобильного профиля Joplin в хранилище Obsidian

Скрипт на Python для конвертации мобильного профиля Joplin в заметки Obsidian.

Инструкции:

- Экспортируйте профиль Joplin (Конфигурация->Экспортировать Профиль) на карту устройства и скопириуйте его на локальный диск.

- Установите Python3 и запустите в консоли комманду ```pip install markdownify``` и потом ```python3 convert.py [путь к папке профиля т.е. d:\joplin или /media/sdcard/joplin]``` 
Скрипт создаст подпапку с именем Obsidian и запишет туда все ноутбуки и заметки (папка должна иметь права на запись)

- Все.

* * *

# Joplin Mobile To Obsidian Vault

Python script to convert Joplin mobile exported profile to Obsidian plain text MD files.

Instructions:

- Export your Joplin profile (Configuration->Export Profile) to SDCARD and copy it to your local disk

- Install Python3 and run in your console ```pip install markdownify``` and then ```python3 convert.py [path to the profile folder e.g. d:\joplin or /media/sdcard/joplin]``` 
The script will create a subfolder called Obsidian and write all notebooks and notes there (the folder should be writable)

- That is it.


## Donations

Share your  wishes and ideas about this software or buy me a coffee (or hot chocolate)

[![Buy me a coffee](https://img.shields.io/badge/-buy_me_a%C2%A0coffee-gray?logo=buy-me-a-coffee)](https://www.buymeacoffee.com/sergeikorneev)


