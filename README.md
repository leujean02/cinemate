# CineMate Lex Bot

CineMate is an AWS Lex bot designed to help users search for movies by title, with options to filter results based on the release year. Users can ask for movie recommendations or search for specific titles, and the bot will refine its responses accordingly.

I have included the Lambda function that powers the back-end logic of this bot in the file `lambda_function.py`, which handles API integration and data fetching using Python.

## Technologies Used

- **AWS Lex**: Natural language processing for understanding user inputs.
- **AWS Lambda**: Backend logic implemented in Python, including API integration for fetching movie data from external sources.
- **Python**: Used to develop the Lambda function for API handling and back-end logic.