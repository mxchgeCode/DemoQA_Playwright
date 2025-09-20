# Makefile для автоматизации запуска тестов

.PHONY: help install test smoke regression allure clean

# Переменные
PYTHON := python
PYTEST := pytest
ALLURE := allure
RESULTS_DIR := allure-results
REPORT_DIR := allure-report

help: ## Показать справку по командам
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Установить зависимости
	@echo "Устанавливаем зависимости..."
	pip install -r requirements.txt
	playwright install

test: ## Запустить все тесты
	@echo "Запускаем все тесты..."
	$(PYTEST) --alluredir=$(RESULTS_DIR)

smoke: ## Запустить smoke тесты
	@echo "Запускаем smoke тесты..."
	$(PYTEST) -m smoke --alluredir=$(RESULTS_DIR)

regression: ## Запустить regression тесты
	@echo "Запускаем regression тесты..."
	$(PYTEST) -m regression --alluredir=$(RESULTS_DIR)

elements: ## Запустить тесты Elements
	@echo "Запускаем тесты Elements..."
	$(PYTEST) -m elements --alluredir=$(RESULTS_DIR)

alerts: ## Запустить тесты Alerts
	@echo "Запускаем тесты Alerts..."
	$(PYTEST) -m alerts --alluredir=$(RESULTS_DIR)

widgets: ## Запустить тесты Widgets
	@echo "Запускаем тесты Widgets..."
	$(PYTEST) -m widgets --alluredir=$(RESULTS_DIR)

parallel: ## Запустить тесты параллельно
	@echo "Запускаем тесты параллельно..."
	$(PYTEST) -n auto --alluredir=$(RESULTS_DIR)

failed: ## Перезапустить упавшие тесты
	@echo "Перезапускаем упавшие тесты..."
	$(PYTEST) --lf --alluredir=$(RESULTS_DIR)

allure-serve: ## Запустить Allure сервер
	@echo "Запускаем Allure сервер..."
	$(ALLURE) serve $(RESULTS_DIR)

allure-generate: ## Сгенерировать HTML отчет Allure
	@echo "Генерируем HTML отчет Allure..."
	$(ALLURE) generate $(RESULTS_DIR) -o $(REPORT_DIR) --clean

allure-open: ## Открыть сгенерированный отчет
	@echo "Открываем отчет Allure..."
	$(ALLURE) open $(REPORT_DIR)

clean: ## Очистить результаты и отчеты
	@echo "Очищаем результаты..."
	rm -rf $(RESULTS_DIR) $(REPORT_DIR) .pytest_cache __pycache__
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

test-debug: ## Запустить тесты в debug режиме
	@echo "Запускаем тесты в debug режиме..."
	$(PYTEST) -v -s --tb=long --alluredir=$(RESULTS_DIR)
