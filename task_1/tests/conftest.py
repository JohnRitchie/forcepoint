import os
import csv
import pytest
import allure


# It would be more correct to put all the data in separate files.
# But this is not done intentionally to demonstrate the use of the main features of pytest:
# conftest, fixture and parametrize
@pytest.fixture(scope="module")
def setup_directories():
    input_folder = 'requests_for_tests'
    output_folder = 'distributed_rides_for_tests'

    with allure.step("Creating directories for test files"):
        os.makedirs(input_folder, exist_ok=True)
        os.makedirs(output_folder, exist_ok=True)

    yield input_folder, output_folder

    with allure.step("Deleting test files"):
        for folder in [input_folder, output_folder]:
            for filename in os.listdir(folder):
                os.remove(os.path.join(folder, filename))

    with allure.step("Deleting directories for test files"):
        os.rmdir(input_folder)
        os.rmdir(output_folder)


@pytest.fixture(scope="function")
def create_test_files(setup_directories):
    input_folder, _ = setup_directories
    test_files = {
        'requests1.csv': [
            ['Microsoft', '11 times sq', '300'],
            ['Uber', '175 Greenwich S', '700'],
            ['Facebook', '770 Broadway', '100'],
            ['Amazon', '770 Broadway', '200']
        ],
        'requests2.csv': [
            ['Google', '5th Avenue', '500'],
            ['Apple', 'Central Park', '300'],
            ['IBM', 'Wall Street', '200']
        ],
        'requests3.csv': [
            ['Microsoft', '11 times sq', '300'],
            ['175 Greenwich S', '700']
        ],
        'requests4.csv': [
            ['Microsoft', '11 times sq', '300'],
            ['Uber', '700']
        ],
        'requests5.csv': [
            ['Microsoft', '11 times sq', '300'],
            ['Uber', '175 Greenwich S', '-700']
        ],
        'requests6.csv': [
            ['Microsoft', '11 times sq', '300'],
            ['Uber', '175 Greenwich S', '%!№-=+']
        ],
        'requests7.csv': [
            ['Microsoft', '11 times sq', '300'],
            ['Uber', '175 Greenwich S', '70000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000']
        ]
    }

    with allure.step("Creating test files"):
        for filename, rows in test_files.items():
            with open(os.path.join(input_folder, filename), 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)

    yield test_files

