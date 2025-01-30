# NetSentry - Real-time Packet Capture and Streaming

## Overview:
- NetSentry is a real-time packet capturing and streaming web application that allows you to capture network traffic using `tcpdump` and stream it live to a web interface.  
- The application supports starting and stopping packet capture, displaying live packet data, and downloading the captured packets in `.pcap` format.  
- It uses Flask for the backend and provides a frontend interface built with HTML, CSS, and JavaScript (TailwindCSS).

## Features:
- **Live Packet Capture**: Capture network packets on a specified interface (e.g., `eth0` by default) and stream them to a web interface.
- **Real-time Streaming**: The application streams live packet data to the web interface using Server-Sent Events (SSE).
- **Download .pcap File**: After capturing packets, users can download the captured traffic as a `.pcap` file.
- **Control Buttons**: Buttons to start/stop capturing packets and display relevant status updates.

## Technologies Used:
- **Backend**: Python with Flask
- **Packet Capture**: `tcpdump`
- **Frontend**: HTML, CSS (TailwindCSS), JavaScript
- **Real-time Streaming**: Server-Sent Events (SSE)
- **Cross-Origin Resource Sharing**: Flask-Cors

## Installation Instructions:
1. **Clone the repository:**
   ```bash
   git clone https://github.com/iqlipx/NetSentry.git
   cd NetSentry
   ```
2. **Install the dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   python app.py
   ```
4. Open your web browser and navigate to `http://localhost:5000`.

## Configuration:
- Change the `interface_name` variable in `app.py` to specify the network interface to capture traffic from (e.g., `eth0`, `wlan0`).
- The captured packet data is saved in `captured_traffic.pcap` file.

## Usage:
- Click the `Start Capture` button to begin capturing network traffic.
- Click the `Stop Capture` button to stop capturing and save the traffic.
- Click `Get PCAP File` to download the captured packets as a `.pcap` file.

## Screenshots:



