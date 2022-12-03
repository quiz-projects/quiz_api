# Quiz project for the course "Python programming"

## Description
This project is a quiz game. The user is asked a question and has to answer it. The user can choose between 3 different levels of difficulty. The user can also choose to play again or quit the game.

## Features
- The user can choose between 3 different levels of difficulty
- The user can choose to play again or quit the game
- The user can see the score after each question
- The user can see the total score at the end of the game
- The user can see the correct answer if he/she answers incorrectly

## Tasks
- [x] Create a README.md file
- [x] Create a requirements.txt file
- [x] Create a .gitignore file
- [x] Create a django project
- [x] Create a django app
- [x] Create a model for the questions
- [x] Create a model for the answers
- [x] Create a model for the levels
- [x] Create a model for the score
- [x] Create a view for the home page


## API endpoints

The Quiz API has the following endpoints:
|Methode | Endpoint | Description |
|--------|----------|-------------|
|GET|/api/quiz/|Get all questions|
|GET|/api/quiz/<int:pk>/|Get a specific question|
|POST|/api/quiz/|Create a new question|
|PUT|/api/quiz/<int:pk>/|Update a specific question|
|DELETE|/api/quiz/<int:pk>/|Delete a specific question|
|POST| /api/answer/| Check the answer of the user|


