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


- Multiple-choice: a question that presents a list of possible answers, and the person taking the quiz must choose the correct answer from the options provided.

- True/false: a question that presents a statement, and the person taking the quiz must determine whether the statement is true or false.

- Fill-in-the-blank: a question that presents a sentence with one or more words missing, and the person taking the quiz must fill in the blanks with the correct words.

- Matching: a question that presents a list of items on one side, and a list of corresponding items on the other side, and the person taking the quiz must match the items on one side with the correct items on the other side.

- Short answer: a question that requires the person taking the quiz to provide a brief, written response to the question.

- Essay: a question that requires the person taking the quiz to write a longer, more detailed response to the question.

- Ordering: a question that presents a list of items that must be placed in a specific order, and the person taking the quiz must arrange the items in the correct order.

- Ranking: a question that presents a list of items, and the person taking the quiz must rank the items in order of importance, preference, or some other criteria.

- Grouping: a question that presents a list of items that must be organized into specific groups or categories, and the person taking the quiz must correctly group the items.

- Picture identification: a question that presents a picture or image, and the person taking the quiz must identify the objects, people, or scenes depicted in the picture.