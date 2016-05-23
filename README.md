#Interop LCD display with HTTP and REST server
##Downloading and installing the libraries
This project uses the [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) library.

Download it, move to the `python` directory, and build it by following the instructions noted in the README.

##Creating the database
The `interopLCD.py` script uses a sqlite3 database to display all the posted texts.

Type the following to create a database.
```
$ python
>>> from interopLCD import init_db
>>> init_db()
```
The folder which the database will be created is written in `interopLCD.py`, so change it to whereever you want it to be.

##Starting the script
Type `sudo python interopLCD.py -b 25 -r 16 -c 2` in order to start the script.

Please refer the arguments from the `wledmatrix.py` file.

##Controlling the LCD from a web browser
The `interopLCD.py` script uses Flask to create a HTTP server.

Please change the argument `host='10.24.128.182'` in the `app.run()`function in the `interopLCD.py` file to the appropriate IP address.

##Accessing the REST server
The `interopLCD.py` script also uses Flask to create a REST server.

Test the REST server by typing `curl -i -H "Content-Type: application/json" -X POST -d '{"background":"black","text":"Hello World!","color":"white"}' http://<Raspberry Pi IP address>:5000/rest/api/data`.
