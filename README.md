## WebChat
This project is an attempt to create an instant messaging website, similar to WhatsApp Web.<br/><br/>
The website currently supports:
- Individual Chats
- Group chats
- Multi media messaging (images, audios, videos, etc)

## Steps to Set Up The Webpage
1. Create a docker container for the mongo db server<br/>
   `docker run -d -p 27017:27017 mongodb-server mongo:latest`
   
2. Create the config properties file (Location: src/configuration/config.properties)<br/>
   `CLOUD_NAME={Cloudinary Cloud Name / Username}`<br/>
   `API_KEY={Cloudinary API Key}`<br/>
   `API_SECRET={Cloudinary API Secret}`<br/>
   `FLASK_SECRET_KEY={Unique Secret Key}`<br/>
   `MONGODB_DB_STRING={NOT USED! IGNORE!}`<br/>
   `MESSAGE_LIMIT_PER_SCREEN={Provide integer value}`<br/>
   
3. Start the Flask server<br/>
   `python main.py`

4. Visit `localhost:8080` to access the page. Sign up and then login to the website. Enjoy!

## Tech Stack
- Backend: Flask Web Server (Python based)
- Front End: HTML + CSS + Javascript + Bootstrap
- Data Base: MongoDB (SQL databases are also supported)
- Messaging: WebSockets (For lower latency and faster performance, compared to HTTP requests)

## Further Development
- Further development of the project, to add support for audio and video calls, are being considered.
- The project is open to any of sort of help, suggestions or criticisms.

## Screenshots

### Login Screen:
<p align="center">
  <img src="https://github.com/user-attachments/assets/4b7d535c-68ff-4f02-860f-b2d99621c0db" width="900">
<p/>

### Chat Window:
<p align="center">
  <img src="https://github.com/user-attachments/assets/fa35558f-6e75-4115-9b9c-b00cc930fdeb" width="900">
<p/>

### View Images In Chat:
<p align="center">
  <img src="https://github.com/user-attachments/assets/62a24ac3-f808-48e6-803f-a72bd325c0ba" width="900">
<p/>

### Create New Groups:
<p align="center">
  <img src="https://github.com/user-attachments/assets/0487eddf-df58-462e-af1c-92a7f29fdd4b" width="900">
<p/>


<!-- ------------- -->
<!-- to do -->

<!-- 1. One user is to be displayed when app is starting
2. incoperate image sending
3. incoperate voice sending
4. incoperate voice calling
5. search feature 
6.

![Screenshot (20)](https://github.com/user-attachments/assets/4b7d535c-68ff-4f02-860f-b2d99621c0db)
![Screenshot (21)](https://github.com/user-attachments/assets/fa35558f-6e75-4115-9b9c-b00cc930fdeb)
![Screenshot (22)](https://github.com/user-attachments/assets/62a24ac3-f808-48e6-803f-a72bd325c0ba)
![Screenshot (23)](https://github.com/user-attachments/assets/0487eddf-df58-462e-af1c-92a7f29fdd4b)


-->
