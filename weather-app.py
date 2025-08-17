# weather-app.py
from datetime import datetime
from weather_sql import (
    init_db,
    get_current_weather,
    get_5day_forecast,
    create_weather_record,
    read_all_records,
    update_record,
    delete_record,
    export_to_csv,
    export_to_json,
    generate_google_maps_link,
    get_youtube_search_link
)

def weather_icon(desc: str) -> str:
    desc = desc.lower()
    if "clear" in desc:
        return "☀️"
    elif "cloud" in desc:
        return "☁️"
    elif "rain" in desc or "drizzle" in desc:
        return "🌧️"
    elif "thunderstorm" in desc:
        return "⛈️"
    elif "snow" in desc:
        return "❄️"
    elif "mist" in desc or "fog" in desc or "haze" in desc:
        return "🌫️"
    else:
        return "🌡️"

def main():
    init_db()

    print("### Weather App by Javisetty Siva swathi ###")
    print("Learn more about PM Accelerator: https://www.linkedin.com/company/product-manager-accelerator/\n")

    while True:
        print("\n=== Weather App Menu ===")
        print("1. View current weather")
        print("2. View 5-day forecast")
        print("3. Save weather to database")
        print("4. View saved records")
        print("5. Update a record")
        print("6. Delete a record")
        print("7. Export data (CSV/JSON)")
        print("8. Show Google Maps / YouTube links")
        print("9. Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            city = input("Enter city: ").strip()
            data = get_current_weather(city)
            if data:
                icon = weather_icon(data['desc'])
                print(f"\n{icon} {data['city']}: {data['temp']}°C, {data['desc']}")
            else:
                print("❌ Could not fetch current weather.")

        elif choice == "2":
            city = input("Enter city: ").strip()
            forecast = get_5day_forecast(city)
            if forecast:
                print("\n--- 5-Day Forecast (12:00 PM) ---")
                for day in forecast:
                    dt = datetime.strptime(day["date"], '%Y-%m-%d')
                    icon = weather_icon(day['desc'])
                    print(f"{dt.strftime('%A, %B %d')}: {day['temp']}°C, {icon} {day['desc']}")
            else:
                print("❌ Could not fetch forecast.")

        elif choice == "3":
            city = input("Enter city to save: ").strip()
            if create_weather_record(city):
                print("✅ Weather saved to database.")
            else:
                print("❌ Failed to fetch/save weather.")

        elif choice == "4":
            records = read_all_records()
            if records:
                print("\n--- Saved Records ---")
                for r in records:
                    # r[0]: id, r[1]: city, r[2]: date, r[3]: temp, r[4]: desc
                    icon = weather_icon(r[4])
                    print(f"[{r[0]}] {r[2]} - {r[1]}: {r[3]}°C, {icon} {r[4]}")
            else:
                print("📭 No records found.")

        elif choice == "5":
            try:
                rid = int(input("Enter record ID to update: ").strip())
            except ValueError:
                print("❌ Invalid ID, must be a number.")
                continue
            temp = input("New temperature (°C): ").strip()
            desc = input("New description: ").strip()
            update_record(rid, temp, desc)
            print("✅ Record updated.")

        elif choice == "6":
            try:
                rid = int(input("Enter record ID to delete: ").strip())
            except ValueError:
                print("❌ Invalid ID, must be a number.")
                continue
            confirm = input(f"Are you sure you want to delete record {rid}? (y/n): ").strip().lower()
            if confirm == 'y':
                delete_record(rid)
                print("🗑️ Record deleted.")
            else:
                print("Deletion cancelled.")

        elif choice == "7":
            fmt = input("Choose format (csv/json): ").strip().lower()
            if fmt == "csv":
                filename = export_to_csv()
                print(f"✅ Exported to {filename}")
            elif fmt == "json":
                filename = export_to_json()
                print(f"✅ Exported to {filename}")
            else:
                print("❌ Invalid format.")

        elif choice == "8":
            city = input("Enter city: ").strip()
            print(f"📍 Google Maps: {generate_google_maps_link(city)}")
            print(f"🎥 YouTube Search: {get_youtube_search_link(city)}")

        elif choice == "9":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
