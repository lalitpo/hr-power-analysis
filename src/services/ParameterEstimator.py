import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.interpolate import BSpline
from scipy.interpolate import splev
from scipy.interpolate import splrep

# Read CSV file
activity_df = pd.read_csv("/Users/lalitpoddar/Desktop/Uni/MS Project Thesis/hr-power-analysis/src/services/activity_data.csv",
                         dtype=str)

# Convert list columns to integer lists
for col in activity_df.columns:
    if col.startswith("heartrate"):
        activity_df[col] = activity_df[col].apply(lambda x: [int(i) for i in x.split(",") if i != ""])
    elif col.startswith("power"):
        activity_df[col] = activity_df[col].apply(lambda x: [int(i) for i in x.split(",") if i != ""])

# Filter activity data
activity_8746996449 = activity_df[activity_df['activity_id'] == '8746996449']
activity_8752058834 = activity_df[activity_df['activity_id'] == '8752058834']
activity_8758003008 = activity_df[activity_df['activity_id'] == '8758003008']
activity_8763450311 = activity_df[activity_df['activity_id'] == '8763450311']

# Convert lists to vectors
power_8746996449 = np.concatenate(activity_8746996449['power'].values)
heartrate_8746996449 = np.concatenate(activity_8746996449['heartrate'].values)
power_8752058834 = np.concatenate(activity_8752058834['power'].values)
heartrate_8752058834 = np.concatenate(activity_8752058834['heartrate'].values)
power_8758003008 = np.concatenate(activity_8758003008['power'].values)
heartrate_8758003008 = np.concatenate(activity_8758003008['heartrate'].values)
power_8763450311 = np.concatenate(activity_8763450311['power'].values)
heartrate_8763450311 = np.concatenate(activity_8763450311['heartrate'].values)

# Create new dataframes
activity_8746996449_data = pd.DataFrame({'power': power_8746996449, 'heartrate': heartrate_8746996449})
activity_8752058834_data = pd.DataFrame({'power': power_8752058834, 'heartrate': heartrate_8752058834})
activity_8758003008_data = pd.DataFrame({'power': power_8758003008, 'heartrate': heartrate_8758003008})
activity_8763450311_data = pd.DataFrame({'power': power_8763450311, 'heartrate': heartrate_8763450311})

# Generate B-spline
knots = np.arange(1, len(activity_8746996449_data) + 1)
spl = splrep(knots, activity_8746996449_data['heartrate'], k=3, task=-1, t=knots, full_output=0, per=0)
bspline = BSpline(spl[0], spl[1], spl[2], extrapolate=False)

# Calculate derivatives and rolling means
sample_data = activity_8746996449_data.copy().iloc[:3600]
sample_data['heartrate_rollmean'] = bspline(sample_data.index, nu=1)
sample_data['heartrate_derivate'] = np.gradient(sample_data['heartrate'], sample_data.index)
sample_data['time_derivate'] = np.gradient(sample_data['heartrate_rollmean'], sample_data.index)

# Calculate rolling means for power
power_cols = [col for col in sample_data.columns if col.startswith('power')]
for col in power_cols:
    sample_data[col + '_rollmean'] = bspline(sample_data.index, nu=1, control_points=sample_data[col])

# Perform linear regression
X_cols = ['heartrate_rollmean'] + [col + '_rollmean' for col in power_cols]
X = sm.add_constant(sample_data[X_cols])
y = sample_data['heartrate_derivate']
bs_fit_model1 = sm.OLS(y, X).fit()

# Extract regression results
resultmean = pd.DataFrame({
    'id': 'All',
    'gamma': -1 * bs_fit_model1.params['heartrate_rollmean'],
    'gamma_stde': bs_fit_model1.bse['heartrate_rollmean'],
    'yeqgamma': bs_fit_model1.params['const'],
    'yeqgamma_stde': bs_fit_model1.bse['const']
})
resultmean['tau'] = 1 / resultmean['gamma']
resultmean['yeq'] = resultmean['yeqgamma'] / resultmean['gamma']

# Perform calculations for power columns
resultmean['power_kgamma'] = bs_fit_model1.params['power_rollmean']
resultmean['power_kgamma_stde'] = bs_fit_model1.bse['power_rollmean']
resultmean['power_k'] = resultmean['power_kgamma'] * resultmean['tau']
sample_data['totalexc'] = 0
sample_data['totalexcroll'] = 0

for col in power_cols:
    sample_data['totalexc'] += bs_fit_model1.params[col + '_rollmean'] * resultmean['tau'] * sample_data[col]
    sample_data['totalexcroll'] += bs_fit_model1.params[col + '_rollmean'] * resultmean['tau'] * sample_data[col + '_rollmean']

# Generate estimated heart rate
sample_data['heartrate_estimated'] = bspline(sample_data.index, nu=1, control_points=sample_data['totalexc'], per=0)

# Calculate R2
R2 = 1 - np.sum((sample_data['heartrate'] - sample_data['heartrate_estimated']) ** 2) / np.sum((sample_data['heartrate'] - np.mean(sample_data['heartrate'])) ** 2)
if np.isnan(R2):
    R2 = 0

resultmean['R2'] = R2

res = {
    'data': sample_data,
    'resultid': None,
    'resultmean': resultmean,
    'regression': bs_fit_model1,
    'dermethod': "gold",
    'derparam': 3,
    'str_time': "time",
    'str_exc': "power",
    'str_signal': "heartrate",
    'str_id': "id"
}

# Define plot and summary functions
def plot(res):
    # Plotting code here
    pass

def summary(res):
    # Summary code here
    pass

# Call the plot and summary functions
plot(res)
summary(res)
