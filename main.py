from services.chatbot import WeddingPlannerChatbot

def main():
    print("💍 Welcome to the Wedding Planner AI Chatbot!")
    bot = WeddingPlannerChatbot()

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("👋 Wishing you a wonderful wedding journey! Goodbye!")
            break

        reply = bot.chat(user_input)
        print(f"AI : {reply}")


if __name__ == "__main__":
    main()
