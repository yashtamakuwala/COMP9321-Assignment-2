A Data Analysis and Machine Learning project that analyses Airbnb data of properties in Sydney, Australia(as of 14 September, 2019). Users can fill in their requirements such as - room type(private/sharing), property_type and more to get a rough idea of nightly stay they could expect to pay.

## Running the Application

First, install all requirements:
```
pip3 install -r requirements.txt
```

Next, run the script to setup the database and clean the dataset:
```
python3 setup_all.py -d
```

Set the `JWT_SECRET` environment variable to any string you like to make the JWT authentication secure.

Run the server:
```
python3 run_tahelka.py
```
When the server is running, its swagger documentation can be accessed on `http://[hostname]:5000/api/v1/`

To run the client, you must have node.js installed with npm bundled. You can download from the below link:
```
https://nodejs.org/en/download/
```
You will need angular CLI to run the development of Web-Client:
```
npm install -g @angular/cli
```
Navigate to the web client folder and install dependencies:
```
cd web
cd web-client
npm install
```
Run the Web Client:
```
ng serve
```
The web client can be accessed on:
```
http://localhost:4200/
```
