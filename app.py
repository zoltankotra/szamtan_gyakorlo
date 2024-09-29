import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Globális változók
current_problems = []
correct_answers = []


def generate_problem(operation):
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)

    # Ha a művelet "random mindenféle", akkor válasszon véletlenszerűen egy műveletet
    if operation == 'random':
        operation = random.choice(['+', '-', '*', '/'])

    if operation == '+':
        answer = num1 + num2
        problem = f"{num1} + {num2}"
    elif operation == '-':
        answer = num1 - num2
        problem = f"{num1} - {num2}"
    elif operation == '*':
        answer = num1 * num2
        problem = f"{num1} * {num2}"
    elif operation == '/':
        # Biztosítsuk, hogy ne oszthassunk nullával és hogy az eredmény egész szám legyen
        if num2 == 0:
            num2 = 1
        if num1 % num2 != 0:  # Ha nem egész az osztás
            num1 = num2 * random.randint(1, 10)  # Új számot generálunk, hogy biztosan egész legyen
        answer = num1 // num2
        problem = f"{num1} / {num2}"

    return problem, answer


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_problems = int(request.form['num_problems'])
        operation_type = request.form['operation']

        # Feladatok generálása
        global current_problems, correct_answers
        current_problems = []
        correct_answers = []

        for _ in range(num_problems):
            problem, answer = generate_problem(operation_type)
            current_problems.append(problem)
            correct_answers.append(answer)

        return render_template('problems.html', problems=current_problems)

    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check_answers():
    user_answers = request.form.getlist('answers')

    results = []
    incorrect_count = 0  # Hány hibás válasz volt
    for i in range(len(user_answers)):
        try:
            user_answer = int(user_answers[i])
            if user_answer == correct_answers[i]:
                results.append(f"{current_problems[i]}: Helyes válasz! Az eredmény: {correct_answers[i]}")
            else:
                results.append(f"{current_problems[i]}: Hibás válasz! A helyes válasz {correct_answers[i]}.")
                incorrect_count += 1  # Ha hibás a válasz, növeljük a hibaszámlálót
        except ValueError:
            results.append(f"{current_problems[i]}: Érvénytelen válasz.")
            incorrect_count += 1  # Érvénytelen válasz is hibának számít

    # Üzenet generálása a hibák száma alapján
    total_problems = len(correct_answers)
    if incorrect_count == 0:
        message = "Nagyon ügyes vagy, a megoldás tökéletes!"
    elif incorrect_count <= total_problems // 2:
        message = "Szép munka, de van még hova fejlődni!"
    else:
        message = "Ne aggódj, gyakorlat teszi a mestert!"

    # Eredmények megjelenítése, beleértve a hibás válaszok számát és az üzenetet is
    return render_template('results.html', results=results, incorrect_count=incorrect_count, message=message)


if __name__ == '__main__':
    app.run(debug=True)

