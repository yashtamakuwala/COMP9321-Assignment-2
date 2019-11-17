A Data Analysis project that analyses Airbnb data of properties in Sydney, Australia(as of 14 September, 2019). Users can fill in their requirements such as - room type(private/sharing), property_type and more to get a rough idea of nightly stay they could expect to pay.

To setup all the things before running the server:
```
pip3 install -r requirements.txt
python3 db_setup.py
python3 data_setup.py
```

To run the server:
```
python3 run_tahelka.py
```
To run the client, you must have node.js installed with npm bundled. You can download from the below link
```
https://nodejs.org/en/download/
```
You will need angular CLI to run the development of Web-Client
```
npm install -g @angular/cli
```
Navigate to the web client folder and install dependencies
```
cd web
cd web-client
npm install
```
Run the Web Client
```
ng server
```
Your application can be accessed on
```
http://localhost:4200/
```
