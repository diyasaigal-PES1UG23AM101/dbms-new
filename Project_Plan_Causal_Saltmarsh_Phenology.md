# 📊 Project Plan: Causal Analysis of Coastal Saltmarsh Phenology

**Project Title:** Quantifying the Heterogeneous Causal Impact of Climate Variables on Coastal Saltmarsh Phenological Shifts using Satellite Panel Data

**Objective:** Move beyond correlation to establish causal relationships between climate variables and changes in saltmarsh phenology, specifically quantifying Average Treatment Effect (ATE) and Heterogeneous Treatment Effect (HTE) across different marsh salinity types.

**Methodology:** Fixed Effects Panel Regression with Interaction Terms

**Time Frame:** August - December 2025

---

## 1. ⚙️ Technical Stack and Tools

### Primary Programming Language
- **Python 3.10+** (recommended for scientific computing and ecosystem compatibility)

### Core Libraries and Environments

#### Data Acquisition & Geospatial Processing
- **Google Earth Engine (GEE) Python API** (`earthengine-api`) - Satellite data access
- **geopandas** - Spatial data manipulation
- **rasterio** - Raster data I/O
- **xarray** - Multi-dimensional arrays for geospatial time-series
- **netCDF4** - NOAA climate data handling

#### Time-Series Analysis & Phenology Extraction
- **numpy** - Numerical computing
- **pandas** - Panel data structure and manipulation
- **scipy** - Signal processing (smoothing, filtering)
- **scikit-learn** - Preprocessing utilities

#### Econometric Modeling
- **linearmodels** - Panel data regression (Fixed Effects, Random Effects)
- **statsmodels** - Statistical modeling and diagnostics
- **pymc** (optional) - Bayesian causal inference

#### Visualization & Reporting
- **matplotlib** - Plotting
- **seaborn** - Statistical visualization
- **plotly** - Interactive visualizations
- **jupyter** - Interactive development environment

#### Data Storage
- **h5py** - Efficient storage of large time-series arrays
- **sqlite3** or **PostgreSQL** - Panel data database (optional)

### Development Environment
- **Jupyter Notebook/Lab** - Interactive analysis
- **VS Code** or **PyCharm** - Code development
- **Git** - Version control

---

## 2. 🗺️ Phase 1: Data Acquisition and Structuring

### 2.1 Data Sources

#### Outcome Variables (Y): Phenological Metrics
- **MODIS Terra/Aqua** (MOD13Q1, MYD13Q1) - 16-day NDVI/EVI composites, 250m resolution, 2000-present
- **Landsat 5/7/8/9** (Collection 2) - 16-day NDVI composites, 30m resolution, 1984-present
- **Access Method:** Google Earth Engine (GEE) or NASA Earthdata

#### Treatment Variables (T): Climate Data
- **NOAA OISST v2.1** - Daily Sea Surface Temperature (SST), 0.25° resolution, 1981-present
- **NOAA Climate Data Online (CDO)** - Precipitation data (daily/monthly)
- **NASA GPM IMERG** - Global Precipitation Measurement, 0.1° resolution
- **NOAA Tides & Currents** - Sea level proxies (tidal gauge stations)
- **Access Method:** NOAA ERDDAP, NASA GES DISC, or direct API

#### Heterogeneity Variable: Marsh Salinity Categories
- **USGS Coastal Change Analysis Program (C-CAP)** - Land cover classification
- **NOAA Coastal Assessment Framework** - Marsh salinity zonation maps
- **Field survey data** (if available) - Ground-truth salinity measurements
- **Access Method:** USGS EarthExplorer, NOAA Digital Coast

### 2.2 Spatial Filtering and Study Area Definition

```python
# Pseudocode: Define Study Area
def define_study_area(coastline_shapefile, buffer_distance_km=5):
    """
    Create a buffer zone around coastal areas for saltmarsh extraction.
    
    Parameters:
    - coastline_shapefile: Vector file of coastline
    - buffer_distance_km: Distance to extend inland/seaward
    
    Returns:
    - study_area_geometry: Shapely geometry object
    """
    # Load coastline
    coastline = gpd.read_file(coastline_shapefile)
    
    # Create buffer (convert km to meters)
    buffer_m = buffer_distance_km * 1000
    study_area = coastline.buffer(buffer_m)
    
    # Merge all polygons
    study_area_merged = study_area.unary_union
    
    return study_area_merged
```

