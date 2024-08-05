from typing import List, Dict, Tuple, Union
import csv


Scientist = Dict[str, Union[str, int, List[str], None]]
QueryCondition = Tuple[str, str]


def load_db(file_path: str) -> List[Scientist]:
    """
    Load scientists' data from a TSV file.

    Args:
        file_path (str): Path to the TSV file.

    Returns:
        List[Scientist]: A list of dictionaries, each representing a scientist.
    """
    scientists = []
    with open(file_path, "r") as file:
        reader = csv.reader(file, delimiter="\t")
        for row in reader:
            scientist = {
                "first_name": row[0],
                "surname": row[1],
                "sex": row[2],
                "year_of_birth": int(row[3]),
                "year_of_death": int(row[4]) if row[4] else None,
                "occupation": row[5].strip('"').split("; "),
            }
            scientists.append(scientist)
    return scientists


def parse_query(query: str) -> List[QueryCondition]:
    """
    Parse a query string into a list of query conditions.

    Args:
        query (str): A string containing one or more conditions separated by 'AND'.

    Returns:
        List[QueryCondition]: A list of tuples, each containing a field and a value.

    Raises:
        ValueError: If the query format is invalid.
    """
    conditions = query.lower().split(" and")  # 'AND' or 'and' are okay
    parsed_conditions: List[QueryCondition] = []

    for condition in conditions:
        parts = condition.split(":")
        if len(parts) == 2:
            field, value = parts
            parsed_conditions.append(
                (field.strip().lower(), value.strip().lower())
            )
        else:
            raise ValueError(f"Invalid condition format: {condition}")

    return parsed_conditions


def filter_scientists(
    scientists: List[Scientist], query: str
) -> List[Scientist]:
    """
    Filter scientists based on the given query.

    Args:
        scientists (List[Scientist]): List of scientists to filter.
        query (str): Query string to filter scientists.

    Returns:
        List[Scientist]: Filtered list of scientists matching the query.
    """
    parsed_query = parse_query(query)

    def matches_condition(
        scientist: Scientist, condition: QueryCondition
    ) -> bool:
        """
        Check if a scientist matches a single query condition.

        Args:
            scientist (Scientist): The scientist to check.
            condition (QueryCondition): The condition to match against.

        Returns:
            bool: True if the scientist matches the condition, False otherwise.
        """
        field, value = condition
        if field == "occupation":
            return value in [occ.lower() for occ in scientist[field]]
        if field == "sex":
            # Handle both 'f'/'m' and 'female'/'male' query values
            return scientist[field].lower().startswith(value[0])
        elif field == "alive-in":
            year = int(value)
            # Check if the scientist was alive in the given year
            return scientist["year_of_birth"] <= year and (
                scientist["year_of_death"] is None
                or scientist["year_of_death"] >= year
            )
        else:
            # Implicitly reject queries for unsupported attributes
            return False

    # Return scientists that match all conditions in the query
    return [
        s
        for s in scientists
        if all(matches_condition(s, cond) for cond in parsed_query)
    ]


def display_scientist(scientist: Scientist) -> None:
    """
    Utility function to pretty-print the scientist dictionary.

    Args:
        scientist (Scientist): The scientist to display.
    """
    print(f"Name: {scientist['first_name']} {scientist['surname']}")
    print(f"Sex: {scientist['sex']}")
    print(f"Born: {scientist['year_of_birth']}")
    print(
        f"Died: {scientist['year_of_death'] if scientist['year_of_death'] else 'Still alive'}"
    )
    print(f"Occupation(s): {', '.join(scientist['occupation'])}")
    print()


# Load the database
scientists = load_db("BiographicDB.tsv")

# Main query loop
while True:
    print("How can I help you?")
    query = input(">")
    if query == "":
        break
    print(parse_query(query))
    results = filter_scientists(scientists, query)
    for row in results:
        display_scientist(row)
    print(f"Your query returned {len(results)} matches.")
