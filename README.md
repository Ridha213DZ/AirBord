# AirBord

AirBord is an interactive air-drawing whiteboard application.

The system allows a user to draw in the air using hand/finger movements
captured by a webcam.

## Core Concepts

- Webcam-based hand and face interaction.
- Air drawing using finger movements.
- Whiteboard canvas.
- Drawing color selection.
- Drawing stroke-size selection.
- Gesture-based operations.
- Face-based user identification.
- Automatic profile creation for new users.
- Manual user profile registration using the keyboard.
- Personal drawing pages for each user.
- Page navigation using gestures.
- Persistent storage of user profiles and drawings.

## Initial Architecture

The project is being developed in Python.

The application will be divided into independent layers:

- Camera input
- Face detection and recognition
- Hand / finger tracking
- Gesture interpretation
- Drawing engine
- User profile management
- Drawing page management
- Persistence / storage
- Graphical user interface

## Development Principles

- Keep camera acquisition independent from computer vision processing.
- Keep computer vision independent from the UI.
- Avoid processing queues that accumulate old frames.
- Prefer the newest available camera frame for real-time interaction.
- Keep each subsystem independently testable.
- Introduce dependencies only when required.
- Make architectural decisions before implementing features.
- Maintain small, meaningful Git commits.

## Status

Project initialization.

The application architecture and development environment are being established
before implementing the main functionality.