### 2.3 Panel Data Structure Creation

```python
# Pseudocode: Create Panel Data Structure
def create_panel_structure(satellite_data, climate_data, marsh_salinity_map):
    """
    Organize data into panel format: Unit (i) x Time (t) structure.
    
    Panel Structure:
    - Unit ID (i): Unique identifier for each marsh pixel/polygon
    - Time ID (t): Year or seasonal period (e.g., 2000-2024)
    - Variables:
        * Y_it: Phenological metrics (SOS, EOS, LOGS)
        * T_it: Climate variables (SST, Precipitation, Sea Level)
        * X_it: Control variables (if any)
        * Z_i: Time-invariant heterogeneity (Salinity Category)
    
    Returns:
    - panel_df: pandas DataFrame with MultiIndex (unit_id, time_id)
    """
    # Initialize panel list
    panel_records = []
    
    # For each marsh unit (pixel or polygon)
    for unit_id, marsh_location in enumerate(marsh_units):
        # Extract time-invariant characteristics
        salinity_category = extract_salinity(marsh_location, marsh_salinity_map)
        latitude = marsh_location.centroid.y
        longitude = marsh_location.centroid.x
        
        # For each time period
        for time_id, time_period in enumerate(time_series):
            # Extract outcome variables
            ndvi_ts = extract_ndvi_time_series(marsh_location, time_period, satellite_data)
            
            # Extract treatment variables
            sst = extract_sst(marsh_location, time_period, climate_data)
            precipitation = extract_precipitation(marsh_location, time_period, climate_data)
            sea_level = extract_sea_level(marsh_location, time_period, climate_data)
            
            # Create record
            record = {
                'unit_id': unit_id,
                'time_id': time_id,
                'year': time_period.year,
                'salinity_category': salinity_category,  # Z_i (time-invariant)
                'latitude': latitude,
                'longitude': longitude,
                'sst': sst,  # T_it
                'precipitation': precipitation,  # T_it
                'sea_level': sea_level,  # T_it
                'ndvi_ts': ndvi_ts  # Will be processed in Phase 2
            }
            panel_records.append(record)
    
    # Convert to DataFrame
    panel_df = pd.DataFrame(panel_records)
    panel_df = panel_df.set_index(['unit_id', 'time_id'])
    
    return panel_df
```

### 2.4 Data Quality Checks

- **Temporal Coverage:** Ensure continuous time-series (handle missing data)
- **Spatial Alignment:** Resample all rasters to common resolution and projection
- **Outlier Detection:** Flag extreme values in climate and NDVI data
- **Missing Data Strategy:** Interpolation or exclusion criteria

---

## 3. 📈 Phase 2: Feature Engineering (Phenology Extraction)

### 3.1 NDVI Time-Series Preprocessing

```python
# Pseudocode: Time-Series Smoothing
def smooth_ndvi_time_series(ndvi_raw, method='savitzky_golay'):
    """
    Smooth NDVI time-series to reduce noise and cloud contamination.
    
    Parameters:
    - ndvi_raw: 1D array of NDVI values (length = number of observations)
    - method: 'savitzky_golay', 'whittaker', or 'double_logistic'
    
    Returns:
    - ndvi_smooth: Smoothed NDVI time-series
    """
    if method == 'savitzky_golay':
        from scipy.signal import savgol_filter
        # Window length should be odd and less than time-series length
        window_length = min(7, len(ndvi_raw) // 2)
        if window_length % 2 == 0:
            window_length += 1
        ndvi_smooth = savgol_filter(ndvi_raw, window_length, polyorder=3)
    
    elif method == 'whittaker':
        from pywhittaker import whittaker
        ndvi_smooth = whittaker(ndvi_raw, lmbda=10)
    
    elif method == 'double_logistic':
        # Fit double logistic curve
        from scipy.optimize import curve_fit
        def double_logistic(t, a, b, c, d, e, f):
            return a + (b - a) / (1 + np.exp(-c * (t - d))) + (e - b) / (1 + np.exp(-f * (t - d)))
        # Initial parameter estimates
        p0 = [0.2, 0.8, 0.1, 100, 0.2, 0.1]
        popt, _ = curve_fit(double_logistic, np.arange(len(ndvi_raw)), ndvi_raw, p0=p0)
        ndvi_smooth = double_logistic(np.arange(len(ndvi_raw)), *popt)
    
    return ndvi_smooth
```

