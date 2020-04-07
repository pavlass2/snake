pyinstaller \
	--noconfirm \
	--name snake \
	--add-data ./snake/img/apple.png:img \
	--add-data ./snake/img/wall.png:img \
	--add-data ./snake/img/snake.png:img \
	./snake/main.py
