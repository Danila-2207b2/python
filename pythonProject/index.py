import random
class Hero:
    def __init__(self, name, level, health=100, power=10):
        self.name = name
        self.level = level
        self.health = health
        self.power = power

    def go_on_scouting(self):
        success = random.choice([True, False])  # Успех разведки случайный
        return success


class Warrior(Hero):
    def __init__(self, name, level, health=120, power=15):
        super().__init__(name, level, health, power)

    def attack(self, enemy):
        # Логика атаки воина
        if self.health > 0 and self.level >= enemy.level:
            return True  # Победа
        else:
            return False  # Поражение


class Mage(Hero):
    def __init__(self, name, level, health=80, power=10, mana=50):
        super().__init__(name, level, health, power)
        self.mana = mana

    def cast_spell(self, enemy):
        # Логика магической атаки
        if self.mana >= 10 and self.level >= enemy.level:
            self.mana -= 10  # Расход маны
            return True  # Победа
        return False  # Поражение


class Enemy:
    def __init__(self, level):
        self.level = level
        self.health = 100 + 10 * level  # Здоровье противника


class Kingdom:
    def __init__(self):
        self.food = 100
        self.territory = 50
        self.heroes = []

    def add_hero(self, hero):
        self.heroes.append(hero)

    def feed_people(self):
        if self.food < len(self.heroes) * 10:
            return False
        self.food -= len(self.heroes) * 10
        return True

    def manage_resources(self, success, Hero=None):
        if success:
            self.food += 20  # Прибыль от успешного похода
            self.territory += 5  # Увеличение территории
            if Hero:
                Hero.level += 1
                print(f"level {Hero.level}")
        else:
            self.food -= 10  # Потеря ресурсов при провале
            self.territory -= 2  # Потеря территории при провале

    def check_revolt(self):
        if self.food < 0 or self.territory < 0:
            print("Бунт! Игра окончена!")
            return True
        return False


def main():
    kingdom = Kingdom()
    # Добавляем героев
    kingdom.add_hero(Warrior("Тимоша", level=1))
    kingdom.add_hero(Mage("Аксенчик", level=1))
    while True:
        if not kingdom.feed_people():
            print("Недостаточно пищи! Люди голодают.")
            if kingdom.check_revolt():
                break

        hero_choice = input("Выберите героя (воин/маг): ").strip().lower()
        if hero_choice not in ['воин', 'маг']:
            print("Некорректный выбор. Попробуйте снова.")
            continue

        selected_hero = next((h for h in kingdom.heroes if (isinstance(h, Warrior) and hero_choice == 'воин') or
                              (isinstance(h, Mage) and hero_choice == 'маг')), None)

        if selected_hero.go_on_scouting():
            print(f"{selected_hero.name} успешно вернулся из разведки! Ваш уровень {selected_hero.level}")
            kingdom.manage_resources(success=True)
            print(f"Продовольствие: {kingdom.food}, Территория: {kingdom.territory}")
        else:
            print(f"{selected_hero.name} неудачно прошел разведку.")
            kingdom.manage_resources(success=False)

        # Случайная встреча с противником
        enemy = Enemy(level=random.randint(0, 2))
        print(f"Встреча с противником уровня {enemy.level}!")

        action = input("Хотите сразиться (да/нет)? ").strip().lower()
        if action == 'да':
            if isinstance(selected_hero, Warrior):
                if selected_hero.attack(enemy):
                    print(f"{selected_hero.name} победил противника!")
                    kingdom.manage_resources(success=True)
                else:
                    print(f"{selected_hero.name} проиграл противнику.")
                    kingdom.manage_resources(success=False)
            elif isinstance(selected_hero, Mage):
                if selected_hero.cast_spell(enemy):
                    print(f"{selected_hero.name} победил противника!")
                    kingdom.manage_resources(success=True)
                else:
                    print(f"{selected_hero.name} проиграл противнику.")
                    kingdom.manage_resources(success=False)

        if kingdom.check_revolt():
            break

    print("Игра окончена!")


if __name__ == "__main__":
    main()