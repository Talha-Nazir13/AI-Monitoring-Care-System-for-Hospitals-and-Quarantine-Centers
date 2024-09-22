<h1>AI Monitoring Care System for Hospitals and Quarantine Centers</h1>

<p>This project implements an AI-based monitoring system designed for hospitals and quarantine centers. It uses machine learning and computer vision to detect fall events and irregular activities of patients, raising alarms for caretakers when necessary. The system provides a real-time monitoring interface, generates activity reports in JSON format, and supports video-based detection using a graphical interface (Tkinter).</p>

<h2>Project Overview</h2>
<ul>
  <li><strong>Objective:</strong> To create an AI-powered system that monitors fall detection and irregular activities in hospitals or quarantine centers, generating real-time alerts and comprehensive activity reports.</li>
  <li><strong>Core Features:</strong> 
    <ul>
      <li>Real-time fall and activity detection using video analysis.</li>
      <li>Generates alerts for caretakers in case of critical events like falls.</li>
      <li>Produces detailed JSON reports of detected activities.</li>
      <li>Displays live graphs for activity data.</li>
      <li>Easy-to-use graphical interface built with Tkinter.</li>
    </ul>
  </li>
  <li><strong>Technologies Used:</strong> OpenCV, NumPy, Tkinter, JSON, and PIL (Python Imaging Library).</li>
</ul>

<h2>Features</h2>
<ul>
  <li><strong>Fall Detection:</strong> Detects falls based on visual cues from a live or recorded video feed and triggers an alarm for caretakers.</li>
  <li><strong>Activity Detection:</strong> Monitors irregular or suspicious movements and logs these activities.</li>
  <li><strong>Graphical Interface:</strong> Provides a user-friendly interface where users can select a video, run detection, and view results in real-time.</li>
  <li><strong>JSON Reports:</strong> Automatically generates reports containing timestamped activities in JSON format, which can be saved for future reference.</li>
</ul>

<h2>Installation</h2>
<p>To run this project locally, ensure you have Python and the required libraries installed. Follow the steps below:</p>

<pre>
<code>git clone https://github.com/your-username/ai-monitoring-care-system.git
cd ai-monitoring-care-system
pip install -r requirements.txt
</code>
</pre>

<h2>Running the Application</h2>
<ol>
  <li>Run the Python script using the command:</li>
  <pre><code>python ai_monitoring_system.py</code></pre>
  <li>Log in using the provided credentials (Username: <strong>aicare</strong>, Password: <strong>123</strong>).</li>
  <li>Select a video file to be monitored using the "Select Video" button.</li>
  <li>Click "Run Detection" to start the monitoring process. Detected activities (including fall events) will appear in the output box.</li>
  <li>To save a report of the detected activities in JSON format, click "Save Report."</li>
  <li>To exit the application, click the "Exit" button.</li>
</ol>

<h2>Technologies Used</h2>
<ul>
  <li><strong>OpenCV:</strong> For video processing and fall/activity detection using image analysis.</li>
  <li><strong>NumPy:</strong> For numerical computations and handling image data.</li>
  <li><strong>Tkinter:</strong> For creating the graphical user interface (GUI).</li>
  <li><strong>PIL (Python Imaging Library):</strong> For displaying the video frames within the Tkinter GUI.</li>
  <li><strong>JSON:</strong> For storing activity logs in a structured format for future reference.</li>
</ul>

<h2>Project Structure</h2>
<ul>
  <li><strong>ai_monitoring_system.py:</strong> Main application file containing the logic for video processing, activity detection, and the Tkinter interface.</li>
  <li><strong>requirements.txt:</strong> Lists all necessary dependencies for the project.</li>
</ul>

<h2>Activity Detection Logic</h2>
<ul>
  <li>The system processes each frame from the video feed to detect significant movements.</li>
  <li>Ellipses are drawn around detected objects, and specific angles and distances are calculated to identify falls or other irregular activities.</li>
  <li>When an event is detected (such as a fall), it is logged, and the alarm triggers if a fall is confirmed.</li>
  <li>The user can save the activity report in JSON format.</li>
</ul>

<h2>Contributing</h2>
<p>Contributions to improve this project are welcome! Feel free to submit pull requests or open issues for bugs, improvements, or suggestions.</p>


<h2>Acknowledgments</h2>
<ul>
  <li>Thanks to the developers of OpenCV and the Python libraries used in this project.</li>
  <li>Special thanks to healthcare workers, as this project aims to support patient care in hospitals and quarantine settings.</li>
</ul>
