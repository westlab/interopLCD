#Interop LED matrix display with HTTP and REST server
##1. Downloading and installing the libraries
This project uses the [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) library.

Download it, move to the `python` directory, and build it by following the instructions noted in the README.

##2. Creating the database
The `interopLCD.py` script uses a sqlite3 database to display all the posted texts.

Type the following to create a database.
```
$ python
>>> from interopLCD import init_db
>>> init_db()
```
The folder which the database will be created is written in `interopLCD.py`, so change it to whereever you want it to be.

##3. Starting the script
Type `sudo python interopLCD.py -b 25 -r 16 -c 2` in order to start the script.

Please refer the arguments from the `wledmatrix.py` file.

##4. Accessing the REST server
The `interopLCD.py` script also uses Flask to create a REST server.

Test the REST server by typing `curl -i -H "Content-Type: application/json" -X POST -d '{"background":"black","text":"Hello World!","color":"white"}' http://<Raspberry Pi IP address>:5000/api/lcd`.
##5. Displaying the data from DooR
The DooR program sends data via socket communication.

Run `python doorpost.py` in order to receive data from the DooR program and send that data to the REST server.
