from django.shortcuts import render
import matplotlib
matplotlib.use('Agg')  # backend server
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np
from ..forms import FullBridgePhaseShiftConverterForm



def full_bridge_phase_shift_converter(request):

    form = FullBridgePhaseShiftConverterForm(request.POST or None)
    results = {}   # inițial gol
    error = None

    spec_fields = [form[f] for f in form.spec_fields]
    tr_fields = [form[f] for f in form.tr_fields]
    ind_fields = [form[f] for f in form.ind_fields]
    mos_fields = [form[f] for f in form.mos_fields]
    other_fields = [form[f] for f in form.other_fields]


    context = {
        'form': form,
        'spec_fields': spec_fields,
        'tr_fields': tr_fields,
        'ind_fields': ind_fields,
        'mos_fields': mos_fields,
        'other_fields': other_fields,
    }
    # context = {
    #     'form': form,
    #     'conv': conv,
    # }

    if request.method == "POST" and form.is_valid():
        try:
            # ===================== CITIRE DATE =====================
            V_in_min = float(form.cleaned_data['Vs_min'])      # Vin min
            V_in_max = float(form.cleaned_data['Vs_max'])      # Vin max
            V_in_nom = float(form.cleaned_data['Vs_nom'])      # Vin nom

            V_out_min = float(form.cleaned_data['Vo_min'])      # Vout min
            V_out_max = float(form.cleaned_data['Vo_max'])      # Vout max
            V_out_nom = float(form.cleaned_data['Vo_nom'])      # Vout nom

            Io_min = float(form.cleaned_data['Io_min'])      # Iout min
            Io_max = float(form.cleaned_data['Io_max'])      # Iout max

            F_sw      = float(form.cleaned_data['f'])          # frecvență [Hz]
            ripple_Vo = float(form.cleaned_data['ripple_Vo'])  # ripple relativ (ex. 0.01 pentru 1%)
            Pout_max  = float(form.cleaned_data['Pout_max'])   # Pout max [W]

            D_max       = float(form.cleaned_data['D_max'])
            D_theo      = float(form.cleaned_data['D_theo'])
            Lk          = float(form.cleaned_data['Lk'])
            Lp          = float(form.cleaned_data['Lp'])
            Ns          = int(form.cleaned_data['Ns'])
            R_prim      = float(form.cleaned_data['R_prim'])
            R_sec       = float(form.cleaned_data['R_sec'])
            Rdson_PR    = float(form.cleaned_data['Rdson_PR'])
            Rdson_SR    = float(form.cleaned_data['Rdson_SR'])
            RLo         = float(form.cleaned_data['RLo'])
            N_Lo        = int(form.cleaned_data['N_Lo'])
            C_oss       = float(form.cleaned_data['C_oss'])
            C_oss_SR    = float(form.cleaned_data['C_oss_SR'])
            C_tr        = float(form.cleaned_data['C_tr'])
            delta_Us    = float(form.cleaned_data['delta_Us'])
            V_cc        = float(form.cleaned_data['V_cc'])
            Qg_PR       = float(form.cleaned_data['Qg_PR'])
            Qg_SR       = float(form.cleaned_data['Qg_SR'])
            Cm_3C90     = float(form.cleaned_data['Cm_3C90'])
            x_3C90      = float(form.cleaned_data['x_3C90'])
            y_3C90      = float(form.cleaned_data['y_3C90'])
            B_sat_3c90  = float(form.cleaned_data['B_sat_3c90'])
            Cm_3F3      = float(form.cleaned_data['Cm_3F3'])
            x_3F3       = float(form.cleaned_data['x_3F3'])
            y_3F3       = float(form.cleaned_data['y_3F3'])
            Ac_ferita   = float(form.cleaned_data['Ac_ferita'])
            Vc          = float(form.cleaned_data['Vc'])
            Ae_ER51     = float(form.cleaned_data['Ae_ER51'])
            Vc_ER51     = float(form.cleaned_data['Vc_ER51'])

           ####################################################################
            #### 2.1 Converter final specifications
            ####################################################################

            # # Date numerice - valori unice
            # D_max = 0.45         # teoretic, ales 
            # D_theo = 0.5         # teoretic ()

            # Lk = 0.5e-6          # H (0.5 μH) - inductanța de scăpări estimată a transformatorului 
            # Lp = 147 # uH 

            # Ns = 16  # ex: 16 spire pe secundar


            # R_prim = 25e-3       # Ω
            # R_sec = 1e-3         # Ω

            # Rdson_PR = 0.180     # Ω
            # Rdson_SR = 0.002625  # Ω

            # RLo = 2.5e-3         # Ω

            # # Exemplu: calcul spire primar și secundar
            # # Alegem un număr de spire secundar (Ns) și calculăm Np
            # N_Lo = 2
            # # MOSFET PRIMAR: IPB65R110CFDA 
            # C_oss = 120e-12 # F (pF)
            # C_tr = 100e-12  # F (pF)
            # delta_Us = 100e-3 # V (mV)
            # V_cc = 12; Qg_PR = 118e-12; Qg_SR = 81e-12 
            # # MOSFET SECUNDAR: AUIRF7669L2
            # C_oss_SR = 1040e-12
            # # Material 3C90 
            # Cm_3C90 = 3.2e-3; x_3C90 = 1.46; y_3C90 = 2.75 
            # B_sat_3c90 = 0.38 # T (material 3C90)
            # # Material 3F3 
            # Cm_3F3 = 0.25e-3; x_3F3= 1.63; y_3F3= 2.45; 
            # # Miez Magnetic E32/6/20 Ferroxcube (inductanta de iesire)
            # Ac_ferita = 130 # mm^2, maerial:  
            # Vc = 5.3 # cm^2 (volumul fierului)
            # # Miez Magnetic ER51/10/38 (Transformator)
            # Ae_ER51 = 351 # mm^2 ER51/10/38 # de fapt este AE = 314 !!!! 
            # Vc_ER51 = 25.8 # cm^3 # ER51/10/38
            ##################################################################
            ###### DE AICI INCEP CALCULELE ################################
            ##################################################################
            T = 1/F_sw
            Io = Io_max/2            # A - curentul nominal de ieșire.
            I_out_modul = Io_max/2 # A 
            ####################################################################
            #### 2.2 Power transformer turns ratio calculation
            ####################################################################

            # Calculul raportului maxim al spirelor
            N_ratio_max = (V_in_min / V_out_max) * D_max
            # Alegerea numărului întreg cel mai apropiat mai mic
            N_ratio_int = int(N_ratio_max)
            N_ratio = N_ratio_int
            Np = Ns * N_ratio_int

            #######################################################################
            #### 2.3 Deduction of the ideal and effective duty-cycle
            ########################################################################
            # Calcul raport de conducție ideal ### Duty Cycle = raport de conductie 
            D_ideal = (V_out_nom / V_in_nom) * N_ratio

            ##############################################################################
            ########### (1) Căderea de tensiune pe inductanța de scăpări
            ##############################################################################

            # Calcul cadere de tensiune pe inductanta de scapari
            delta_V_Lk = (Lk * Io * F_sw * Ns) / Np # delta_V_Lk = 1.642 V 

            ##############################################################################
            ########### (2) Căderea de tensiune datorată rezistenței înfășurărilor transformatorului
            ##############################################################################

            # Calcul cadere de tensiune pe rezistenta infasurarii
            delta_V_TR = Io * (R_prim * (Ns/Np) + R_sec * (Np/Ns)) # delta_V_TR = 1.215 

            ##############################################################################
            ########### (3) Căderea de tensiune pe elementele semiconductoare de comutație
            ##############################################################################

            # Calcul cadere de tensiune pe elementele semiconductoare
            delta_V_Rdson = Io * (2*Rdson_PR * (Ns/Np) + Rdson_SR * (Np/Ns)) # delta_V_Rdson = 8.03 V 

            ##############################################################################
            ########### (4) Căderea de tensiune pe inductorul de ieșire
            #############################################################################

            # Calcul cadere de tensiune pe inductorul de iesire
            delta_V_Lo = (Io * RLo)/2 # delta_V_Lo = 0.143 V 

            ##############################################################################
            ########### (5) Raport de conducție efectiv (conditii nominale si maxime)
            ##############################################################################

            # Calcul raport de conductie efectiv: D_eff = 0.296; D_eff_max = 0.45
            D_eff = ((V_out_nom+delta_V_Lo)/(V_in_nom - delta_V_Lk -delta_V_TR - delta_V_Rdson))*(Np/Ns) 
            D_eff_max = ((V_out_max+delta_V_Lo)/(V_in_min - delta_V_Lk -delta_V_TR - delta_V_Rdson))*(Np/Ns)

            ##############################################################################
            ### [[2.4]] Dimensioning of the output inductor
            ##############################################################################

            ##############################################################################
            ########### 2.4.1 Output inductor value calculation #########################
            ##############################################################################
            Io_min = (18/100)*Io # I0_min este 18 % din curentul nominal Io (empiric ales intre 10% si 30% din Io )
            delta_I_Lo = 2*Io_min # A # delta_I_Lo  = 40 A
            Lo = ((V_in_nom* (Ns/Np)*D_ideal*(1-D_ideal))/(delta_I_Lo*F_sw))*1e6 # Lo = 1.25 uH 

            ##############################################################################
            ########### 2.4.2 Calculation of the peak and RMS inductor current
            ##############################################################################

            I_Lo_max = I_out_modul/2 + delta_I_Lo/2 # I_Lo_max = 77.5 A 
            I_Lo_min = I_out_modul/2 - delta_I_Lo/2 # I_Lo_min = 37.5 A 

            I_Lo_RMS = np.sqrt((I_Lo_min**2 + I_Lo_max**2 + I_Lo_max*I_Lo_min)/3) # I_Lo_RMS = 58.64 A 

            ##############################################################################
            ########### 2.4.3 Selection of magnetic core and calculation of maximum flux density
            ##############################################################################
            Ac_min = (Lo * I_Lo_max / (N_Lo * B_sat_3c90)) # Ac_min = 127.46 mm^2 
            print(f"Ac_min: {Ac_min:3f} mm^2")

            B_max = (Lo * I_Lo_max)/(N_Lo * Ac_ferita) # B_max = 0.37 T 
            print(f"B_max: {B_max:3f} T")

            ##############################################################################
            ### [[2.5]] Dimensioning of the power switches from the secondary circuit (MOSFET)
            ##############################################################################
            ### intreruptor static = mosfet 
            ##############################################################################
            ########### 2.5.1 Calculation of maximum and RMS currents in the secondary circuit
            ##############################################################################
            # Durata conductiei [0, DT]
            delta_i_L10 = (((V_in_nom*(Ns/Np)-V_out_nom)/Lo)*(D_ideal/F_sw))*1e6 # delta_i_L10 = 40A
            delta_i_L20 = -((V_out_nom/Lo)*(D_ideal/F_sw))*1e6 # delta_i_L20 =  - 15.9 A 
            delta_i_SR0 = delta_i_L10 + delta_i_L20 # delta_i_SR0 = 24.1 A 
            I_SR_min0 = Io - delta_i_SR0/2 # I_SR_min0 = 102.95 A 
            I_SR_max0 = Io + delta_i_SR0/2 # I_SR_max0 = 127.05 A 

            I_SR_RMS_ON = np.sqrt((I_SR_min0**2 + I_SR_max0**2 + I_SR_max0*I_SR_min0)/3) # I_SR_RMS_ON  = 115.2 A 

            #############################################################
            # Pe durata conducției libere [0, (0.5-D)T],
            ###############################################################
            delta_i_L11 = (V_out_nom/(2*Lo))*((0.5-D_ideal)/F_sw)*1e6 # delta_i_L11 = 6.05 A
            delta_i_L21 = (V_out_nom/(2*Lo))*((0.5-D_ideal)/F_sw)*1e6 # delta_i_L21 = 6.05 A 
            delta_i_SR1 = delta_i_L11 + delta_i_L21 # delta_i_SR1 = 12.1 A 
            I_SR_min1 = Io - delta_i_SR1/2 # I_SR_min1 = 108.95 A 
            I_SR_max1 = Io + delta_i_SR1/2 # I_SR_max1 = nu exista in lucrare 
            # I_SR_max1 = 127.83 

            I_SR_RMS_FW = np.sqrt((I_SR_min1**2 + I_SR_max1**2 + I_SR_max1*I_SR_min1)/3) # I_SR_RMS_FW = 118.11 A 
            #############
            I_SR_RMS  = np.sqrt(D_ideal*I_SR_RMS_ON**2 + (0.5-D_ideal)*I_SR_RMS_FW**2) # I_SR_RMS = 82.69 A 
            print(f"I_SR_RMS: {I_SR_RMS:3f} A")
            ##############################################################################
            ########### 2.5.2 Selection of the power switch for synchronous rectifier
            ##############################################################################
            ### aleger de mosfet. s-a ales AUIRF7669L2 ---- (4.4mΩ @ Tj = 100°C).
            ##############################################################################
            ### [[2.6]]  Dimensioning of power switches for the primary circuit
            ################################################################################

            ##############################################################################
            ########### 2.6.1 Calculation of currents value through power switches from the primary circuit
            ##############################################################################

            Im = (V_in_nom/Lp)*(D_ideal/F_sw) # Im = 3.33 A (corect)
            I_p_min = I_Lo_min*(Ns/Np)-Im/2 # I_p_min  = 5.23 A (greseal in teza)
            # I_p_min = 5.23
            I_p_max = I_Lo_max*(Ns/Np)+Im/2 # I_p_max = 12.73 A (corect)
            I_p_rms_on = np.sqrt((I_p_min**2 + I_p_max**2 + I_p_min*I_p_max)/3)
            ## ------------------------------------------------------------
            Re = (2*Rdson_PR+R_prim+(R_sec+2*Rdson_SR)*(Np/Ns)**2)*1e3
            I_p_min_2 = I_p_max*np.exp(-(Re/Lk*(0.5-D_ideal)*T))+Im/2
            # I_p_min_2 = 4.52
            I_p_rms_FW = np.sqrt((I_p_min_2**2 + I_p_max**2 + I_p_min_2*I_p_max)/3)
            I_PR_RMS = np.sqrt(D_ideal*I_p_rms_on**2 + (0.5-D_ideal)*I_p_rms_FW**2)
            I_p_RMS = np.sqrt(I_PR_RMS**2+I_PR_RMS**2)

            ##############################################################################
            ### [[2.6]].2 Selection of the power switch for the primary circuit
            ##############################################################################
            '''
            Pe baza rezultatelor obținute din relațiilor (2.52) și (2.60), întreruptoarele statice de
            putere din circuitul primar de comutație vor trebui să fie capabile să suporte o tensiune la borne
            de minim 500V (420V + tensiuni tranzitorii), să asigure un curent de vârf și efectiv de minim:
            Imax_ întreruptor  = 12.73A (2.62)
            Irms _ întreruptor = 6.45A (2.63)
            Se va selecta un dispozitiv de tip MOSFET optimizat pentru acest tip de aplicație. Un
            astfel de dispozitiv este IPB65R110CFDA în tehnologie CoolMOS de la producătorul Infineon
            Technologies [12]. Principalele date de catalog sunt prezentate în Fig. 2.9.
            Conform specificațiilor, acest întreruptor static de putere are o tensiune nominală de
            650V, rezistența drenă-sursă de 180mΩ și un curent nominal de 19.7A la o temperatură de
            100°C a capsulei, ceea ce este mai mult decât suficient pentru această aplicație.
            '''
            ##############################################################################
            ### [[2.7]] Calculation of available energy in leakage inductance
            ##############################################################################

            E_cap = ((1/2)*(2*C_oss+C_tr)*V_in_max**2)*1e6
            E_k = (1/2)*Lk*I_p_min_2**2*1e7

            ##############################################################################
            ### [[2.8]] Output capacitor calculation
            ##############################################################################

            delta_I_Co = delta_i_L10 + delta_i_L20
            Co_min = (delta_I_Co / (8*delta_Us*F_sw*2))*1e6

            ##############################################################################
            ### [[2.9]] Calculation of converter losses
            ##############################################################################
            ##############################################################################
            ########### 2.9.1 Losses in the output inductors
            ##############################################################################
            Cm = Cm_3C90; x = x_3C90; y = y_3C90; 
            P_DCR_Lo = I_Lo_RMS**2*RLo
            delta_B_ac = ((V_in_nom*(Ns/Np)-V_out_nom)/(N_Lo*Ac_ferita))*(D_ideal/F_sw)*1e6
            f_eq = (2/(np.pi**2)*F_sw)*(1/(D_ideal*(1-D_ideal)))*1e-3
            P_MSE = ((Cm*((f_eq*1e3)**x)*((delta_B_ac/2)**y)))
            P_core_Lo = P_MSE*Vc*1e-3
            P_Lo = P_DCR_Lo + P_core_Lo

            ##############################################################################
            ########### 2.9.2 Power losses on power switch from the primary circuit
            ##############################################################################
            P_sw_PR = (1/8)*(2*C_oss + C_tr)*V_in_nom**2*F_sw
            P_cond_PR = (I_PR_RMS**2)*Rdson_PR
            P_PR = P_cond_PR + P_sw_PR

            ##############################################################################
            ########### 2.9.3 Power dissipated on power switches from the secondary circuit
            ##############################################################################
            P_cond_SR = (I_SR_RMS)**2*Rdson_SR
            P_sw_SR = (1/2)*C_oss_SR*(V_in_nom*(Ns/Np))**2*F_sw
            P_SR = P_cond_SR+2*P_sw_SR

            ##############################################################################
            ########### 2.9.4 Losses in the power transformer
            ##############################################################################
            Ae = Ae_ER51; Vc1 = Vc_ER51 
            Cm1 = Cm_3F3; x1= x_3F3; y1 = y_3F3 
            Pt_res_prim = I_p_RMS**2*R_prim
            Pt_res_sec = I_Lo_RMS**2*R_sec
            B_hat = (V_in_nom*D_ideal)/(2*N_ratio_int*Ae*F_sw)*1e6
            P_MSE = Cm1*((f_eq*1e3)**x1)*(B_hat**y1)
            Pt_core = P_MSE*Vc1*1e-3
            Pt = Pt_res_prim + Pt_res_sec + Pt_core 

            ##############################################################################
            ########### 2.9.5 Power consumed by control circuits
            ##############################################################################
            P_DRV = V_cc*(4*Qg_PR + 4*Qg_SR)*F_sw*1e3
            print(f"P_DRV : {P_DRV:3f} W") # P_DRV = 1.81 W

            #############################################################################
            ########### 2.9.6 Power dissipated due to voltage stress limiting circuits
            ##############################################################################

            Cs = 470e-12 
            P_snubber = 2*Cs*(V_in_nom*(Ns/Np))**2*F_sw
            print(f"P_snubber : {P_snubber:3f} W") # P_DRV = 0.46 W
            ##############################################################################
            ### [[2.10]] Loss balance and efficiency calculation
            ##############################################################################

            Pd = 2*P_Lo + 4*P_PR + 2*P_SR + Pt + P_DRV + P_snubber # Pd = 108.6W 
            print(f"Pd: {Pd:3f} W") # Pd = 108.6W W

            # ===================== REZULTATE =====================
            # ... după toate calculele tale existente ...

            # Colectăm TOATE valorile printate într-un dicționar
            results = {}

            # 2.2 Power transformer turns ratio calculation
            results['N_ratio_max']       = round(N_ratio_max, 4)
            results['N_ratio_int']       = N_ratio_int
            results['N_ratio']           = N_ratio
            results['Np']                = Np
            results['Ns']                = Ns   # deja ai Ns din form, dar îl punem și aici pentru claritate

            # 2.3 Deduction of the ideal and effective duty-cycle
            results['D_ideal']           = round(D_ideal, 4)
            results['delta_V_Lk']        = round(delta_V_Lk, 4)
            results['delta_V_TR']        = round(delta_V_TR, 3)
            results['delta_V_Rdson']     = round(delta_V_Rdson, 3)
            results['delta_V_Lo']        = round(delta_V_Lo, 3)

            if D_eff_max > D_theo:
                results['D_eff_max_comment'] = f"> {D_theo} (prea mare față de D teoretic)"
            elif D_eff_max <= 0:
                results['D_eff_max_comment'] = "(negativ - imposibil)"
            else:
                results['D_eff_max_comment'] = f"< {D_theo} (OK)"

            results['D_eff_max']         = round(D_eff_max, 3)
            results['D_eff']             = round(D_eff, 3)

            # 2.4.1 Output inductor value calculation
            results['Io_min_calc']       = round(Io_min, 2)          # redenumit ca să nu se confunde cu input-ul
            results['delta_I_Lo']        = round(delta_I_Lo, 3)
            results['Lo_uH']             = round(Lo, 6)              # mai multe zecimale, valorea e mică

            # 2.4.2 Peak and RMS inductor current
            results['I_Lo_max']          = round(I_Lo_max, 2)
            results['I_Lo_min']          = round(I_Lo_min, 2)
            results['I_Lo_RMS']          = round(I_Lo_RMS, 3)

            # 2.4.3 Magnetic core
            results['Ac_min_mm2']        = round(Ac_min, 2)
            results['Ac_ferita_mm2']     = Ac_ferita
            results['B_max_T']           = round(B_max, 3)

            # 2.5.1 Secondary circuit currents (pe durata DT)
            results['delta_i_L10']       = round(delta_i_L10, 3)
            results['delta_i_L20']       = round(delta_i_L20, 3)
            results['delta_i_SR0']       = round(delta_i_SR0, 3)
            results['I_SR_min0']         = round(I_SR_min0, 3)
            results['I_SR_max0']         = round(I_SR_max0, 3)
            results['I_SR_RMS_ON']       = round(I_SR_RMS_ON, 3)

            # 2.5.1 Secondary (pe durata (0.5-D)T)
            results['delta_i_L11']       = round(delta_i_L11, 3)
            results['delta_i_L21']       = round(delta_i_L21, 3)
            results['delta_i_SR1']       = round(delta_i_SR1, 3)
            results['I_SR_min1']         = round(I_SR_min1, 3)
            results['I_SR_max1']         = round(I_SR_max1, 3)
            results['I_SR_RMS_FW']       = round(I_SR_RMS_FW, 3)

            results['I_SR_RMS']          = round(I_SR_RMS, 3)

            # 2.6.1 Primary circuit currents
            results['Im']                = round(Im, 3)
            results['I_p_min']           = round(I_p_min, 3)
            results['I_p_max']           = round(I_p_max, 3)
            results['I_p_rms_on']        = round(I_p_rms_on, 3)
            results['Re_mOhm']           = round(Re, 3)
            results['I_p_min_2']         = round(I_p_min_2, 3)
            results['I_p_rms_FW']        = round(I_p_rms_FW, 3)
            results['I_PR_RMS']          = round(I_PR_RMS, 3)
            results['I_p_RMS']           = round(I_p_RMS, 3)

            # 2.7 Energy in leakage inductance
            results['E_cap_uJ']          = round(E_cap, 3)           # era uC → probabil eroare, presupun μJ
            results['E_k_uJ']            = round(E_k, 3)

            # 2.8 Output capacitor
            results['delta_I_Co']        = round(delta_I_Co, 3)
            results['Co_min_uF']         = round(Co_min, 3)

            # 2.9.1 Losses output inductor
            results['P_DCR_Lo']          = round(P_DCR_Lo, 3)
            results['delta_B_ac_T']      = round(delta_B_ac, 3)
            results['f_eq_kHz']          = round(f_eq, 3)
            results['P_MSE_mW_cm3']      = round(P_MSE, 3)
            results['P_core_Lo']         = round(P_core_Lo, 3)
            results['P_Lo']              = round(P_Lo, 3)

            # 2.9.2 Primary switches losses
            results['P_sw_PR']           = round(P_sw_PR, 3)
            results['P_cond_PR']         = round(P_cond_PR, 3)
            results['P_PR']              = round(P_PR, 3)

            # 2.9.3 Secondary switches losses
            results['P_sw_SR']           = round(P_sw_SR, 3)
            results['P_cond_SR']         = round(P_cond_SR, 3)
            results['P_SR']              = round(P_SR, 3)

            # 2.9.4 Transformer losses
            results['Pt_res_prim']       = round(Pt_res_prim, 3)
            results['Pt_res_sec']        = round(Pt_res_sec, 3)
            results['B_hat_T']           = round(B_hat, 3)
            results['P_MSE_tr_mW']       = round(P_MSE, 3)           # atenție: variabila se cheamă la fel ca mai sus
            results['Pt_core']           = round(Pt_core, 3)
            results['Pt']                = round(Pt, 3)

            # 2.9.5 Control circuits
            results['P_DRV']             = round(P_DRV, 3)

            # 2.9.6 Snubber
            results['P_snubber']         = round(P_snubber, 3)

            # 2.10 Total losses & efficiency
            results['Pd_total']          = round(Pd, 2)
            results['eta_percent']       = round(100 * (Pout_max / (Pout_max + Pd)), 2) if (Pout_max + Pd) > 0 else 0.0

            # Acum bagi în context
            context.update({
                'form': form,
                'results': results,
            })

            if 'error' not in context:
                context['error'] = None
        except Exception as e:
            context['error'] = str(e)

    return render(request, './app23_PSFB_converter/power95_full_bridge_phase_shift.html', context)

