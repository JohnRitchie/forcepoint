import csv
import os
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO)


def mock_request_rides(requested_rides: Dict[str, int], predefined_rides: Dict[str, int]) -> Dict[str, int]:
    return {key: predefined_rides.get(key, 0) for key in requested_rides}


def read_requests_from_csv(file_path: str) -> Dict[str, Dict[str, int]]:
    requests = {}
    seen_combinations = set()
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            try:
                company, destination, rides = row
                rides = int(rides.strip())
                if rides <= 0:
                    raise ValueError(f"Requested rides should be more than 0. Found: {rides}")
                if rides % 100 != 0:
                    raise ValueError(f"Requested rides should be in multiples of 100. Found: {rides}")
                destination = destination.strip()
                combination = (company, destination)
                if combination in seen_combinations:
                    raise ValueError(f"Duplicate combination of company and destination found: {combination}")
                seen_combinations.add(combination)
                requests.setdefault(destination, {})[company] = rides
            except ValueError as ve:
                logging.error(f"Error parsing row {row}: {ve}")
                continue
    return requests


def aggregate_requests(requests: Dict[str, Dict[str, int]]) -> Dict[str, int]:
    return {destination: sum(companies.values()) for destination, companies in requests.items()}


def distribute_rides(approved_rides: Dict[str, int], requests: Dict[str, Dict[str, int]]) -> Dict[str, Dict[str, int]]:
    distribution = {destination: {} for destination in approved_rides.keys()}

    for destination, approved in approved_rides.items():
        total_requested = sum(requests[destination].values())
        try:
            if approved > total_requested:
                raise ValueError(f"Approved rides {approved} for {destination} "
                                 f"exceed total requested {total_requested}")
        except ValueError as ve:
            logging.error(f"Error in approved rides : {ve}")
            approved = total_requested

        remaining_rides = approved
        companies = list(requests[destination].items())
        companies.sort(key=lambda x: x[1], reverse=True)

        # First pass: Allocate chunks of 100 as fairly as possible
        allocated_rides = {company: 0 for company, _ in companies}

        for company, requested in companies:
            if remaining_rides <= 0:
                break
            share = (requested / total_requested) * approved
            allocated = int(share // 100) * 100
            if allocated > remaining_rides:
                allocated = remaining_rides - (remaining_rides % 100)
            allocated_rides[company] += allocated
            remaining_rides -= allocated

        # Second pass: Distribute remaining rides in chunks of 100
        for company, _ in companies:
            if remaining_rides <= 0:
                break
            additional_rides = min(100, remaining_rides)
            allocated_rides[company] += additional_rides
            remaining_rides -= additional_rides

        # Distribute the allocated rides ensuring chunks of 100
        for company, rides in allocated_rides.items():
            if rides > 0:
                distribution[destination][company] = rides

    return distribution


def write_distributed_rides_to_csv(distributed_rides: Dict[str, Dict[str, int]], file_path: str) -> None:
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['company', 'destination', 'rides'])

        for destination, companies in distributed_rides.items():
            for company, rides in companies.items():
                writer.writerow({'company': company, 'destination': destination, 'rides': rides})


def process_request_file(request_file: str, output_file: str,
                         predefined_rides: Dict[str, int], with_logs: bool = True) -> None:
    requests = read_requests_from_csv(request_file)
    aggregated_requests = aggregate_requests(requests)
    approved_rides = mock_request_rides(aggregated_requests, predefined_rides)
    distributed_rides = distribute_rides(approved_rides, requests)
    write_distributed_rides_to_csv(distributed_rides, output_file)

    if with_logs:
        logging.info(f"Requests: {requests}")
        logging.info(f"Aggregated Requests: {aggregated_requests}")
        logging.info(f"Approved Rides: {approved_rides}")
        logging.info(f"Distributed Rides: {distributed_rides}")


if __name__ == "__main__":
    input_folder = 'requests'
    output_folder = 'distributed_rides'
    os.makedirs(output_folder, exist_ok=True)

    predefined_rides = {
        "11 times sq": 300,
        "175 Greenwich S": 450,
        "770 Broadway": 290
    }

    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename)
            process_request_file(input_file, output_file, predefined_rides)
