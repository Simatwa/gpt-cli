apt-get install python3
pip install -r requirements.txt
chmod +x main.py
nm="gpt-cli"
DIR="/data/data/com.termux/files/usr/bin"
if [[ -d "$DIR" ]];
then
       cp main.py "$DIR"/"$nm"
else
       cp main.py /usr/bin/"$nm"
fi

echo '[*]' $nm 'installed successfully!'
sleep 2  && clear
"$nm" -v && "$nm" -h  