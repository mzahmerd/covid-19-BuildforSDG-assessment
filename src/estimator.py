
best_case = "best"
severe_case = "severe"

def impact_rate_every_3_days(data):
  return (2**(get_days(data)//3))

def estimator(data):
  input_data = data
  
  data = {
    'data': input_data,
    'impact': {
      'currentlyInfected' : estimate_currently_infected(input_data, best_case),
      'infectionsByRequestedTime' : estimate_infection_by_time(input_data, best_case) ,
      'severeCasesByRequestedTime' : estimate_severe_case_by_time(input_data, best_case) ,
      'hospitalBedsByRequestedTime' : estimate_beds_by_time(input_data, best_case),
      'casesForICUByRequestedTime'  : estimate_case_for_ICU_by_time(input_data, best_case),
      'casesForVentilatorsByRequestedTime' : estimate_case_for_ventilators_by_time(input_data, best_case),
      'dollarsInFlight' : estimate_dollars_in_flight(input_data, best_case)
    },
    'severeImpact': {
      'currentlyInfected' : estimate_currently_infected(input_data, severe_case),
      'infectionsByRequestedTime' : estimate_infection_by_time(input_data, severe_case) ,
      'severeCasesByRequestedTime' : estimate_severe_case_by_time(input_data, severe_case) ,
      'hospitalBedsByRequestedTime' : estimate_beds_by_time(input_data, severe_case),
      'casesForICUByRequestedTime'  : estimate_case_for_ICU_by_time(input_data, severe_case),
      'casesForVentilatorsByRequestedTime' : estimate_case_for_ventilators_by_time(input_data, severe_case),
      'dollarsInFlight' : estimate_dollars_in_flight(input_data, severe_case)

    }
  }
  return data
def estimate_currently_infected(data, case):
  if(case == "best"):
    return int(data['reportedCases'] * 10)
  else:
    return int(data['reportedCases'] * 50)

def estimate_infection_by_time(data, case):
  return int(estimate_currently_infected(data, case) * impact_rate_every_3_days(data))

def estimate_severe_case_by_time(data, case):
  return int(estimate_infection_by_time(data, case) * 0.15)

def estimate_beds_by_time(data, case):
  return int(data['totalHospitalBeds'] * 0.35 - estimate_severe_case_by_time(data,case))

def estimate_case_for_ICU_by_time(data, case):
  return int(estimate_infection_by_time(data, case) * 0.05)

def estimate_case_for_ventilators_by_time(data, case):
  return int(estimate_infection_by_time(data, case) * 0.02)

def estimate_dollars_in_flight(data, case):
  return int((estimate_infection_by_time(data, case) * data['region']['avgDailyIncomePopulation'] * data['region']['avgDailyIncomeInUSD']) / get_days(data))

def get_days(data):
  periodType = data['periodType']
  time = data['timeToElapse']
  if(periodType == 'weeks'):
    return time * 7
  elif(periodType == 'months'):
    return time * 30
  else:
    return time

data = {
  'region': {
    'name': "Africa",
    'avgAge': 19.7,
    'avgDailyIncomeInUSD': 4,
    'avgDailyIncomePopulation': 0.73
  },
  'periodType': "days",
  'timeToElapse': 38,
  'reportedCases': 2747,
  'population': 92931687,
  'totalHospitalBeds': 678874
}
  
data = estimator(data)
print(data)