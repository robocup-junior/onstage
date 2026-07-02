Public Area
===========

The public area is open to visitors and should be designed to ensure that participants have easy access to the performance area on stage. It should also provide a clear view for the audience to watch the teams' performances.

The figure below illustrates an exemplary floor plan of the public space, including the stage, seating area, and AV-Desk (FOH – *Front of House*), where all AV control systems are located. It also displays the recommended AV signal routing between components.

.. figure:: /_static/resources/organizers/stage_setup.svg
   :figwidth: 100%
   :align: center
   :alt: Exemplary venue layout of public area with stage, seating area, FOH, and AV signal routing

   Exemplary layout of the public area with AV signal routing

`Download Layout  </onstage/_static/resources/organizers/stage_setup.pdf>`__

The following setup is recommended for hosting a successful OnStage competition. Components required by the rules are written in **bold**.

Audio / PA-System
-----------------

The following audio devices are controlled by a mixer located at the FOH:

- **Speakers** for the audience
- *Optional:* Monitor speakers for participants on stage
- **Two wireless microphones** on stage for team use
- *Optional:* An additional wireless microphone for the stage host / MC
- **Computer** to play media provided by participants
- **3.5 mm audio jack with ~6 m cable on stage**, allowing teams to connect their robots to the audio system

Video System
------------

The following video devices are controlled by an HDMI mixer at the FOH:

- **LED wall or projector with screen**, positioned at least 1.5 m above the stage floor
- **Computer** to play media provided by participants (can be the same as for audio)
- **HDMI plug with ~6 m cable on stage**, allowing teams to connect their robots to the video system

Additionally, a wireless presenter for controlling slides is helpful for the teams.

Timer System
------------

During performances, two timers must be displayed on a separate screen:

1. A **countdown timer** showing the maximum time a team is allowed on stage, including setup and clearing (7 minutes)
2. A **stopwatch timer** measuring the team's actual performance time, excluding setup

Equipment required:

- TV screen (~48 inches) placed near the stage
- Dedicated computer at the judges table to control the timers

Recommended software for displaying the timers:

- **Timer software** `Stagetimer.io <https://stagetimer.io/>`__
- **Screen control software** `Dashmaster 2k <https://app.dashmaster2k.com/>`__ (Paid version is very affordable in the montly subscription and gives a clean look on the screen)

.. figure:: /_static/resources/organizers/timer_screen.webp
   :figwidth: 50%
   :align: center
   :alt: Screenshot showing a 7-minute countdown timer and a stopwatch timer counting up

   Exemplary timer screen layout

Setup
^^^^^

1. Create two new *Rooms* in stagetimer.io

   a. Room 1:

      - Name / Title: Stage time
      - Start: Manual
      - Duration: 00:07:00
      - Appearance: Countdown
      - Wrap-up times, yellow: 01:00, red: 00:30

   b. Room 2:

      - Name / Title: Performance time
      - Start: Manual
      - Duration: 00:01:30
      - Appearance: Count Up

2. Create *Controller* Views for the Judges controlling the timer

   a. Select *Output Links*
   b. *Viewer*
   c. Send link to Judges device and open in new browser tab
   d. Repeat the same for the other *Room* and open this link in a different browser tab
   e. Place browser tabs next to each other

3. Create a new *Daskmaster 2k* view
   
   a. Adjust view to show two elements only
   b. Edit views to show *stagetimer.io* content
   c. Grab *Stagetimer Room ID* from stagetimer.io URL: e.g. https://stagetimer.io/r/K1I22P9N/controller/ would be *K1I22P9N*
   d. Paste ID of both rooms in the two views

4. Share *Dashboard URL* with the Timer screen (either direcly on a Smart TV or though a separate computer). Hiding header and footer is possible with paid subscription.

.. TIP::
   Using a wired internet connection for viewing and controlling device is recommended, as Wifi will lead to a higher latency!

**Alternative to TV screen:**
Two sports timers that can be remotely controlled from the judges' table

.. figure:: /_static/resources/organizers/sports_timer.webp
   :figwidth: 50%
   :align: center
   :alt: Sports timer

.. WARNING::
   It is required to make sure, that the timers don't both react on the same remote control signal, so they can be started and stopped independently!
