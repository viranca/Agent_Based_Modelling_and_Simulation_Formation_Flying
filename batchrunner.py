'''
# =============================================================================
# When running this file the batchrunner will be used for the model. 
# No visulaization will happen.
# =============================================================================
'''
from mesa.batchrunner import BatchRunner
from formation_flying.model import FormationFlying
from formation_flying.parameters import model_params, max_steps, n_iterations, model_reporter_parameters, agent_reporter_parameters, variable_params
import pandas as pd
import statistics

batch_run = BatchRunner(FormationFlying,
                            fixed_parameters=model_params,
                            variable_parameters=variable_params,
                            iterations=n_iterations,
                            max_steps=max_steps,
                            model_reporters=model_reporter_parameters,
                            agent_reporters=agent_reporter_parameters
                            )

batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()



#%%
'''
# =============================================================================
#This cell drops columns from the results dataframe
# =============================================================================
'''

results_df = pd.DataFrame(run_data)

results_df = results_df.drop([ 'Run', 'Arrival Times', 'Deal values',
       'Real saved fuel', 'Total Arrival Time', 
       'Total planned Fuel', 'Total saved potential saved fuel',
       'added to formations', 'new formations', 'n_flights',
       'n_origin_airports', 'n_destination_airports', 'width', 'height',
       'speed', 'fuel_reduction', 'auction_step',
       'auction_start', 'bidding_threshold',
       'departure_window', 'area_range', 'true_value_av_amount_per'], axis=1)



#%%
mean_arrival_time_iterations = []
std_arrival_time_iterations = []

for iteration in range(len(run_data["Arrival Times"])):
    mean_of_iteration = sum(run_data["Arrival Times"][iteration])/len(run_data["Arrival Times"][iteration])
    mean_arrival_time_iterations.append(mean_of_iteration)
    
    std_of_iteration = statistics.stdev(run_data["Arrival Times"][iteration])
    std_arrival_time_iterations.append(std_of_iteration)

mean_mean_arrival_time = sum(mean_arrival_time_iterations)/len(mean_arrival_time_iterations)
std_mean_arrival_time = statistics.stdev(mean_arrival_time_iterations)

mean_std_arrival_time = sum(std_arrival_time_iterations)/len(std_arrival_time_iterations)
std_std_arrival_time = statistics.stdev(std_arrival_time_iterations)



#%%
'''
# =============================================================================
# This cell computes the mean and std of the complete results
# and creates a dataframe with just those.
# =============================================================================
'''

mean = pd.DataFrame(results_df.mean(axis=0))
std = pd.DataFrame(results_df.std(axis=0))

indicators_df = pd.concat([mean, std], axis = 1)


indicators_df.columns = ['Mean Value', 'Standard Deviation']
indicators_df['Parameter/indicator'] = indicators_df.index

n_itarations_row = {'Parameter/indicator': 'n_iterations', 'Mean Value':n_iterations, 'Standard Deviation':0}
indicators_df = indicators_df.append(n_itarations_row, ignore_index=True)

n_itarations_row = {'Parameter/indicator': 'mean_arrival_time', 'Mean Value':mean_mean_arrival_time, 'Standard Deviation':std_mean_arrival_time}
indicators_df = indicators_df.append(n_itarations_row, ignore_index=True)

n_itarations_row = {'Parameter/indicator': 'std_arrival_time', 'Mean Value':mean_std_arrival_time, 'Standard Deviation':std_std_arrival_time}
indicators_df = indicators_df.append(n_itarations_row, ignore_index=True)

column_names = ['Parameter/indicator','Mean Value','Standard Deviation']
indicators_df = indicators_df.reindex(columns = column_names)


#%%

'''
# =============================================================================
# This cell adds a percentage of the std to the mean to the dataframe.
# =============================================================================
'''

indicators_df["StD Percentage"] = (indicators_df['Standard Deviation'] / indicators_df['Mean Value']) * 100




#%%
'''
# =============================================================================
# This cell writes the dataframes of the complete results and the mean/std to a file for later use.
# =============================================================================
'''

##complete results show each individual iteration, save both for analysis.
#results_df.to_csv('complete_results_japan_200km_join0_airport3_maxsteps4000.txt', index = False)
#indicators_df.to_csv('results_japan_200km_join0_airport3_maxsteps4000.txt', index = False)


print(indicators_df)
















