# app23_PSFB_converter

**Django web application for automated analytical modeling of Phase-Shifted Full-Bridge (PSFB) DC-DC converters**

This project implements a complete analytical model for dimensioning power components and calculating efficiency of isolated PSFB converters (commonly used as HV-LV auxiliary modules in electric and hybrid vehicles).

### Main features

- Web-based interface (Django MVT architecture)
- Full analytical calculations based on classical PSFB equations:
  - Transformer turns ratio
  - Effective duty cycle (with parasitic voltage drops: leakage inductance, winding resistance, Rdson, output inductor)
  - Output inductor sizing (ripple constraint)
  - Peak & RMS currents (inductor, primary/secondary circuits)
  - Magnetic flux density & core selection check
  - Detailed power loss breakdown (conduction, switching, core – modified Steinmetz, snubber)
  - Global efficiency estimation
- Persistent parameter storage (Django model)
- Grouped input form with engineering labels and default values
- Results displayed in structured tables + optional Matplotlib plots (waveforms, loss distribution)
- Error handling and validation
- Initially validated against reference PhD thesis results, then applied to original 2600 W automotive specifications (280–450 V input, 11.5–15.5 V output)

### Technology stack

- Python 3 + Django (MVT pattern)
- NumPy (numerical computations, RMS etc.)
- Matplotlib (server-side plots, Agg backend + base64 embedding)
- SQLite (default database – easy to deploy)

### Live demo

The application is currently running on my professional website:  
**[Link către site-ul tău – ex. https://yourdomain.com/psfb-converter]**  
(Feel free to test with your own parameters.)

### How to run locally

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/app23_PSFB_converter.git
   cd app23_PSFB_converter
