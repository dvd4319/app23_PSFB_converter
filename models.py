from django.db import models

# Create your models here.

class FullBridgePhaseShiftConverter(models.Model):
    name = models.CharField(max_length=100, default="FullBridgePhaseShiftConverter")
    # Input voltage range
    Vs_min = models.FloatField(default= 260)
    Vs_max = models.FloatField(default=420)
    Vs_nom = models.FloatField(default=345)

    # Output voltage range
    Vo_min = models.FloatField(default= 12)
    Vo_max = models.FloatField(default= 16)
    Vo_nom = models.FloatField(default=14)

    # Output current range
    Io_min = models.FloatField(default= 0)
    Io_max = models.FloatField(default= 230)

    # Switching frequency
    f = models.FloatField(default= 200000)

    # Output voltage ripple (relative, e.g. 0.01 = 1%)
    ripple_Vo = models.FloatField(default= 0.01)

    # Maximum output power
    Pout_max = models.FloatField(default=3200)

    ############################################################

    # Date numerice - valori unice
    D_max = models.FloatField(default=0.45)
    D_theo = models.FloatField(default=0.5)

    Lk = models.FloatField(default=0.5e-6)
    Lp = models.FloatField(default=147e-6)

    Ns = models.PositiveIntegerField(default=16)

    R_prim = models.FloatField(default=25e-3)
    R_sec = models.FloatField(default=1e-3)

    Rdson_PR = models.FloatField(default=0.180)
    Rdson_SR = models.FloatField(default=0.002625)

    RLo = models.FloatField(default=2.5e-3)

    N_Lo = models.PositiveIntegerField(default=2)
    C_oss = models.FloatField(default=120e-12)
    C_tr = models.FloatField(default=100e-12)
    delta_Us = models.FloatField(default=100e-3)


    V_cc =  models.FloatField(default=12.0) 
    Qg_PR =  models.FloatField(default=118e-12) 
    Qg_SR =  models.FloatField(default=81e-12)  
    # MOSFET SECUNDAR: AUIRF7669L2
    C_oss_SR =  models.FloatField(default=1040e-12) 
    # Material 3C90 
    Cm_3C90 =  models.FloatField(default=3.2e-3)  
    x_3C90 =  models.FloatField(default=1.46)  
    y_3C90 =  models.FloatField(default=2.75) 
    B_sat_3c90 =  models.FloatField(default=0.38) 
    # Material 3F3 
    Cm_3F3 =  models.FloatField(default=0.25e-3)  
    x_3F3=  models.FloatField(default=1.63)  
    y_3F3=  models.FloatField(default=2.45)  
    # Miez Magnetic E32/6/20 Ferroxcube (inductanta de iesire)
    Ac_ferita =  models.FloatField(default=130) # mm^2, maerial:  
    Vc =  models.FloatField(default=5.3)  # cm^2 (volumul fierului)
    # Miez Magnetic ER51/10/38 (Transformator)
    Ae_ER51 =  models.FloatField(default=351) # mm^2 ER51/10/38 # de fapt este AE = 314 !!!! 
    Vc_ER51 =  models.FloatField(default=25.8)  # cm^3 # ER51/10/38


    def __str__(self):
        return (
            f"Full-Bridge Converter: "
            f"Vs={self.Vs_min}-{self.Vs_nom}-{self.Vs_max} V, "
            f"Vo={self.Vo_min}-{self.Vo_nom}-{self.Vo_max} V, "
            f"Io={self.Io_min}-{self.Io_max} A, "
            f"f={self.f} Hz"
            f"ripple_Vo={self.ripple_Vo}"
            f"Po = {self.Pout_max} W"
        )
    