### 3.2 Phenological Metric Extraction

```python
# Pseudocode: Calculate Phenological Metrics
def extract_phenology_metrics(ndvi_smooth, dates, method='threshold'):
    """
    Extract Start of Season (SOS), End of Season (EOS), and Length of Growing Season (LOGS).
    
    Parameters:
    - ndvi_smooth: Smoothed NDVI time-series (1D array)
    - dates: Corresponding dates (datetime array)
    - method: 'threshold', 'derivative', or 'relative_threshold'
    
    Returns:
    - sos: Start of Season (day of year)
    - eos: End of Season (day of year)
    - logs: Length of Growing Season (days)
    """
    # Calculate annual amplitude
    ndvi_min = np.min(ndvi_smooth)
    ndvi_max = np.max(ndvi_smooth)
    ndvi_amplitude = ndvi_max - ndvi_min
    
    if method == 'threshold':
        # Threshold method: 20% of amplitude above minimum
        threshold = ndvi_min + 0.2 * ndvi_amplitude
        
        # Find SOS: first crossing above threshold in spring
        spring_indices = np.where((ndvi_smooth[:-1] < threshold) & 
                                  (ndvi_smooth[1:] >= threshold))[0]
        if len(spring_indices) > 0:
            sos_idx = spring_indices[0]
            sos = dates[sos_idx].timetuple().tm_yday
        else:
            sos = np.nan
        
        # Find EOS: last crossing below threshold in fall
        fall_indices = np.where((ndvi_smooth[:-1] >= threshold) & 
                                (ndvi_smooth[1:] < threshold))[0]
        if len(fall_indices) > 0:
            eos_idx = fall_indices[-1]
            eos = dates[eos_idx].timetuple().tm_yday
        else:
            eos = np.nan
    
    elif method == 'derivative':
        # Derivative method: maximum rate of increase (SOS) and decrease (EOS)
        ndvi_derivative = np.diff(ndvi_smooth)
        
        # SOS: maximum positive derivative in first half of year
        first_half = len(ndvi_derivative) // 2
        sos_idx = np.argmax(ndvi_derivative[:first_half])
        sos = dates[sos_idx].timetuple().tm_yday
        
        # EOS: maximum negative derivative in second half of year
        second_half = first_half
        eos_idx = second_half + np.argmin(ndvi_derivative[second_half:])
        eos = dates[eos_idx].timetuple().tm_yday
    
    elif method == 'relative_threshold':
        # Relative threshold: percentile-based
        ndvi_median = np.median(ndvi_smooth)
        threshold_low = np.percentile(ndvi_smooth, 25)
        threshold_high = np.percentile(ndvi_smooth, 75)
        
        # SOS: crossing from below 25th percentile to above median
        sos_idx = np.where((ndvi_smooth[:-1] < threshold_low) & 
                           (ndvi_smooth[1:] >= ndvi_median))[0]
        sos = dates[sos_idx[0]].timetuple().tm_yday if len(sos_idx) > 0 else np.nan
        
        # EOS: crossing from above 75th percentile to below median
        eos_idx = np.where((ndvi_smooth[:-1] >= threshold_high) & 
                           (ndvi_smooth[1:] < ndvi_median))[0]
        eos = dates[eos_idx[-1]].timetuple().tm_yday if len(eos_idx) > 0 else np.nan
    
    # Calculate LOGS
    if not (np.isnan(sos) or np.isnan(eos)):
        logs = eos - sos
        if logs < 0:  # Handle year boundary crossing
            logs = 365 - sos + eos
    else:
        logs = np.nan
    
    return sos, eos, logs
```

### 3.3 Feature Engineering Pipeline

