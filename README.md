# Time Recorder
<div style="text-align:center; padding: 20px;">
  <img src="https://github.com/alex-roh/Time-Activity-Recorder/assets/54312875/f83c6170-6b3e-4761-a085-eed309d43e2a" alt="GUI screen" style="height: 400px;">
</div>
The Time Recorder is a simple desktop application designed to track and measure how much time you spend on various activities throughout the day. It provides a visual pie chart that lets you see a distribution of your time across different tasks.

## Features
- **Activity Selection**: Choose from a predefined list of activities, or simply type in your own.
- **Start & Stop Timing**: Start and stop the timer to record sessions of your activities.
- **Activity Log**: Displays a list of your recorded sessions, along with their start, end, and duration.
- **Data Persistence**: Save your recorded sessions to a .json file for future reference and load past session data back into the application.
- **Visual Representation**: Visualize your time distribution across different tasks using a pie chart.
- **Timezone Aware**: By default, this app uses the KST (Korea Standard Time) timezone.

## Installation
1. Ensure you have Python installed on your system.
2. Install the required libraries:
    ```bash
    pip install tkinter matplotlib pytz
    ```

## How to Use
1. Run the script
    ```bash
    python time_recorder.py
    ```
2. Select an activity from the dropdown or type in your own.
3. Press the Start button to start the timer.
4. Press the Stop button to stop the timer and log the activity session.
5. View your sessions in the Activity Log section.
6. To save your sessions, click the Save button. This will create a .json file with the current timestamp. (default location: ./saved_sessions/)
7. To load previous sessions, click the Load button and select the relevant .json file.
8. To visualize your time distribution, click the Show Graph button. This will display a pie chart showing the distribution of time across activities.
9. To clear all sessions, click the Clear button.

## Note
The application will automatically update the timer every 50 milliseconds.

## Developer
This application was developed by Alex Roh.

## License
Free for personal use. Commercial use requires permission.


