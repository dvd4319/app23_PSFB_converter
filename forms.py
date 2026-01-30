from django import forms
from .models import FullBridgePhaseShiftConverter


class FullBridgePhaseShiftConverterForm(forms.ModelForm):
    specifications_fields = [          # 11 – specificațiile de design de bază (input/output)
        'Vs_min', 'Vs_nom', 'Vs_max',
        'Vo_min', 'Vo_nom', 'Vo_max',
        'Io_min', 'Io_max',
        'f',
        'ripple_Vo',
        'Pout_max'
    ]

    spec_transformer = [               # 12 – tot ce ține de transformator
        'Lk', 'Lp', 'Ns',
        'R_prim', 'R_sec',
        'Cm_3F3', 'x_3F3', 'y_3F3',
        'Ae_ER51', 'Vc_ER51',
        'C_tr', 'delta_Us'             # C_tr și delta_Us sunt legate de comutație / transformator
    ]

    spec_inductor = [                  # 6 – inductor de ieșire
        'N_Lo', 'RLo',
        'Cm_3C90', 'x_3C90', 'y_3C90', 'B_sat_3c90',
        'Ac_ferita', 'Vc'
    ]

    spec_mosfets = [                   # 7 – MOSFET-uri primar + secundar
        'Rdson_PR', 'Rdson_SR',
        'Qg_PR', 'Qg_SR',
        'C_oss', 'C_oss_SR',
        'C_tr'                             # poate rămâne aici sau merge la transformer
    ]

    spec_other = [                     # 4 – restul, diverse / auxiliare
        'D_max', 'D_theo',
        'V_cc'
    ]
    class Meta:
        model = FullBridgePhaseShiftConverter
        fields = [
            'Vs_min', 'Vs_nom', 'Vs_max',
            'Vo_min', 'Vo_nom', 'Vo_max',
            'Io_min', 'Io_max',
            'f',
            'ripple_Vo',
            'Pout_max',
            'D_max', 'D_theo', 
            'Lk', 'Lp', 'Ns',
            'R_prim', 'R_sec', 
            'Rdson_PR', 'Rdson_SR', 'RLo', 
            'N_Lo', 'C_oss', 'C_tr', 'delta_Us',
            'V_cc', 'Qg_PR', 'Qg_SR', 'C_oss_SR',
            'Cm_3C90', 'x_3C90', 'y_3C90', 'B_sat_3c90',
            'Cm_3F3', 'x_3F3', 'y_3F3',
            'Ac_ferita', 'Vc', 'Ae_ER51', 'Vc_ER51'
        ]

        widgets = {
            'Vs_min': forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}),
            'Vs_max': forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}),
            'Vs_nom': forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}),

            'Vo_min': forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}),
            'Vo_max': forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}),
            'Vo_nom': forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}),

            'Io_min': forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}),
            'Io_max': forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}),

            'f': forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}),

            'ripple_Vo': forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}),

            'Pout_max': forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}),

            'D_max': forms.NumberInput(attrs={'step': 0.01}),
            'D_theo': forms.NumberInput(attrs={'step': 0.01}),
            'Lk': forms.NumberInput(attrs={'step': 1e-9}),
            'Lp': forms.NumberInput(attrs={'step': 1e-6}),
            'Ns': forms.NumberInput(attrs={'step': 1}),
            'R_prim': forms.NumberInput(attrs={'step': 1e-3}),
            'R_sec': forms.NumberInput(attrs={'step': 1e-3}),
            'Rdson_PR': forms.NumberInput(attrs={'step': 1e-3}),
            'Rdson_SR': forms.NumberInput(attrs={'step': 1e-6}),
            'RLo': forms.NumberInput(attrs={'step': 1e-3}),
            'N_Lo': forms.NumberInput(attrs={'step': 1}),
            'C_oss': forms.NumberInput(attrs={'step': 1e-12}),
            'C_oss_SR': forms.NumberInput(attrs={'step': 1e-12}),
            'C_tr': forms.NumberInput(attrs={'step': 1e-12}),
            'delta_Us': forms.NumberInput(attrs={'step': 1e-3}),
            'V_cc': forms.NumberInput(attrs={'step': 0.1}),
            'Qg_PR': forms.NumberInput(attrs={'step': 1e-12}),
            'Qg_SR': forms.NumberInput(attrs={'step': 1e-12}),
            'Cm_3C90': forms.NumberInput(attrs={'step': 1e-3}),
            'x_3C90': forms.NumberInput(attrs={'step': 0.01}),
            'y_3C90': forms.NumberInput(attrs={'step': 0.01}),
            'B_sat_3c90': forms.NumberInput(attrs={'step': 0.01}),
            'Cm_3F3': forms.NumberInput(attrs={'step': 1e-4}),
            'x_3F3': forms.NumberInput(attrs={'step': 0.01}),
            'y_3F3': forms.NumberInput(attrs={'step': 0.01}),
            'Ac_ferita': forms.NumberInput(attrs={'step': 1}),
            'Vc': forms.NumberInput(attrs={'step': 0.1}),
            'Ae_ER51': forms.NumberInput(attrs={'step': 1}),
            'Vc_ER51': forms.NumberInput(attrs={'step': 0.1}),

        }

        labels = {
            'Vs_min': '1. Input voltage  Vₛ(min) (V)',
            'Vs_max': '2. Input voltage  Vₛ(max) (V)',
            'Vs_nom': '3. Input voltage  Vₛ(nom) (V)',

            'Vo_min': '4. Output voltage  Vₒ(min) (V)',
            'Vo_max': '5. Output voltage  Vₒ(max) (V)',
            'Vo_nom': '6. Output voltage  Vₒ(nom) (V)',

            'Io_min': '7. Output current  Iₒ(min) (A)',
            'Io_max': '8. Output current  Iₒ(max) (A)',

            'f': '9. Switching frequency f (Hz)',

            'ripple_Vo': '10. ΔVₒ (fraction, e.g. 0.01)',

            'Pout_max': '11. Output power Pₒ(max) (W)',

            'D_max': 'p01. Max. duty cycle',
            'D_theo': 'p02. Theo. duty cycle',
            'Lk': 'p03. Leakage Lk [H]',
            'Lp': 'p04. Primary Lp [H]',
            'Ns': 'p05. Secondary turns Ns',
            'R_prim': 'p06. Primary res. R_prim [Ω]',
            'R_sec': 'p07. Secondary res. R_sec  [Ω]',
            'Rdson_PR': 'p08. Prim. MOSFET Rdson [Ω]',
            'Rdson_SR': 'p09. Sec. MOSFET Rdson [Ω]',
            'RLo': 'p10. Output inductor res. [Ω]',
            'N_Lo': 'p11. No. of Lo turns',
            'C_oss': 'p12. Prim. MOSFET C_oss[F]',
            'C_oss_SR': 'p13. Sec. MOSFET C_oss [F]',
            'C_tr': 'p14. Tr. parasitic cap. C_tr [F]',
            'delta_Us': 'p15. Output voltage ripple [V]',
            'V_cc': 'p16. Gate drive voltage [V]',
            'Qg_PR': 'p17. Primary gate charge [C]',
            'Qg_SR': 'p18. Secondary gate charge [C]',
            'Cm_3C90': 'p19. Core mat. ct. 3C90',
            'x_3C90': 'p20. Exponent x 3C90 for Lo',
            'y_3C90': 'p21. Exponent y 3C90 for Lo',
            'B_sat_3c90': 'p22. 3C90 - Lo - B_sat [T]',
            'Cm_3F3': 'p23. Core mat. ct. 3C96 for Tr.',
            'x_3F3': 'p24.  Exponent x 3C96 for Tr.',
            'y_3F3': 'p25. Exponent y 3C96 for Tr.',
            'Ac_ferita': 'p26. Inductor core area [mm²]',
            'Vc': 'p27. Inductor core vol. [cm³]',
            'Ae_ER51': 'p28. Tr. core area [mm²]',
            'Vc_ER51': 'p29. Tr. core volume [cm³]',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get('instance')

        # Atribute separate pentru fiecare grup – le poți folosi în template
        self.spec_fields         = self.specifications_fields
        self.tr_fields           = self.spec_transformer
        self.ind_fields          = self.spec_inductor
        self.mos_fields          = self.spec_mosfets
        self.other_fields        = self.spec_other

        # Dacă vrei și lista cu tot ce nu e în specificații (ca înainte)
        self.parameter_fields = [
            f for f in self.fields if f not in self.specifications_fields
        ]

        # Valori default DOAR la creare nouă
        if not instance:
            # specifications_fields
            spec_defaults = {
                'Vs_min': 280, 'Vs_nom': 365, 'Vs_max': 450,
                'Vo_min': 11.5, 'Vo_nom': 13.5, 'Vo_max': 15.5,
                'Io_min': 0, 'Io_max': 193,
                'f': 200_000,
                'ripple_Vo': 0.01,
                'Pout_max': 2600
            }
            for field in self.specifications_fields:
                if field in self.fields:
                    self.fields[field].initial = spec_defaults.get(field)

            # spec_tr
            for f, v in [
                ('Lk', 0.5e-6), ('Lp', 147e-6), ('Ns', 16),
                ('R_prim', 68e-3), ('R_sec', 1.516e-3),
                ('Cm_3F3', 1.59e-3), ('x_3F3', 1.48), ('y_3F3', 2.93),
                ('Ae_ER51', 194), ('Vc_ER51', 8.48),
                ('C_tr', 100e-12), ('delta_Us', 0.1)
            ]:
                self.fields[f].initial = v

            # spec_inductor
            for f, v in [
                ('N_Lo', 2), ('RLo', 2.5e-3),
                ('Cm_3C90', 3.2e-3), ('x_3C90', 1.46), ('y_3C90', 2.75),
                ('B_sat_3c90', 0.38),
                ('Ac_ferita', 130), ('Vc', 5.3)
            ]:
                self.fields[f].initial = v

            # spec_mosfets
            for f, v in [
                ('Rdson_PR', 0.180), ('Rdson_SR', 0.002625),
                ('Qg_PR', 118e-12), ('Qg_SR', 81e-12),
                ('C_oss', 120e-12), ('C_oss_SR', 1040e-12)
            ]:
                self.fields[f].initial = v

            # spec_other
            for f, v in [
                ('D_max', 0.45), ('D_theo', 0.5),
                ('V_cc', 12.0)
            ]:
                self.fields[f].initial = v



    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.parameter_fields = [f for f in self.fields if f not in self.specifications_fields]
    #     # Default values
    #     self.fields['Vs_min'].initial = 250
    #     self.fields['Vs_max'].initial = 450
    #     self.fields['Vs_nom'].initial = 350

    #     self.fields['Vo_min'].initial = 12
    #     self.fields['Vo_max'].initial = 16
    #     self.fields['Vo_nom'].initial = 14

    #     self.fields['Io_min'].initial = 0
    #     self.fields['Io_max'].initial = 230 

    #     self.fields['f'].initial = 200_000  # 100 kHz
    #     self.fields['ripple_Vo'].initial = 0.01  # 1%
    #     self.fields['Pout_max'].initial = 3200  # W

    #     # Set default (initial) values
    #     self.fields['D_max'].initial = 0.45
    #     self.fields['D_theo'].initial = 0.5

    #     self.fields['Lk'].initial = 0.5e-6
    #     self.fields['Lp'].initial = 147e-6
    #     self.fields['Ns'].initial = 16

    #     self.fields['R_prim'].initial = 25e-3
    #     self.fields['R_sec'].initial = 1e-3
    #     self.fields['Rdson_PR'].initial = 0.180
    #     self.fields['Rdson_SR'].initial = 0.002625
    #     self.fields['RLo'].initial = 2.5e-3

    #     self.fields['N_Lo'].initial = 2
    #     self.fields['C_oss'].initial = 120e-12
    #     self.fields['C_tr'].initial = 100e-12
    #     self.fields['delta_Us'].initial = 0.1

    #     self.fields['V_cc'].initial = 12.0
    #     self.fields['Qg_PR'].initial = 118e-12
    #     self.fields['Qg_SR'].initial = 81e-12
    #     self.fields['C_oss_SR'].initial = 1040e-12

    #     self.fields['Cm_3C90'].initial = 3.2e-3
    #     self.fields['x_3C90'].initial = 1.46
    #     self.fields['y_3C90'].initial = 2.75
    #     self.fields['B_sat_3c90'].initial = 0.38

    #     # self.fields['Cm_3F3'].initial = 0.25e-3 # pentru 3F3
    #     # self.fields['x_3F3'].initial = 1.63  # pentru 3F3
    #     # self.fields['y_3F3'].initial = 2.45  # pentru 3F3

    #     self.fields['Cm_3F3'].initial = 4.2e-3   # pentru 3C96
    #     self.fields['x_3F3'].initial = 1.50     # pentru 3C96
    #     self.fields['y_3F3'].initial = 2.65     # pentru 3C96

    #     self.fields['Ac_ferita'].initial = 130
    #     self.fields['Vc'].initial = 5.3
    #     # self.fields['Ae_ER51'].initial = 351
    #     # self.fields['Vc_ER51'].initial = 25.8
    #     self.fields['Ae_ER51'].initial = 194
    #     self.fields['Vc_ER51'].initial = 9.0
        