```python
# Pseudocode: Complete Feature Engineering Pipeline
def feature_engineering_pipeline(panel_df):
    """
    Apply phenology extraction to all units in panel data.
    
    Returns:
    - panel_df_enhanced: Panel DataFrame with phenological metrics added
    """
    phenology_metrics = []
    
    for (unit_id, time_id), row in panel_df.iterrows():
        ndvi_ts = row['ndvi_ts']
        dates = row['dates']  # Corresponding dates for NDVI time-series
        
        # Smooth time-series
        ndvi_smooth = smooth_ndvi_time_series(ndvi_ts, method='savitzky_golay')
        
        # Extract phenology
        sos, eos, logs = extract_phenology_metrics(ndvi_smooth, dates, method='threshold')
        
        phenology_metrics.append({
            'unit_id': unit_id,
            'time_id': time_id,
            'sos': sos,
            'eos': eos,
            'logs': logs
        })
    
    # Merge phenology metrics into panel
    phenology_df = pd.DataFrame(phenology_metrics)
    phenology_df = phenology_df.set_index(['unit_id', 'time_id'])
    
    panel_df_enhanced = panel_df.join(phenology_df)
    
    return panel_df_enhanced
```

### 3.4 Additional Features

- **Lag Variables:** Create lagged climate variables (T_{t-1}, T_{t-2}) for temporal effects
- **Cumulative Effects:** Sum of climate variables over growing season
- **Extreme Events:** Binary indicators for heatwaves, droughts, floods
- **Spatial Features:** Distance to coast, elevation (if available)

---

## 4. 🧠 Phase 3: Causal Modeling (Fixed Effects Regression)

### 4.1 Model Formulation

#### Core Fixed Effects Panel Regression Equation

The model accounts for unobserved heterogeneity through unit and time fixed effects, and incorporates interaction terms to capture heterogeneous treatment effects:

$$Y_{it} = \alpha_i + \gamma_t + \beta_1 T_{it} + \beta_2 (T_{it} \times Z_i) + \beta_3 X_{it} + \epsilon_{it}$$

**Where:**
- $Y_{it}$ = Outcome variable (SOS, EOS, or LOGS) for unit $i$ at time $t$
- $\alpha_i$ = Unit fixed effect (captures time-invariant characteristics of marsh $i$)
- $\gamma_t$ = Time fixed effect (captures year-specific shocks common to all units)
- $T_{it}$ = Treatment variable (SST, Precipitation, or Sea Level) for unit $i$ at time $t$
- $Z_i$ = Heterogeneity variable (Salinity Category: Freshwater, Brackish, Saline) - **time-invariant**
- $T_{it} \times Z_i$ = Interaction term (captures heterogeneous treatment effect)
- $X_{it}$ = Control variables (optional: lagged climate, spatial features)
- $\epsilon_{it}$ = Error term (assumed i.i.d. with mean zero)

#### Interpretation of Coefficients

- **$\beta_1$ (ATE):** Average Treatment Effect - the average causal effect of treatment $T$ on outcome $Y$ across all marsh types
- **$\beta_2$ (HTE):** Heterogeneous Treatment Effect - how the treatment effect varies by salinity category $Z$
  - For a given salinity category $Z_k$, the total effect is: $\beta_1 + \beta_2 \cdot Z_k$

#### Extended Model with Multiple Treatments

For multiple climate variables:

$$Y_{it} = \alpha_i + \gamma_t + \sum_{j=1}^{J} \left[ \beta_{1j} T_{jit} + \beta_{2j} (T_{jit} \times Z_i) \right] + \beta_3 X_{it} + \epsilon_{it}$$

Where $J$ is the number of treatment variables (e.g., SST, Precipitation, Sea Level).

### 4.2 Code Outline: Fixed Effects Regression

