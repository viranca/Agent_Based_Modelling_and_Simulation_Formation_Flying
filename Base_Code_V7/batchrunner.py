'''
# =============================================================================
# When running this file the batchrunner will be used for the model. 
# No visulaization will happen.
# =============================================================================
'''
from mesa.batchrunner import BatchRunner
from formation_flying.model import FormationFlying
from formation_flying.parameters import model_params, max_steps, n_iterations, model_reporter_parameters, agent_reporter_parameters, variable_params


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
#run_data.head()

#print((run_data["Real saved fuel"] - run_data["Total saved potential saved fuel"])/ run_data["Total Fuel Used"])
print(" ")
print("Model Results:")
print(run_data["negotiation_method"])
print(run_data["joining_method"])
print(run_data["communication_range"])
print(run_data["Total Fuel Used"])
print(run_data["total_manager_change"])
print(run_data["Run"])
print(run_data["steps"])
print(run_data.columns)