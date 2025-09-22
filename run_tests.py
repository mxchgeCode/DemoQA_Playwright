"""
Обновленный универсальный скрипт для запуска тестов.
Добавлены новые команды и улучшена функциональность.
"""

import os
import subprocess
import argparse
import sys
from pathlib import Path


class TestRunner:
    """Улучшенный класс для управления запуском тестов."""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.allure_results = self.project_root / "allure-results"
        self.allure_report = self.project_root / "allure-report"

    @staticmethod
    def run_command(command: str, capture_output: bool = False) -> tuple[int, str]:
        """Выполняет команду и возвращает код возврата и вывод."""
        print(f"🚀 Выполняем: {command}")
        try:
            if capture_output:
                result = subprocess.run(
                    command, shell=True, capture_output=True, text=True
                )
                return result.returncode, result.stdout
            else:
                result = subprocess.run(command, shell=True, check=False)
                return result.returncode, ""
        except Exception as e:
            print(f"❌ Ошибка выполнения команды: {e}")
            return 1, str(e)

    def run_tests(
        self,
        marker: str = None,
        parallel: bool = False,
        verbose: bool = True,
        html_report: bool = False,
    ):
        """Запускает тесты с указанными параметрами."""
        base_command = ["python", "-m", "pytest", "--alluredir=allure-results"]

        if verbose:
            base_command.append("-v")

        if marker:
            base_command.extend(["-m", marker])

        if parallel:
            base_command.extend(["-n", "auto"])

        if html_report:
            base_command.extend(["--html=pytest-report.html", "--self-contained-html"])

        command = " ".join(base_command)
        return self.run_command(command)[0]

    def run_specific_tests(self, test_path: str, verbose: bool = True):
        """Запускает конкретные тесты по пути."""
        command = f"python -m pytest {test_path} --alluredir=allure-results"
        if verbose:
            command += " -v"
        return self.run_command(command)[0]

    @staticmethod
    def clean_all():
        """Полная очистка всех артефактов."""
        print("🧹 Полная очистка проекта...")

        # Список директорий и файлов для удаления
        paths_to_clean = [
            "allure-results",
            "allure-report",
            ".pytest_cache",
            "htmlcov",
            "pytest-report.html",
            ".coverage",
        ]

        for path_str in paths_to_clean:
            path = Path(path_str)
            if path.is_dir():
                import shutil

                shutil.rmtree(path, ignore_errors=True)
                print(f"  ✓ Удалена директория: {path}")
            elif path.is_file():
                path.unlink(missing_ok=True)
                print(f"  ✓ Удален файл: {path}")

        # Удаляем __pycache__ и .pyc файлы
        for root, dirs, files in os.walk("."):
            for dir_name in dirs[:]:
                if dir_name == "__pycache__":
                    import shutil

                    cache_path = Path(root) / dir_name
                    shutil.rmtree(cache_path, ignore_errors=True)
                    dirs.remove(dir_name)

            for file_name in files:
                if file_name.endswith(".pyc"):
                    pyc_path = Path(root) / file_name
                    pyc_path.unlink(missing_ok=True)

        print("✅ Очистка завершена.")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description="Универсальный запускатель тестов с Allure интеграцией"
    )

    parser.add_argument(
        "action",
        choices=[
            "test",
            "smoke",
            "regression",
            "elements",
            "alerts",
            "widgets",
            "forms",
            "interactions",
            "parallel",
            "clean",
            "allure-serve",
            "allure-generate",
            "install",
            "coverage",
            "lint",
        ],
        help="Действие для выполнения",
    )

    parser.add_argument("--path", help="Путь к конкретным тестам для запуска")

    parser.add_argument(
        "--no-verbose", action="store_true", help="Отключить подробный вывод"
    )

    parser.add_argument(
        "--html-report",
        action="store_true",
        help="Дополнительно создать HTML отчет pytest",
    )

    args = parser.parse_args()

    runner = TestRunner()
    verbose = not args.no_verbose

    # Обработка специальных команд
    if args.action == "clean":
        sys.exit(runner.clean_all())

    elif args.action == "install":
        commands = ["pip install -r requirements.txt", "playwright install"]
        for cmd in commands:
            result, _ = runner.run_command(cmd)
            if result != 0:
                print(f"❌ Ошибка установки: {cmd}")
                sys.exit(result)
        print("✅ Зависимости установлены.")
        sys.exit(0)

    elif args.action == "allure-serve":
        if not runner.allure_results.exists():
            print("❌ Результаты тестов не найдены. Запустите тесты сначала.")
            sys.exit(1)
        result, _ = runner.run_command(f"allure serve {runner.allure_results}")
        sys.exit(result)

    elif args.action == "allure-generate":
        if not runner.allure_results.exists():
            print("❌ Результаты тестов не найдены. Запустите тесты сначала.")
            sys.exit(1)
        command = (
            f"allure generate {runner.allure_results} -o {runner.allure_report} --clean"
        )
        result, _ = runner.run_command(command)
        if result == 0:
            print(f"✅ HTML отчет создан: {runner.allure_report}")
        sys.exit(result)

    elif args.action == "coverage":
        result = runner.run_command(
            "python -m pytest --cov=pages --cov=locators --cov-report=html --cov-report=term --alluredir=allure-results"
        )[0]
        sys.exit(result)

    elif args.action == "lint":
        commands = [
            "flake8 pages tests locators --max-line-length=120",
            "mypy pages --ignore-missing-imports",
        ]
        for cmd in commands:
            result, _ = runner.run_command(cmd)
        sys.exit(0)

    # Обработка запуска тестов
    if args.path:
        result = runner.run_specific_tests(args.path, verbose)
    else:
        # Маппинг действий на маркеры
        action_map = {
            "test": (None, False),
            "smoke": ("smoke", False),
            "regression": ("regression", False),
            "elements": ("elements", False),
            "alerts": ("alerts", False),
            "widgets": ("widgets", False),
            "forms": ("forms", False),
            "interactions": ("interactions", False),
            "parallel": (None, True),
        }

        if args.action in action_map:
            marker, parallel = action_map[args.action]
            result = runner.run_tests(
                marker=marker,
                parallel=parallel,
                verbose=verbose,
                html_report=args.html_report,
            )
        else:
            print(f"❌ Неизвестное действие: {args.action}")
            sys.exit(1)

    sys.exit(result)


if __name__ == "__main__":
    main()