```python
# Python Code: Fixed Effects Panel Regression
import pandas as pd
import numpy as np
from linearmodels import PanelOLS
from linearmodels.panel import compare

def fit_fixed_effects_model(panel_df, outcome_var='logs', treatment_vars=['sst', 'precipitation']):
    """
    Fit Fixed Effects Panel Regression model with interaction terms.
    
    Parameters:
    - panel_df: Panel DataFrame with MultiIndex (unit_id, time_id)
    - outcome_var: Name of outcome variable ('sos', 'eos', 'logs')
    - treatment_vars: List of treatment variable names
    
    Returns:
    - results: Regression results object
    """
    # Prepare data
    df = panel_df.copy()
    
    # Create interaction terms for each treatment variable
    # Assuming salinity_category is encoded as: 0=Freshwater, 1=Brackish, 2=Saline
    for treatment in treatment_vars:
        df[f'{treatment}_x_salinity'] = df[treatment] * df['salinity_category']
    
    # Define formula
    # Main effects
    main_effects = ' + '.join(treatment_vars)
    
    # Interaction effects
    interactions = ' + '.join([f'{t}_x_salinity' for t in treatment_vars])
    
    # Control variables (if any)
    controls = ''  # Add control variables here if needed
    if controls:
        formula = f'{outcome_var} ~ {main_effects} + {interactions} + {controls}'
    else:
        formula = f'{outcome_var} ~ {main_effects} + {interactions}'
    
    # Fit Fixed Effects model
    # entity_effects=True: Unit fixed effects (α_i)
    # time_effects=True: Time fixed effects (γ_t)
    model = PanelOLS.from_formula(
        formula,
        data=df,
        entity_effects=True,  # α_i
        time_effects=True,    # γ_t
        drop_absorbed=True    # Drop perfectly collinear variables
    )
    
    # Estimate model
    results = model.fit(cov_type='clustered', cluster_entity=True)  # Cluster standard errors at unit level
    
    return results

# Example usage
# results = fit_fixed_effects_model(panel_df_enhanced, outcome_var='logs', 
#                                   treatment_vars=['sst', 'precipitation', 'sea_level'])

# Print results
# print(results.summary)

# Extract coefficients
# ate_sst = results.params['sst']  # Average Treatment Effect of SST
# hte_sst = results.params['sst_x_salinity']  # Heterogeneous Treatment Effect
```

### 4.3 Alternative: Using statsmodels (if linearmodels unavailable)

```python
# Alternative: Using statsmodels (less efficient for large panels)
import statsmodels.api as sm
from statsmodels.regression.linear_model import OLS

def fit_fixed_effects_statsmodels(panel_df, outcome_var='logs', treatment_vars=['sst']):
    """
    Fit Fixed Effects using dummy variables (statsmodels approach).
    Note: This is less efficient for large panels but more flexible.
    """
    df = panel_df.copy().reset_index()
    
    # Create unit and time dummies
    unit_dummies = pd.get_dummies(df['unit_id'], prefix='unit', drop_first=True)
    time_dummies = pd.get_dummies(df['time_id'], prefix='time', drop_first=True)
    
    # Create interaction terms
    for treatment in treatment_vars:
        df[f'{treatment}_x_salinity'] = df[treatment] * df['salinity_category']
    
    # Prepare X matrix
    X_vars = treatment_vars + [f'{t}_x_salinity' for t in treatment_vars]
    X = df[X_vars].join(unit_dummies).join(time_dummies)
    X = sm.add_constant(X)
    
    # Outcome variable
    y = df[outcome_var]
    
    # Fit model
    model = OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups': df['unit_id']})
    
    return model
```

### 4.4 Model Diagnostics

```python
# Pseudocode: Model Diagnostics
def perform_diagnostics(results, panel_df):
    """
    Perform statistical checks for regression model validity.
    """
    diagnostics = {}
    
    # 1. Residual Analysis
    residuals = results.resids
    diagnostics['residual_normality'] = perform_shapiro_wilk_test(residuals)
    diagnostics['residual_heteroskedasticity'] = perform_breusch_pagan_test(results)
    
    # 2. Multicollinearity Check
    diagnostics['vif'] = calculate_variance_inflation_factor(results)
    
    # 3. Unit Root Test (for time-series)
    diagnostics['unit_root'] = perform_adf_test(panel_df[outcome_var])
    
    # 4. Fixed Effects Test
    # Test if fixed effects are necessary
    diagnostics['hausman_test'] = perform_hausman_test(random_effects_model, fixed_effects_model)
    
    return diagnostics
```

---

## 5. 🔬 Phase 4: Interpretation and Validation (HTE Analysis)

