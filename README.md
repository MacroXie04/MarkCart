# MarkCart

MarkCart is a web application that generates creative recipes based on selected ingredients using OpenAI's GPT-4o model. Users can select from categorized food items, and the application will generate a complete recipe including a creative name, ingredients list, cooking instructions, and tips.

## Features

- User authentication (register, login, logout)
- Ingredient selection from categorized food items
- AI-powered recipe generation using OpenAI's GPT-4o
- Recipe history to view past generated recipes
- Responsive and user-friendly interface

## Technologies Used

- Django 5.2
- OpenAI API (GPT-4o model)
- SQLite database
- HTML/CSS
- Bootstrap (for styling)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/MarkCart.git
   cd MarkCart
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`
   - Or set it directly in your environment variables

5. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser (admin):
   ```
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```
   python manage.py runserver
   ```

8. Access the application at http://127.0.0.1:8000/

## Usage

1. Register a new account or log in with existing credentials
2. On the main page, select ingredients from different categories
3. Click "Submit" to generate a recipe
4. View the generated recipe with detailed instructions
5. Access your recipe history to view past generated recipes

## Adding Food Items

To add new food items and categories:

1. Log in to the admin panel at http://127.0.0.1:8000/admin/
2. Navigate to "Food Item Categories" to add new categories
3. Navigate to "Food Items" to add new ingredients and assign them to categories

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- OpenAI for providing the GPT-4o API
- Django community for the excellent web framework
