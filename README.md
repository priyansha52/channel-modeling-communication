
### Quick Start
```bash
# Basic analysis
python channel.py

# Full experiments (drift sweep, length variation, comparison)
python advanced_analysis.py
```

## Experiments

### Experiment 1: Drift Velocity Optimization
Sweeps drift velocity from 0 to 0.15 m/s to find optimal operating point.
- Identifies maximum data rate
- Computes BER at each velocity
- Plots data rate and error rate curves

### Experiment 2: Channel Length Scaling
Analyzes performance across different channel lengths (5-100 mm).
- Arrival time vs length
- Data rate scalability
- Impulse response variations

### Experiment 3: Baseline Comparison
Direct comparison: Diffusion-only vs Drift-Assisted
- Impulse response overlap
- Channel memory comparison
- Quantified improvement metrics

## Results Summary

| Metric | Diffusion Only | Drift-Assisted | Improvement |
|--------|---|---|---|
| Mean Arrival Time | 0.0914 s | 0.0649 s | **-28.9%** |
| RMS Delay Spread | 0.0305 s | 0.0029 s | **-90.5%** |
| Data Rate (a.u.) | 32.79 | 344.64 | **+950.8%** |
| BER | 2.10e-2 | 1.89e-29 | **Dramatic** |

## Technical Approach
1. **Analytical Solution** - Closed-form impulse response from drift-diffusion PDE
2. **Numerical Analysis** - RMS delay spread as ISI metric
3. **Data Rate Model** - Data rate ∝ 1/RMS_delay_spread
4. **BER Calculation** - Gaussian approximation for error probability
5. **Optimization** - Parameter sweep to find optimal drift velocity

## Key Insights
- **ISI Reduction**: Drift focuses molecular arrivals, reducing tail spread
- **Optimal Trade-off**: Maximum data rate at v = 0.15 m/s (not monotonic)
- **Scalability**: Larger channels show better performance at higher drift velocities
- **Robustness**: BER improves dramatically at optimal velocity

## Usage Examples

### Basic Analysis
```python
from channel import analyze_channel
import numpy as np

D = 1e-5
L = 0.01
t = np.linspace(0.0001, 0.15, 2000)

result = analyze_channel(v=0.1, label='Test Case')
print(f"Data Rate: {result['data_rate']:.2f} a.u.")
```

### Sweep Analysis
```python
import numpy as np
from advanced_analysis import analyze_channel

velocities = np.linspace(0, 0.15, 15)
for v in velocities:
    res = analyze_channel(v, L=0.01, t=t, label=f'v={v:.3f}')
    print(f"v={v:.4f}: Data Rate = {res['data_rate']:.2f}")
```

## Project Structure
