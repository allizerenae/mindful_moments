import requests

BASE_URL = "http://127.0.0.1:5000"  # Default Flask local address

#Log a mood entry
def log_mood():
    mood = input("How are you feeling? (e.g. calm, anxious, tired): ")
    focus = input("What is your focus level? (low / medium / high): ")
    note = input("Any notes you'd like to add? (optional): ")

    data = {
        "mood": mood,
        "focus_level": focus,
        "note": note
    }

    response = requests.post(f"{BASE_URL}/log-mood", json=data)
    print("✅ Mood logged!" if response.status_code == 201 else f"❌ Error: {response.json()}")


#Get your mood history
def view_history():
    response = requests.get(f"{BASE_URL}/mood-history")
    if response.status_code == 200:
        logs = response.json()
        print("\n📅 Your Mood History:")
        for entry in logs:
            print(f"{entry['date_logged']}: {entry['mood']} | Focus: {entry['focus_level']} | Note: {entry['note']}")
    else:
        print("❌ Could not retrieve mood history.")


#Get a mindful moment

def get_mindful_moment():
    response = requests.get(f"{BASE_URL}/mindful-moment")
    if response.status_code == 200:
        suggestion = response.json()
        print(f"\n✨ Mindful Suggestion ({suggestion['type']}):")
        print(f"👉 {suggestion['message']}")
    else:
        print("❌ Failed to get a suggestion.")


#Main menu
def main():
    while True:
        print("\n🌿 Mindful Moments Client")
        print("1. Log Mood")
        print("2. View Mood History")
        print("3. Get a Mindful Moment")
        print("4. Exit")

        choice = input("Choose an option (1–4): ")

        if choice == "1":
            log_mood()
        elif choice == "2":
            view_history()
        elif choice == "3":
            get_mindful_moment()
        elif choice == "4":
            print("👋 Take care!")
            break
        else:
            print("❗ Invalid choice. Try again.")

if __name__ == '__main__':
    main()
