import random
import re


class SimpleNeuralNetwork:
    def __init__(self):
        self.data = {}
        self.animals = []

    def add_animal(self, animal, description):
        if animal not in self.animals:
            self.animals.append(animal)
        if animal not in self.data:
            self.data[animal] = []
        self.data[animal].append(description)

    @staticmethod
    def preprocess_description(description):
        description = re.sub(r'[^\w\s]', '', description)
        return set(description.lower().split())

    def guess_animal(self, description):
        input_words = self.preprocess_description(description)
        best_match = None
        best_score = 0
        _score = 0

        for animal, descriptions in self.data.items():
            for desc in descriptions:
                desc_words = self.preprocess_description(desc)
                score = len(input_words.intersection(desc_words))

                if score > best_score:
                    if animal == best_match:
                        _score = len(desc_words)
                        best_score += score
                        best_match = animal
                    else:
                        _score = len(desc_words)
                        best_score = score
                        best_match = animal

        if best_match is not None:
            score = (best_score / _score) * 100
            return best_match, score

        return random.choice(self.animals), 0

    def learn(self, animal, description):
        if animal in self.animals:
            if description not in self.data[animal]:
                self.data[animal].append(description)
        else:
            self.add_animal(animal, description)


nn = SimpleNeuralNetwork()

nn.add_animal("кошка", "пушистая, мяукает")
nn.add_animal("собака", "пушистая, гавкает")

animal: str = ''
descr: str = ''
valid: int = 0
invalid: int = 0

dataset = open('dataset.db', 'r', encoding='utf-8').read()

for i in dataset.split('\n'):
    animal = i.split('—')[0]
    descr = i.split('—')[1]
    animal = animal.replace(' ', '')
    animal = animal.lower()
    descr = descr.lower()

    _data = nn.guess_animal(descr)

    if _data[0] == animal:
        valid += 1
    else:
        invalid += 1

    print(f'Я думаю это {_data[0]}. Уверен на {int(_data[1])}% ({True if _data[0] == animal else False})')
    nn.learn(animal, descr)


print(f'Я закончила обучаться...\n   Успешно: {valid}\n   Не успешно: {invalid}')
while True:
    data = input('Введите описание животного: ')
    try:
        descr = data.split(';')[0]
        descr = descr.lower()

    except IndexError:
        print('Вы неверно указали описание или название животного')

    _data = nn.guess_animal(descr)
    print(f'Я думаю это {_data[0]}. Уверен на {int(_data[1])}%')
