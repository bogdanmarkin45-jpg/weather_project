import json
import datetime
import matplotlib.pyplot as plt

class WeatherEntry:
    def __init__(self, date, temperature, description, precipitation):
        self._date = date
        self._temperature = temperature
        self.description = description
        self.precipitation = precipitation

    @property
    def date(self): return self._date

    @property
    def temperature(self): return self._temperature

    def to_dict(self):
        return {
            "date": self.date.strftime("%Y-%m-%d"),
            "temperature": self.temperature,
            "description": self.description,
            "precipitation": self.precipitation,
            "type": "General"
        }

class ExtremeWeatherEntry(WeatherEntry):
    def __init__(self, date, temperature, description, precipitation, warning_level):
        super().__init__(date, temperature, description, precipitation)
        self.warning_level = warning_level

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "Extreme"
        data["warning"] = self.warning_level
        return data

class WeatherDiary:
    def __init__(self, filename='data.json'):
        self.filename = filename
        self.entries = self.load_data()

    def add_entry(self, entry):
        self.entries.append(entry)
        self.save_data()

    def delete_entry(self, index):
        if 0 <= index < len(self.entries):
            self.entries.pop(index)
            self.save_data()

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([e.to_dict() for e in self.entries], f, indent=4, ensure_ascii=False)

    def load_data(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [WeatherEntry(datetime.datetime.strptime(d['date'], "%Y-%m-%d"), 
                                    d['temperature'], d['description'], d['precipitation']) for d in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def filter_by_temp(self, min_t, max_t):
        return [e for e in self.entries if min_t <= e.temperature <= max_t]

    def plot_temp(self):
        if not self.entries: return print("Нет данных для графика")
        sorted_entries = sorted(self.entries, key=lambda x: x.date)
        dates = [e.date.strftime("%d.%m") for e in sorted_entries]
        temps = [e.temperature for e in sorted_entries]
        
        plt.figure(figsize=(10, 5))
        plt.plot(dates, temps, marker='o', color='tab:blue')
        plt.title("Дневник температуры")
        plt.xlabel("Дата")
        plt.ylabel("Температура (°C)")
        plt.grid(True)
        plt.show()

def get_valid_date():
    while True:
        try:
            date_str = input("Введите дату (ГГГГ-ММ-ДД): ")
            return datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Ошибка! Формат должен быть ГГГГ-ММ-ДД.")

def get_valid_temp():
    while True:
        try:
            return float(input("Введите температуру: "))
        except ValueError:
            print("Ошибка! Введите число.")

def main():
    diary = WeatherDiary()
    while True:
        print("\n1. Добавить 2. Показать 3. Удалить 4. Фильтр 5. График 6. Выход")
        choice = input("Выберите действие: ")
        
        if choice == '1':
            date = get_valid_date()
            temp = get_valid_temp()
            desc = input("Описание: ")
            prec = input("Осадки: ")
            diary.add_entry(WeatherEntry(date, temp, desc, prec))
        elif choice == '2':
            for i, e in enumerate(diary.entries):
                print(f"{i}. {e.date.date()} | {e.temperature}°C | {e.description}")
        elif choice == '3':
            try:
                idx = int(input("Индекс для удаления: "))
                diary.delete_entry(idx)
            except ValueError:
                print("Введите корректное число")
        elif choice == '4':
            print("Мин. температура:")
            t1 = get_valid_temp()
            print("Макс. температура:")
            t2 = get_valid_temp()
            for e in diary.filter_by_temp(t1, t2):
                print(f"{e.date.date()}: {e.temperature}°C")
        elif choice == '5':
            diary.plot_temp()
        elif choice == '6':
            break

if __name__ == "__main__":
    main()