### 5.1 Coefficient Interpretation

#### Average Treatment Effect (ATE)

For a treatment variable $T$ (e.g., SST):

$$\text{ATE} = \beta_1$$

**Interpretation:** A one-unit increase in SST causes, on average, a $\beta_1$ unit change in the outcome variable (e.g., LOGS in days), holding all else constant.

**Example:** If $\beta_1 = -2.5$ for SST on LOGS, then a 1°C increase in SST reduces the length of growing season by 2.5 days on average across all marsh types.

#### Heterogeneous Treatment Effect (HTE)

For interaction term $T \times Z$:

$$\text{HTE for Salinity Category } Z_k = \beta_2 \cdot Z_k$$

**Total Effect for Category $Z_k$:**
$$\text{Total Effect} = \beta_1 + \beta_2 \cdot Z_k$$

**Interpretation:** The treatment effect differs by $\beta_2$ units for each unit increase in salinity category.

**Example:** 
- If $\beta_1 = -2.5$ (ATE) and $\beta_2 = 1.5$ (HTE coefficient)
- For Freshwater marshes ($Z = 0$): Total Effect = $-2.5 + 1.5 \times 0 = -2.5$ days
- For Brackish marshes ($Z = 1$): Total Effect = $-2.5 + 1.5 \times 1 = -1.0$ days
- For Saline marshes ($Z = 2$): Total Effect = $-2.5 + 1.5 \times 2 = 0.5$ days

This indicates that saline marshes are more resilient to SST increases (or even benefit), while freshwater marshes are more vulnerable.

### 5.2 HTE Analysis Strategy

```python
# Pseudocode: HTE Analysis and Visualization
def analyze_heterogeneous_effects(results, panel_df, treatment_var='sst'):
    """
    Analyze and visualize heterogeneous treatment effects across salinity categories.
    """
    # Extract coefficients
    ate = results.params[treatment_var]
    hte_coef = results.params[f'{treatment_var}_x_salinity']
    
    # Calculate total effects for each salinity category
    salinity_categories = [0, 1, 2]  # Freshwater, Brackish, Saline
    total_effects = {}
    confidence_intervals = {}
    
    for salinity in salinity_categories:
        # Total effect
        total_effect = ate + hte_coef * salinity
        total_effects[salinity] = total_effect
        
        # Confidence interval (using delta method or bootstrap)
        se_ate = results.std_errors[treatment_var]
        se_hte = results.std_errors[f'{treatment_var}_x_salinity']
        cov_ate_hte = results.cov.loc[treatment_var, f'{treatment_var}_x_salinity']
        
        # Variance of total effect: Var(β1 + β2*Z) = Var(β1) + Z²*Var(β2) + 2*Z*Cov(β1,β2)
        se_total = np.sqrt(se_ate**2 + (salinity**2) * se_hte**2 + 2 * salinity * cov_ate_hte)
        
        # 95% CI
        ci_lower = total_effect - 1.96 * se_total
        ci_upper = total_effect + 1.96 * se_total
        confidence_intervals[salinity] = (ci_lower, ci_upper)
    
    # Create visualization
    plot_hte_by_salinity(total_effects, confidence_intervals, treatment_var)
    
    # Statistical test: Is HTE significant?
    hte_pvalue = results.pvalues[f'{treatment_var}_x_salinity']
    print(f"HTE significance (p-value): {hte_pvalue}")
    
    if hte_pvalue < 0.05:
        print("Heterogeneous treatment effect is statistically significant.")
        print("Treatment effects vary significantly across salinity categories.")
    else:
        print("No significant heterogeneity detected. ATE is sufficient.")
    
    return total_effects, confidence_intervals

def plot_hte_by_salinity(total_effects, confidence_intervals, treatment_var):
    """
    Visualize heterogeneous treatment effects with confidence intervals.
    """
    import matplotlib.pyplot as plt
    
    categories = ['Freshwater', 'Brackish', 'Saline']
    effects = [total_effects[i] for i in [0, 1, 2]]
    ci_lower = [confidence_intervals[i][0] for i in [0, 1, 2]]
    ci_upper = [confidence_intervals[i][1] for i in [0, 1, 2]]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    x_pos = np.arange(len(categories))
    
    # Plot effects with error bars
    ax.errorbar(x_pos, effects, yerr=[np.array(effects) - np.array(ci_lower),
                                       np.array(ci_upper) - np.array(effects)],
                fmt='o', capsize=5, capthick=2, markersize=8)
    
    ax.axhline(y=0, color='r', linestyle='--', alpha=0.5)
    ax.set_xlabel('Salinity Category', fontsize=12)
    ax.set_ylabel(f'Treatment Effect of {treatment_var}', fontsize=12)
    ax.set_title('Heterogeneous Treatment Effects by Marsh Salinity Type', fontsize=14)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(categories)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'hte_analysis_{treatment_var}.png', dpi=300)
    plt.show()
```

