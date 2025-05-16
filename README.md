# Digital Platform Project

## Overview
This digital platform is designed to provide users with a seamless experience for engaging with quizzes across various topics, including programming and cybersecurity. The platform includes user authentication, quiz selection, statistics tracking, and content management features.

## Directory Structure
```
digital-platform
├── src
│   ├── main.py                # Entry point of the application
│   ├── modules
│   │   ├── welcome.py         # Module for displaying welcome messages
│   │   ├── user_auth
│   │   │   ├── login.py       # User login functionality
│   │   │   └── password.py    # Password reset functionality
│   │   ├── quiz_selection
│   │   │   ├── logic.py       # Quiz logic management
│   │   │   ├── security.py     # Security features for quiz selection
│   │   │   ├── progpy.py      # Functions for programming quizzes
│   │   │   └── cyber.py       # Functions for cybersecurity quizzes
│   │   ├── statistics
│   │   │   ├── correct_answers.py  # Tracks correct answers
│   │   │   └── average_usage_time.py # Tracks average usage time
│   │   └── content_insertion.py # Module for inserting quiz content
│   ├── data
│   │   ├── quizzes            # Directory for quiz content files
│   │   ├── user_data
│   │   │   └── users.json     # JSON file for storing user data
│   │   └── usage_statistics
│   │       ├── time.json      # JSON file for usage time statistics
│   │       └── age.json       # JSON file for age-related statistics
├── requirements.txt           # Lists project dependencies
└── README.md                  # Project documentation
```

## Setup Instructions
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using the command:
   ```
   pip install -r requirements.txt
   ```
4. Run the application by executing:
   ```
   python src/main.py
   ```

## Features
- **User Authentication**: Secure login and password reset functionalities.
- **Quiz Selection**: Users can choose from a variety of quizzes based on their interests.
- **Statistics Tracking**: The platform tracks user performance and engagement metrics.
- **Dynamic Content Insertion**: Admins can add new quizzes easily through the content insertion module.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.