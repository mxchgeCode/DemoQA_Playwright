# DemoQA_Playwright


Как запустить тесты с разными браузерами(Chromium, Firefox) через CLI:

```shell
   pytest --profile=full
````
или запустить в браузере Chromium:
```shell
   pytest --profile=demo
```
или запустить в Chromium в headless:
```shell
   pytest --profile=smoke
```


Автоматизированные тесты созданные с использованием pytest и playwright

Реализованы проверки:

1. Прогресс бар на странице (https://demoqa.com/progress-bar)
2. Слайдер на странице (https://demoqa.com/slider)
3. Текстовый аккордеон на странице (https://demoqa.com/accordian)
4. Поля ввода с автозаполнением на странице (https://demoqa.com/auto-complete) 

