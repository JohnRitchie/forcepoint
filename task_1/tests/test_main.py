import os
import csv
import pytest
import allure
from assertpy import assert_that
from ..main import process_request_file


@allure.suite("Distributed Rides")
class TestDistributedRides:
    # It would be more correct to put all the data in separate files.
    # But this is not done intentionally to demonstrate the use of the main features of pytest:
    # conftest, fixture and parametrize
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Distributed Rides")
    @pytest.mark.parametrize("request_file, predefined_rides, expected_output", [
        (
            'requests1.csv',
            {
                "11 times sq": 300,
                "175 Greenwich S": 450,
                "770 Broadway": 290
            },
            [
                ['Microsoft', '11 times sq', '300'],
                ['Uber', '175 Greenwich S', '450'],
                ['Amazon', '770 Broadway', '200'],
                ['Facebook', '770 Broadway', '90']
            ]
        ),
        (
            'requests2.csv',
            {
                "5th Avenue": 500,
                "Central Park": 300,
                "Wall Street": 200
            },
            [
                ['Google', '5th Avenue', '500'],
                ['Apple', 'Central Park', '300'],
                ['IBM', 'Wall Street', '200']
            ]
        ),
        (
            'requests3.csv',
            {
                "11 times sq": 300,
            },
            [
                ['Microsoft', '11 times sq', '300']
            ]
        ),
        (
            'requests4.csv',
            {
                "11 times sq": 300,
            },
            [
                ['Microsoft', '11 times sq', '300']
            ]
        ),
        (
            'requests5.csv',
            {
                "11 times sq": 300,
            },
            [
                ['Microsoft', '11 times sq', '300']
            ]
        ),
        (
            'requests6.csv',
            {
                "11 times sq": 300,
            },
            [
                ['Microsoft', '11 times sq', '300']
            ]
        ),
        (
            'requests7.csv',
            {
                "11 times sq": 300,
                "175 Greenwich S": 450,
            },
            [
                ['Microsoft', '11 times sq', '300'],
                ['Uber', '175 Greenwich S', '450'],
            ]
        )
    ])
    def test_distributed_rides(self, setup_directories, create_test_files, request_file,
                               predefined_rides, expected_output):
        input_folder, output_folder = setup_directories
        test_files = create_test_files

        input_file = os.path.join(input_folder, request_file)
        output_file = os.path.join(output_folder, request_file)
        process_request_file(input_file, output_file, predefined_rides)

        with allure.step(f"Check {output_file} format"):
            with open(output_file, newline='') as csvfile:
                reader = csv.reader(csvfile)
                result = list(reader)
                assert_that(len(result)).is_greater_than(0)
                for row in result:
                    company, destination, rides = row
                    rides = int(rides)
                    assert_that(row).is_length(3)
                    original_requests = {r[0]: int(r[2])
                                         for r in test_files[request_file] if r[1].strip() == destination}
                    assert_that(rides).is_less_than_or_equal_to(original_requests[company])

        with allure.step(f"Check that output for {request_file} matches {expected_output}"):
            assert_that(sorted(result)).is_equal_to(sorted(expected_output))


if __name__ == '__main__':
    pytest.main()
