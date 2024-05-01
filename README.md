**installation**
**clone this repository**

git clone https://github.com/muhammedseydali/taxi-app/new/main
cd project

**pip install -r requirements.txt**

Enter
python manage.py runserver

**WebSocket Connection:**

Connect to the WebSocket endpoint using appropriate WebSocket client libraries or tools.
WebSocket URL: ws://localhost:8000/ws/taxi/

**Sending Messages:**
Supported message types: create.trip, update.trip, echo.message.



**Dependencies**
Django Channels
Django
Other dependencies specified in requirements.txt



**About this project**
This Django Channels consumer handles WebSocket connections for managing taxi trips between riders and drivers.



The TaxiConsumer class is responsible for handling WebSocket connections and performing various operations related to taxi trips, including creating and updating trips, managing connections between drivers and riders, and sending/receiving messages.


**Functionality**

Connect: Handles WebSocket connections and adds the consumer to appropriate groups based on user authentication and trip details.

Create Trip: Creates a new trip, sends trip data to all available drivers, and adds the rider to the trip group.

Update Trip: Updates trip details, sends updated trip data to the rider, and adds the driver to the trip group.

Disconnect: Handles WebSocket disconnections and removes the consumer from groups.

