import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

D = 1e-5  # Diffusion coefficient (m²/s)

def analyze_channel(v, L, t, label):
    """Analyze channel for given drift velocity and length"""
    
    h_t = (L / (2 * np.sqrt(np.pi * D * t**3))) * np.exp(-(L - v*t)**2 / (4*D*t))
    h_t = np.maximum(h_t, 0)
    h_t = h_t / np.sum(h_t)  # Normalize
    
    mean_arrival = np.sum(t * h_t)
    peak_arrival = t[np.argmax(h_t)]
    t_sq = t**2
    rms_spread = np.sqrt(np.sum(h_t * t_sq) - mean_arrival**2)
    
    # Data rate and BER (simplified)
    data_rate = 1 / rms_spread if rms_spread > 0 else 0
    ber = 0.5 * erfc(np.sqrt(data_rate / 10))  # Noise-dependent BER
    
    return {
        'velocity': v,
        'length': L,
        'label': label,
        'h_t': h_t,
        'mean_arrival': mean_arrival,
        'peak_arrival': peak_arrival,
        'rms_spread': rms_spread,
        'data_rate': data_rate,
        'ber': ber
    }

# ============================================
# EXPERIMENT 1: Sweep Drift Velocity
# ============================================
print("\n" + "="*70)
print("EXPERIMENT 1: OPTIMAL DRIFT VELOCITY")
print("="*70)

t = np.linspace(0.0001, 0.2, 2000)
L = 0.01
velocities = np.linspace(0, 0.15, 15)
results = []

for v in velocities:
    res = analyze_channel(v, L, t, f'v={v:.3f}')
    results.append(res)

# Find optimal
optimal_idx = np.argmax([r['data_rate'] for r in results])
optimal_result = results[optimal_idx]

print(f"\nOptimal Drift Velocity: {optimal_result['velocity']:.4f} m/s")
print(f"Maximum Data Rate: {optimal_result['data_rate']:.2f} a.u.")
print(f"BER at Optimal: {optimal_result['ber']:.2e}")

# ============================================
# EXPERIMENT 2: Vary Channel Length
# ============================================
print("\n" + "="*70)
print("EXPERIMENT 2: CHANNEL LENGTH VARIATION")
print("="*70)

lengths = np.array([0.005, 0.01, 0.02, 0.05, 0.1])  # meters
t = np.linspace(0.0001, 0.5, 2000)
v_optimal = optimal_result['velocity']

length_results = []
for L in lengths:
    res = analyze_channel(v_optimal, L, t, f'L={L*1000:.1f}mm')
    length_results.append(res)

print(f"\nDrift Velocity Fixed at: {v_optimal:.4f} m/s\n")
print(f"{'Channel Length':<20} {'Arrival Time (s)':<20} {'Data Rate (a.u.)':<20} {'BER':<15}")
print("-"*75)
for res in length_results:
    print(f"{res['length']*1000:.1f} mm{'':<14} {res['mean_arrival']:<20.6f} {res['data_rate']:<20.2f} {res['ber']:<15.2e}")

# ============================================
# EXPERIMENT 3: Drift vs Diffusion Comparison
# ============================================
print("\n" + "="*70)
print("EXPERIMENT 3: DRIFT-ASSISTED vs DIFFUSION-ONLY")
print("="*70)

t = np.linspace(0.0001, 0.15, 2000)
L = 0.01

diffusion_only = analyze_channel(v=0, L=L, t=t, label='Diffusion Only')
drift_assisted = analyze_channel(v=v_optimal, L=L, t=t, label='Drift-Assisted')

improvement = ((drift_assisted['data_rate'] / diffusion_only['data_rate']) - 1) * 100
arrival_improve = ((diffusion_only['mean_arrival'] - drift_assisted['mean_arrival']) / diffusion_only['mean_arrival']) * 100
ber_improve = ((diffusion_only['ber'] - drift_assisted['ber']) / diffusion_only['ber']) * 100

print(f"\n{'Metric':<30} {'Diffusion Only':<20} {'Drift-Assisted':<20}")
print("-"*70)
print(f"{'Drift Velocity (m/s)':<30} {diffusion_only['velocity']:<20.4f} {drift_assisted['velocity']:<20.4f}")
print(f"{'Mean Arrival Time (s)':<30} {diffusion_only['mean_arrival']:<20.6f} {drift_assisted['mean_arrival']:<20.6f}")
print(f"{'RMS Delay Spread (s)':<30} {diffusion_only['rms_spread']:<20.6f} {drift_assisted['rms_spread']:<20.6f}")
print(f"{'Data Rate (a.u.)':<30} {diffusion_only['data_rate']:<20.2f} {drift_assisted['data_rate']:<20.2f}")
print(f"{'BER':<30} {diffusion_only['ber']:<20.2e} {drift_assisted['ber']:<20.2e}")
print("="*70)

print(f"\n✓ DATA RATE IMPROVEMENT: {improvement:.1f}%")
print(f"✓ ARRIVAL TIME REDUCTION: {arrival_improve:.1f}%")
print(f"✓ BER REDUCTION: {ber_improve:.1f}%\n")

# ============================================
# ALL PLOTS IN ONE FIGURE
# ============================================

fig = plt.figure(figsize=(16, 20))

