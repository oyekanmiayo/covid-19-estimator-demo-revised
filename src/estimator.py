def get_days(period_type, time_elapsed):
    if period_type == 'days':
        return time_elapsed

    if period_type == 'weeks':
        return time_elapsed * 7

    if period_type == 'months':
        return time_elapsed * 30


def get_currently_infected_people(data, output):
    reported_cases = data['reportedCases']
    output['impact']['currentlyInfected'] = reported_cases * 10
    output['severeImpact']['currentlyInfected'] = reported_cases * 50


def get_infections_by_requested_time(data, output):
    days = get_days(data['periodType'], data['timeToElapse'])
    output['impact']['infectionsByRequestedTime'] = \
        int(output['impact']['currentlyInfected'] * (2 ** int(days / 3)))

    output['severeImpact']['infectionsByRequestedTime'] = \
        int(output['severeImpact']['currentlyInfected'] * (2 ** int(days / 3)))


def get_severe_cases_by_requested_time(output):
    output['impact']['severeCasesByRequestedTime'] = \
        int(0.15 * output['impact']['infectionsByRequestedTime'])

    output['severeImpact']['severeCasesByRequestedTime'] = \
        int(0.15 * output['severeImpact']['infectionsByRequestedTime'])


def get_hospital_beds_by_requested_time(data, output):
    available_beds = 0.35 * data['totalHospitalBeds']

    impact_severe_cases = output['impact']['severeCasesByRequestedTime']
    output['impact']['hospitalBedsByRequestedTime'] = int(available_beds - impact_severe_cases)

    s_impact_severe_cases = output['severeImpact']['severeCasesByRequestedTime']
    output['severeImpact']['hospitalBedsByRequestedTime'] = int(available_beds - s_impact_severe_cases)


def get_cases_for_icu_by_requested_time(output):
    output['impact']['casesForICUByRequestedTime'] = \
        int(0.05 * output['impact']['infectionsByRequestedTime'])

    output['severeImpact']['casesForICUByRequestedTime'] = \
        int(0.05 * output['severeImpact']['infectionsByRequestedTime'])


def get_cases_for_ventilators_by_requested_time(output):
    output['impact']['casesForVentilatorsByRequestedTime'] = \
        int(0.02 * output['impact']['infectionsByRequestedTime'])

    output['severeImpact']['casesForVentilatorsByRequestedTime'] = \
        int(0.02 * output['severeImpact']['infectionsByRequestedTime'])


def get_dollars_in_flight(data, output):
    population_perc = data['region']['avgDailyIncomePopulation']
    population_inc = data['region']['avgDailyIncomeInUSD']
    days = get_days(data['periodType'], data['timeToElapse'])

    impact_infections = output['impact']['infectionsByRequestedTime']
    output['impact']['dollarsInFlight'] = \
        int((impact_infections * population_perc * population_inc) / days)

    s_impact_infections = output['severeImpact']['infectionsByRequestedTime']
    output['severeImpact']['dollarsInFlight'] = \
        int((s_impact_infections * population_perc * population_inc) / days)


def build_estimation_output(data):
    # Assuming 'data' is a dictionary

    output = {
        'data': data,
        'impact': {},
        'severeImpact': {}
    }

    get_currently_infected_people(data, output)
    get_infections_by_requested_time(data, output)
    get_severe_cases_by_requested_time(output)
    get_hospital_beds_by_requested_time(data, output)
    get_cases_for_icu_by_requested_time(output)
    get_cases_for_ventilators_by_requested_time(output)
    get_dollars_in_flight(data, output)

    return output


def estimator(data):
    return build_estimation_output(data)

