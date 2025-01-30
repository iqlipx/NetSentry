import subprocess
import time
import os
import threading
from flask import Flask, Response, render_template, send_file, jsonify
from flask_cors import CORS

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable cross-origin resource sharing

# Set your network interface here
interface_name = 'eth0'  # Change this to your interface name (e.g., eth0,)

pcap_file = 'captured_traffic.pcap'  # File to store captured packets

# Global variables for capturing
capture_thread = None
capture_process = None
is_capturing = False  # Flag to track if capturing is active


@app.route('/')
def home():
    """Home route that renders the main page."""
    return render_template('index.html', interface_name=interface_name)


def start_tcpdump():
    """Starts tcpdump to capture packets on the specified interface."""
    global capture_process
    command = ['sudo', 'tcpdump', '-i', interface_name, '-w', pcap_file, '-nn', '-v', '-l']
    print(f"Starting tcpdump on interface {interface_name}...")

    capture_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the process to complete or be terminated
    while capture_process and capture_process.poll() is None:
        time.sleep(1)


@app.route('/start')
def start_capture():
    """Start capturing packets."""
    global capture_thread, is_capturing
    if not is_capturing:
        is_capturing = True
        capture_thread = threading.Thread(target=start_tcpdump)
        capture_thread.start()
        return jsonify({"status": "Capture started"}), 200
    return jsonify({"status": "Capture is already running"}), 400


@app.route('/stop')
def stop_capture():
    """Stop capturing packets."""
    global capture_process, is_capturing
    if is_capturing:
        is_capturing = False
        if capture_process:
            capture_process.terminate()  # Terminate the tcpdump process
            capture_process = None
        return jsonify({"status": "Capture stopped"}), 200
    return jsonify({"status": "No capture process found"}), 400


@app.route('/download')
def download_pcap():
    """Download the captured packets as a .pcap file."""
    if os.path.exists(pcap_file):
        return send_file(pcap_file, as_attachment=True)
    return jsonify({"status": "PCAP file not found"}), 404


def capture_packets_live():
    """Captures packets live and streams them."""
    command = ['sudo', 'tcpdump', '-i', interface_name, '-nn', '-v', '-l']  # -l for line-buffered output
    print(f"Capturing packets live on interface {interface_name}...")

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Stream the output from tcpdump
    while is_capturing and process.poll() is None:
        output = process.stdout.readline()

        if output:
            packet_data = output.decode('utf-8').strip()

            # Send each line as an SSE event
            yield f"data: {packet_data}\n\n"

        # Add a small delay to prevent CPU overload
        time.sleep(0.1)

    process.terminate()  # Ensure tcpdump is stopped when not capturing


@app.route('/stream')
def stream_packets():
    """Streams real-time packet data."""
    if not is_capturing:
        return jsonify({"error": "Capture not started"}), 400
    return Response(capture_packets_live(), content_type='text/event-stream;charset=utf-8', status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