# EXPERIMENT 1 PLOTS (top row)
# Plot 1: Data Rate vs Drift Velocity
ax1 = plt.subplot(4, 2, 1)
vels = [r['velocity'] for r in results]
rates = [r['data_rate'] for r in results]
ax1.plot(vels, rates, 'bo-', linewidth=2.5, markersize=8)
ax1.axvline(optimal_result['velocity'], color='r', linestyle='--', linewidth=2, label=f"Optimal: {optimal_result['velocity']:.4f} m/s")
ax1.set_xlabel('Drift Velocity (m/s)', fontsize=11)
ax1.set_ylabel('Data Rate (a.u.)', fontsize=11)
ax1.set_title('EXPERIMENT 1: Data Rate vs Drift Velocity', fontsize=12, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(alpha=0.3)

# Plot 2: BER vs Drift Velocity
ax2 = plt.subplot(4, 2, 2)
bers = [r['ber'] for r in results]
ax2.semilogy(vels, bers, 'ro-', linewidth=2.5, markersize=8)
ax2.axvline(optimal_result['velocity'], color='r', linestyle='--', linewidth=2)
ax2.set_xlabel('Drift Velocity (m/s)', fontsize=11)
ax2.set_ylabel('Bit Error Rate (BER)', fontsize=11)
ax2.set_title('EXPERIMENT 1: BER vs Drift Velocity', fontsize=12, fontweight='bold')
ax2.grid(alpha=0.3, which='both')

# EXPERIMENT 2 PLOTS (middle rows)
# Plot 3: Impulse Responses at Different Lengths
ax3 = plt.subplot(4, 2, 3)
for res in length_results:
    ax3.plot(t, res['h_t'], linewidth=2, label=f"L={res['length']*1000:.1f}mm")
ax3.set_xlabel('Time (s)', fontsize=11)
ax3.set_ylabel('Impulse Response h(t)', fontsize=11)
ax3.set_title('EXPERIMENT 2: Impulse Responses at Different Lengths', fontsize=12, fontweight='bold')
ax3.legend(fontsize=9)
ax3.grid(alpha=0.3)
ax3.set_xlim(0, 0.3)

# Plot 4: Arrival Time vs Channel Length
ax4 = plt.subplot(4, 2, 4)
lens = [r['length']*1000 for r in length_results]
arrivals = [r['mean_arrival'] for r in length_results]
ax4.plot(lens, arrivals, 'go-', linewidth=2.5, markersize=8)
ax4.set_xlabel('Channel Length (mm)', fontsize=11)
ax4.set_ylabel('Mean Arrival Time (s)', fontsize=11)
ax4.set_title('EXPERIMENT 2: Arrival Time vs Channel Length', fontsize=12, fontweight='bold')
ax4.grid(alpha=0.3)

# Plot 5: Data Rate vs Channel Length
ax5 = plt.subplot(4, 2, 5)
rates_length = [r['data_rate'] for r in length_results]
ax5.plot(lens, rates_length, 'mo-', linewidth=2.5, markersize=8)
ax5.set_xlabel('Channel Length (mm)', fontsize=11)
ax5.set_ylabel('Data Rate (a.u.)', fontsize=11)
ax5.set_title('EXPERIMENT 2: Data Rate vs Channel Length', fontsize=12, fontweight='bold')
ax5.grid(alpha=0.3)

# EXPERIMENT 3 PLOTS (bottom rows)
# Plot 6: Impulse Response Comparison
ax6 = plt.subplot(4, 2, 6)
ax6.plot(t, diffusion_only['h_t'], 'b-', linewidth=2.5, label='Diffusion Only')
ax6.plot(t, drift_assisted['h_t'], 'r-', linewidth=2.5, label='Drift-Assisted')
ax6.set_xlabel('Time (s)', fontsize=11)
ax6.set_ylabel('Impulse Response h(t)', fontsize=11)
ax6.set_title('EXPERIMENT 3: Channel Impulse Response Comparison', fontsize=12, fontweight='bold')
ax6.legend(fontsize=10)
ax6.grid(alpha=0.3)

# Plot 7: Channel Memory Comparison
ax7 = plt.subplot(4, 2, 7)
cum_diff = np.cumsum(diffusion_only['h_t'])
cum_drift = np.cumsum(drift_assisted['h_t'])
ax7.plot(t, cum_diff, 'b-', linewidth=2.5, label='Diffusion Only')
ax7.plot(t, cum_drift, 'r-', linewidth=2.5, label='Drift-Assisted')
ax7.set_xlabel('Time (s)', fontsize=11)
ax7.set_ylabel('Cumulative Response', fontsize=11)
ax7.set_title('EXPERIMENT 3: Channel Memory Comparison', fontsize=12, fontweight='bold')
ax7.legend(fontsize=10)
ax7.grid(alpha=0.3)

# Plot 8: Performance Metrics Summary (text box)
ax8 = plt.subplot(4, 2, 8)
ax8.axis('off')

summary_text = f"""
PERFORMANCE SUMMARY

Optimal Drift Velocity: {optimal_result['velocity']:.4f} m/s
Channel Length: {L*1000:.1f} mm

DIFFUSION ONLY:
  • Mean Arrival: {diffusion_only['mean_arrival']:.6f} s
  • Data Rate: {diffusion_only['data_rate']:.2f} a.u.
  • BER: {diffusion_only['ber']:.2e}

DRIFT-ASSISTED:
  • Mean Arrival: {drift_assisted['mean_arrival']:.6f} s
  • Data Rate: {drift_assisted['data_rate']:.2f} a.u.
  • BER: {drift_assisted['ber']:.2e}

IMPROVEMENTS:
  ✓ Data Rate: +{improvement:.1f}%
  ✓ Arrival Time: -{arrival_improve:.1f}%
  ✓ BER Reduction: {ber_improve:.1f}%
"""

ax8.text(0.1, 0.5, summary_text, fontsize=11, family='monospace',
         verticalalignment='center', bbox=dict(boxstyle='round', 
         facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.subplots_adjust(hspace=0.4)
plt.show()