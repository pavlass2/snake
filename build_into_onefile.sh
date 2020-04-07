pyinstaller \
	--noconfirm \
	--onefile \
	--name snake_onefile \
	--add-data ./snake/img/apple.png:img \
	--add-data ./snake/img/wall.png:img \
	--add-data ./snake/img/snake.png:img \
	./snake/main.py
rm /dist/snake.zip
mkdir ./dist/temp/
cp ./dist/snake_onefile ./dist/temp/snake
cp -r ./snake/img/ ./dist/temp/
cd ./dist/temp
zip ../snake.zip -r .*
cd ..
rm -r ./temp
cd ..
