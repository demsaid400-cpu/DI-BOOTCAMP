import random
class Game:
    def __init__(self):
        self.choices = ["rock", "paper", "scissors"]
    def get_computer_choice(self):
        return random.choice(self.choices)
    def determine_winner(self, player, computer):
        if player == computer:
            return "draw"
        elif (player == "rock" and computer == "scissors") or (player == "paper") and computer == "rock" or (player == "scissors" and computer == "paper"):
            return "player"
        else:
            return "computer"
    def play(self):
        print("=== Rock Paper Scissors ===")
        player_choice = input("Choose rock, paper or scissors: ").lower()
        if player_choice not in self.choices:
            print("Invalid choice.")
            return
        computer_choice = self.get_computer_choice()
        print(f"Computer chose: {computer_choice}")
        result = self.determine_winner(player_choice, computer_choice)
        if result == "draw":
            print("It's a draw!")
        elif result == "player":
            print("You win!")
        else:
            print("Computer wins !")
if __name__ == "__main__":
    game = Game()
    game.play()
            
        
        