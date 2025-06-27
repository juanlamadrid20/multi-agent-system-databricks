import os
from agents import function_tool
from census import Census
from us import states


@function_tool
def get_state_census_data(state_code: str) -> str:
    """
    Get census data for a specific state.

    Args:
        state_code: The two-letter state code (e.g., 'MD' for Maryland)

    Returns:
        A formatted string with the state name, population, and median household income
    """
    print("INFO: `get_state_census_data` tool called")
    c = Census(os.getenv("CENSUS_API_KEY"))
    state_obj = getattr(states, state_code.upper())
    results = c.acs5.get(
        (
            "NAME",
            "B11016_001E",  # total households
            "B25081_001E",  # owner occupied households
            "B01003_001E",  # total population
            "B19013_001E",  # median household income
            "B15003_022E",  # bachelors degree graduates
            "B15003_023E",  # masters degree graduates
            "B15003_025E",  # doctorate degree graduates
        ),
        {"for": "state:{}".format(state_obj.fips)},
    )

    if results:
        state_name = results[0]["NAME"]
        total_households = int(results[0]["B11016_001E"] or 0)
        owner_occupied_households = int(results[0]["B25081_001E"] or 0)
        population = int(results[0]["B01003_001E"] or 0)
        median_income = int(results[0]["B19013_001E"] or 0)
        bachelors_degree_graduates = int(results[0]["B15003_022E"] or 0)
        masters_degree_graduates = int(results[0]["B15003_023E"] or 0)
        doctorate_degree_graduates = int(results[0]["B15003_025E"] or 0)

        # Calculate percentages and ratios
        owner_occupied_percent = (
            (owner_occupied_households / total_households * 100)
            if total_households
            else 0
        )
        people_per_household = (
            (population / total_households) if total_households else 0
        )
        bachelors_percent = (
            (bachelors_degree_graduates / population * 100) if population else 0
        )
        masters_percent = (
            (masters_degree_graduates / population * 100) if population else 0
        )
        doctorate_percent = (
            (doctorate_degree_graduates / population * 100) if population else 0
        )

        return (
            f"{state_name} has an estimated population of {round(population)} and a median household income of ${round(median_income)}. "
            f"{round(owner_occupied_percent, 1)}% of households are owner-occupied with an average of {round(people_per_household, 2)} people per household. "
            f"Education levels: {round(bachelors_percent, 1)}% have a bachelor's degree, {round(masters_percent, 1)}% have a master's degree, "
            f"and {round(doctorate_percent, 1)}% have a doctorate degree."
        )
    else:
        return f"No census data found for state code {state_code}."