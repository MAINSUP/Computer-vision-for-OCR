 
⏹TASK 2⏹
Читання документів та їх перед обробка

Завдання:
Створити код для читання і передобробки зображення

Підкроки:
* Створити файл data_preprocessor.py в якому зберігатиметься механізм передобробки зображень перед АІ обробкою за допомогою opencv (посилання нижче)
* Створити файл, в якому буде відбуватися читання документу .pdf документу у вигляді зображень
* main.py - для запуску функціоналу програми, яку необхідно створити
* main.py матиме вигляд CLI, детальніше про створення CLI нижче. Можна для цього використовувати інші комфортні Вам інструменти, а не те що надано в посиланні нижче.
* CLI прийматиме як аргумент назву .pdf файлу, який необхідно обробити
* Візуалізувати зображення сторінки з документи до і після обробки (можна як і за допомогою opencv, так і інші інструменти як matplot, plotly і тд)

* Код який писали в першому завданні, перенести в папку libraries_examples

Що я хочу бачити в репозиторії?
В Readme.md повинні бути скріншоти того, як виглядає візуалізація результатів, яку робить створена Вами програма, так і команда, якою можна запустити застосунок (наприклад, python main.py --path myfile.pdf).
Наведені вище файли за описанними вимогами (в файлі data_preprocessor.py реалізувати обраний Вам підхід передобробки на основі вивченої з наведених посилань інформації).
Для тестування наведеного функціоналу, можна використовувати будь-який .pdf файл який заманеться

Посилання
CLI:
https://www.codium.ai/blog/building-user-friendly-python-command-line-interfaces-with-click/

Data processing techniques:
https://codersingh27.medium.com/preprocess-the-images-using-python-opencv-eacf4bf34477
https://www.freecodecamp.org/news/getting-started-with-tesseract-part-ii-f7f9a0899b3f/
https://nanonets.com/blog/ocr-with-tesseract/
https://towardsdatascience.com/pre-processing-in-ocr-fc231c6035a7
https://tesseract-ocr.github.io/tessdoc/ImproveQuality

Датасети для тестування передобробки:
https://guillaumejaume.github.io/FUNSD/download/
https://www.kaggle.com/datasets/aravindram11/funsdform-understanding-noisy-scanned-documents/data
https://www.kaggle.com/datasets/sthabile/noisy-and-rotated-scanned-documents/code

Для тесту можна взяти кілька документів просто
=======
⏹TASK 1⏹
Вибір бібліотек АІ для проходження інтернатури

Під які завдання обрати бібліотеки?

1. Робота з друкованим текстом на зображеннях:
https://github.com/mindee/doctr
https://github.com/JaidedAI/EasyOCR
https://pypi.org/project/pytesseract/

2. Робота з рукописним текстом на зображеннях:
https://github.com/rsommerfeld/trocr
https://pypi.org/project/handprint/
https://github.com/JaidedAI/EasyOCR
https://github.com/PaddlePaddle/PaddleOCR

3. Робота з тренуванням власних бібліотек:
https://github.com/tensorflow/tensorflow
https://github.com/pytorch/pytorch
https://github.com/BVLC/caffe

За яким принципом обирати бібліотеки?
Залежить від Вашого заліза, та зручності роботи
Бібліотеки попередня необхідно протестувати у себе, обрати яка зручніша серед всіх цих бібліотек для кожної задачі саме для Вас

Що я хочу бачити в репозиторії?

Приклади їх використання (по .py файліку для кожної бібліотеки або .ipynb, це можуть бути навіть приклади з документації бібліотеки, головне протестуйте їх)
Файл requirements.txt в якому будуть ці бібліотеки (https://www.freecodecamp.org/news/python-requirementstxt-explained/)

Також, встановити такі бібліотеки і додати їх до requirements.txt:
opencv-python
streamlit
Pillow
fitz / pymupdf

