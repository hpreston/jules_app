jules_app
=========
This is the app/api layer for a personal home automation project I'm working on.  

This project provides a REST API for Arduino based sensors to periodically update with status, 
and pull down any state changes that have been indicated by a user of the system.  

Interactive clients will also interact with this project to retrieve information about 
the current status for display in web or mobile form factors.  These clients can also 
send commands back to the app layer for schedules or ASAP actions for the sensors.  