### 5.3 Statistical Validation Checks

#### Required Statistical Tests

1. **Fixed Effects Necessity Test (Hausman Test)**
   - **Null Hypothesis:** Random Effects model is appropriate
   - **Alternative:** Fixed Effects model is necessary
   - **Action:** If p < 0.05, use Fixed Effects (reject random effects)

2. **Residual Normality Test (Shapiro-Wilk or Jarque-Bera)**
   - **Purpose:** Check if residuals are normally distributed
   - **Action:** If violated, consider robust standard errors or transformation

3. **Heteroskedasticity Test (Breusch-Pagan)**
   - **Purpose:** Check if error variance is constant
   - **Action:** Use clustered standard errors (already implemented in code)

4. **Serial Correlation Test (Wooldridge Test)**
   - **Purpose:** Check for autocorrelation in panel residuals
   - **Action:** If present, use HAC (Newey-West) standard errors

5. **Multicollinearity Check (VIF)**
   - **Purpose:** Ensure interaction terms don't cause severe multicollinearity
   - **Action:** VIF < 10 is acceptable; if higher, consider centering variables

6. **Sensitivity Analysis**
   - **Robustness Checks:** Run model with different specifications (lagged treatments, different time windows)
   - **Placebo Tests:** Test treatment effects on pre-treatment periods (should be null)

### 5.4 Reporting Results

#### Key Outputs to Report

1. **Regression Table:** Coefficients, standard errors, p-values, confidence intervals
2. **HTE Visualization:** Bar/line plots showing treatment effects by salinity category
3. **Diagnostic Plots:** Residual plots, Q-Q plots, leverage plots
4. **Summary Statistics:** Descriptive statistics for all variables
5. **Model Fit Statistics:** R-squared (within, between, overall), F-statistic

#### Interpretation Framework

- **Causal Claims:** Emphasize that Fixed Effects control for unobserved confounders, strengthening causal inference
- **Policy Implications:** Discuss how different marsh types respond differently to climate change
- **Limitations:** Acknowledge assumptions (no time-varying confounders, linearity, etc.)

---

## 6. 📋 Implementation Timeline

### Week 1-2: Phase 1 (Data Acquisition)
- Set up GEE and NOAA API access
- Download and preprocess satellite and climate data
- Create panel data structure

### Week 3-4: Phase 2 (Feature Engineering)
- Implement time-series smoothing algorithms
- Extract phenological metrics for all units
- Create lag and cumulative variables

### Week 5-7: Phase 3 (Modeling)
- Implement Fixed Effects regression
- Run models for each outcome variable (SOS, EOS, LOGS)
- Perform model diagnostics

### Week 8-10: Phase 4 (Analysis & Validation)
- Interpret ATE and HTE coefficients
- Create visualizations
- Perform robustness checks
- Write final report

---

## 7. 📚 Additional Resources

### Key Papers
- Angrist, J. D., & Pischke, J. S. (2009). *Mostly Harmless Econometrics*
- Wooldridge, J. M. (2010). *Econometric Analysis of Cross Section and Panel Data*
- Zhang, X., et al. (2003). "Monitoring vegetation phenology using MODIS"

### Software Documentation
- [linearmodels Documentation](https://bashtage.github.io/linearmodels/)
- [Google Earth Engine Python API](https://developers.google.com/earth-engine/guides/python_install)
- [xarray Documentation](https://docs.xarray.dev/)

---

**End of Project Plan**

