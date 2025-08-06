import google.generativeai as genai
import os
from dotenv import load_dotenv

class GeminiChatBot:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        prompt = f"""You are a rock-paper-scissors game.

            Please do the following:
            1. First, check if the user wants to exit the game (they might say "exit", "quit", "stop", "bye", "goodbye", or similar)
            - If they want to exit, respond with exactly: "EXIT_GAME_TOKEN"
            2. Validate the user's choice (rock, paper, or scissors).
            - If the user enters an invalid choice (not rock/paper/scissors and not wanting to exit), respond with an error message asking them to choose rock, paper, scissors, or exit.
            3. If it's a valid game choice, choose your own move randomly (rock, paper, or scissors)
            4. Determine who wins based on the rules:
            - Rock beats scissors
            - Paper beats rock  
            - Scissors beats paper
            - Same choice = tie

            For valid game moves, format your response like this:
            My choice: [your choice]
            Result: [who won and why]
        """
        self.model = genai.GenerativeModel('gemini-2.5-pro', system_instruction=prompt)
        self.chat = self.model.start_chat()

    def get_gemini_response(self, prompt):
        try:
            response = self.chat.send_message(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error getting Gemini response: {e}")
            return "I'm having trouble connecting. Let's try again!"

    def play(self):
        print("Let's play Rock, Paper, Scissors with Gemini!")
        print("You can say 'exit', 'quit', 'stop', or similar to end the game.\n")
        
        while True:
            user_choice = input("Enter your choice (rock, paper, scissors) or say when you want to quit: ")
            
            response = self.get_gemini_response(user_choice)
            
            # Check if Gemini returned the exit token
            if "EXIT_GAME_TOKEN" in response:
                print("Thanks for playing! Goodbye!")
                break
            
            print("\n" + response)
            print("-" * 50)  # Separator between games

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    # Try to get API key from environment variable first
    api_key = os.getenv('GEMINI_API_KEY')
    
    # If not found in environment, prompt user for it
    if not api_key:
        api_key = input("Enter your Gemini API key: ").strip()
        if not api_key:
            print("API key is required to run the game.")
            exit(1)
    
    bot = GeminiChatBot(api_key)
    bot.play()