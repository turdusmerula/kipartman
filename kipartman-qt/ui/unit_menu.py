from PyQt6.QtCore import pyqtSignal, QModelIndex
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction

base_units = [
    (["A", "ampere", "amp"]),
    (["C", "coulomb"], "ampere*second"),
    (["°C", "celsius", "degC", "degreeC", "degree_Celsius"], "kelvin; offset: 273.15"),
    (["F", "farad"], "coulomb/volt"),
    (["g", "gram"]),
    (["H", "henry"], "weber/ampere"),
    (["Hz", "hertz"], "1/second"),
    (["J", "joule"], "newton*meter"),
    (["L", "liter", "l", "litre"], "decimeter**3"), 
    (["N", "newton"], "kilogram*meter/second**2"),
    (["Ω", "ohm"], "volt/ampere"),
    (["S", "siemens", "mho"], "ampere/volt"),
    (["V", "volt"], "joule/coulomb"),
    (["W", "watt"], "joule/second"),
    (["Wb", "weber"], "volt*second"),
    (["Wh", "watt_hour", "watthour"], "watt*hour"),
    "",
    ("bit"),
    (["B", "byte", "octet"], "8*bit"),
]

constants = [
    (["π", "pi"], "3.1415926535897932384626433832795028841971693993751"),
    ("tansec", "4.8481368111333441675396429478852851658848753880815e-6"),
    ("ln10", "2.3025850929940456840179914546843642076011014886288"),
    ("wien_x", "4.9651142317442763036987591313228939440555849867973"),
    ("wien_u", "2.8214393721220788934031913302944851953458817440731"),
    ("eulers_number", "2.71828182845904523536028747135266249775724709369995"),
    (["c", "speed_of_light", "c_0"], "299792458 m/s"),
    (["h", "planck_constant"], "6.62607015e-34*J*s"),
    (["elementary_charge", "e"], "1.602176634e-19*C"),
    ("avogadro_number", "6.02214076e23"),
    (["boltzmann_constant", "k", "k_B"], "1.380649e-23*J*K^-1"),
    (["standard_gravity", "g_0", "g0", "g_n", "gravity"], "9.80665*m/s^2"),
    (["standard_atmosphere", "atm", "atmosphere"], "1.01325e5*Pa"),
    (["conventional_josephson_constant", "K_J90"], "4.835979e14*Hz/V"),
    (["conventional_von_klitzing_constant", "R_K90"], "2.5812807e4*ohm"),
    (["zeta", "ζ"], "c/(cm/s)"), 
    (["dirac_constant", "ħ", "hbar", "atomic_unit_of_action", "a_u_action"], "h/(2*π)"), 
    (["avogadro_constant", "N_A"], "avogadro_number*mol^-1"), 
    (["molar_gas_constant", "R"], "k*N_A"),
    (["faraday_constant"], "e*N_A"),
    (["conductance_quantum", "G_0"], "2*e**2/h"),
    (["magnetic_flux_quantum", "Φ_0", "Phi_0"], "h/(2*e)"),
    (["josephson_constant", "K_J"], "2*e/h"),
    (["von_klitzing_constant", "R_K"], "h/e**2"),
    (["stefan_boltzmann_constant", "σ", "sigma"], "2/15*π**5*k**4/(h**3*c**2)"), 
    (["first_radiation_constant", "c_1"], "2*π*h*c**2"), 
    (["second_radiation_constant", "c_2"], "h*c/k"),
    (["wien_wavelength_displacement_law_constant"], "h*c/(k*wien_x)"),
    (["wien_frequency_displacement_law_constant"], "wien_u*k/h"),
    (["newtonian_constant_of_gravitation", "gravitational_constant"], "6.67430e-11m^3/(kg*s^2)"),
    (["rydberg_constant", "R_∞", "R_inf"], "1.0973731568160e7*m^-1"),
    (["electron_g_factor", "g_e"], "-2.00231930436256"),
    (["atomic_mass_constant", "m_u"], "1.66053906660e-27*kg"),
    (["electron_mass", "m_e", "atomic_unit_of_mass", "a_u_mass"], "9.1093837015e-31*kg"),
    (["proton_mass", "m_p"], "1.67262192369e-27*kg"),
    (["neutron_mass", "m_n"], "1.67492749804e-27*kg"),
    (["lattice_spacing_of_Si", "d_220"], "1.920155716e-10*m"),
    (["K_alpha_Cu_d_220"], "0.80232719"),
    (["K_alpha_Mo_d_220"], "0.36940604"),
    (["K_alpha_W_d_220"], "0.108852175"),
    (["fine_structure_constant", "α", "alpha"], "(2*h*R_inf/(m_e*c))**0.5"), 
    (["vacuum_permeability", "µ_0", "mu_0", "mu0", "magnetic_constant"], "2*α*h/(e**2*c)"), 
    (["vacuum_permittivity", "ε_0", "epsilon_0", "eps_0", "eps0", "electric_constant"], "e**2/(2*α*h*c)"), 
    (["impedance_of_free_space", "Z_0", "characteristic_impedance_of_vacuum"], "2*α*h/e**2"), 
    (["coulomb_constant", "k_C"], "α*hbar*c/e**2"), 
    (["classical_electron_radius", "r_e"], "α*hbar/(m_e*c)"), 
    (["thomson_cross_section", "σ_e", "sigma_e"], "8/3*π*r_e**2"), 
]

units = [
    "Acceleration",
        (["galileo", "Gal"], "centimeter/second**2"),
    "Amount of substance",
        (["particle", "molec", "molecule"], "1/N_A"),
    "Angle",
        ("radian"),
        (["turn", "revolution", "cycle", "circle"], "2π*radian"),
        (["degree", "deg", "arcdeg", "arcdegree", "angular_degree"], "π/180*radian"),
        (["arcminute", "arcmin", "arc_minute", "angular_minute"], "degree/60"),
        (["arcsecond", "arcsec", "arc_second", "angular_second"], "arcminute/60"),
        (["milliarcsecond", "mas"], "1e-3*arcsecond"),
        (["grade", "grad", "gon"], "π/200*radian"), 
        ("mil", "π/32000*radian"),
    "Area",
        ("are", "100*meter**2"),
        (["barn", "b"], "1e-28*meter**2"),
        ("darcy", "centipoise*centimeter**2/(second*atmosphere)"),
        (["ha", "hectare"], "100*are"),
    "Capacitance",
        (["F", "farad"], "coulomb/volt"),
        (["abfarad", "abF"], "1e9*farad"),
        (["conventional_farad_90", "F_90"], "R_K90/R_K*farad"),
    "Catalytic activity",
        (["katal", "kat"], "mole/second"),
        (["enzyme_unit", "U", "enzymeunit"], "micromole/minute"),
    "Charge",
        (["C", "coulomb"], "ampere*second"),
        (["abcoulomb", "abC"], "10*C"),
        ("faraday", "e*N_A*mole"),
        (["conventional_coulomb_90", "C_90"], "K_J90*R_K90/(K_J*R_K)*coulomb"),
        (["Ah", "ampere_hour"], "ampere*hour"), 
    "Concentration",
        (["mole", "mol"]),
        (["molar", "M"], "mole/liter"),
    "Conductance",
        (["S", "siemens", "mho"], "ampere/volt"),
        (["absiemens", "abS", "abmho"], "1e9*siemens"), 
    "Count",
        ("count"),
    "Current",
        (["A", "ampere", "amp"]),
        (["biot", "Bi"], "10*ampere"), 
        (["abampere", "abA", "biot", "abA"]),
        (["atomic_unit_of_current", "a_u_current"], "e/atomic_unit_of_time"), 
        (["mean_international_ampere", "A_it"], "mean_international_volt/mean_international_ohm"),
        (["US_international_ampere", "A_US"], "US_international_volt/US_international_ohm"), 
        (["conventional_ampere_90", "A_90"], "K_J90*R_K90/(K_J*R_K)*ampere"),
        (["planck_current"], "(c**6/gravitational_constant/k_C)**0.5"),
    "Density (as auxiliary for pressure)",
        (["mercury", "Hg", "Hg_0C", "Hg_32F", "conventional_mercury"], "13.5951*kilogram/liter"),
        (["water", "H2O", "conventional_water"], "1.0*kilogram/liter"),
        (["mercury_60F", "Hg_60F"], "13.5568*kilogram/liter"),
        (["water_39F", "water_4C"], "0.999972*kilogram/liter"),
        (["water_60F"], "0.999001*kilogram/liter"),
    "Electric field",
        # atomic_unit_of_electric_field = e * k_C / a_0 ** 2 = a_u_electric_field
    "Electric dipole moment",
    # [electric_dipole] = [charge] * [length]
    # debye = 1e-9 / ζ * coulomb * angstrom = D  # formally 1 D = 1e-10 Fr*Å, but we generally want to use it outside the Gaussian context
    "Electric potential",
        (["V", "volt"], "joule/coulomb"),
        # abvolt = 1e-8 * volt = abV
        # mean_international_volt = 1.00034 * volt = V_it  # approximate
        # US_international_volt = 1.00033 * volt = V_US    # approximate
        # conventional_volt_90 = K_J90 / K_J * volt = V_90
    "Electric quadrupole moment",
        # buckingham = debye * angstrom
    "Energy",
        (["J", "joule"], "newton*meter"),
        # erg = dyne * centimeter
        (["Wh", "watt_hour", "watthour"], "watt*hour"),
        # electron_volt = e * volt = eV
        # rydberg = h * c * R_inf = Ry
        # hartree = 2 * rydberg = E_h = Eh = hartree_energy = atomic_unit_of_energy = a_u_energy
        # calorie = 4.184 * joule = cal = thermochemical_calorie = cal_th
        # international_calorie = 4.1868 * joule = cal_it = international_steam_table_calorie
        # fifteen_degree_calorie = 4.1855 * joule = cal_15
        # british_thermal_unit = 1055.056 * joule = Btu = BTU = Btu_iso
        # international_british_thermal_unit = 1e3 * pound / kilogram * degR / kelvin * international_calorie = Btu_it
        # thermochemical_british_thermal_unit = 1e3 * pound / kilogram * degR / kelvin * calorie = Btu_th
        # quadrillion_Btu = 1e15 * Btu = quad
        # therm = 1e5 * Btu = thm = EC_therm
        # US_therm = 1.054804e8 * joule  # approximate, no exact definition
        # ton_TNT = 1e9 * calorie = tTNT
        # tonne_of_oil_equivalent = 1e10 * international_calorie = toe
        # atmosphere_liter = atmosphere * liter = atm_l
    "Entropy",
        # clausius = calorie / kelvin = Cl
    "Fluidity",
        # rhe = 1 / poise
    "Force",
        (["N", "newton"], "kilogram*meter/second**2"),
        # dyne = gram * centimeter / second ** 2 = dyn
        # force_kilogram = g_0 * kilogram = kgf = kilogram_force = pond
        # force_gram = g_0 * gram = gf = gram_force
        # force_metric_ton = g_0 * metric_ton = tf = metric_ton_force = force_t = t_force
        # atomic_unit_of_force = E_h / a_0 = a_u_force
    "Frequency",
        (["Hz", "hertz"], "1/second"),
        # revolutions_per_minute = revolution / minute = rpm
        # revolutions_per_second = revolution / second = rps
        # counts_per_second = count / second = cps
    "Heat transimission",
        # peak_sun_hour = 1e3 * watt_hour / meter ** 2 = PSH
        # langley = thermochemical_calorie / centimeter ** 2 = Ly
    "Illuminance",
        # lux = lumen / meter ** 2 = lx
    "Inductance",
        (["H", "henry"], "weber/ampere"),
        (["abhenry", "abH"], "1e-9*henry"), 
        (["conventional_henry_90", "H_90"], "R_K/R_K90*henry"),
    "Information",
        ("bit"),
        (["bps", "baud", "Bd"], "bit/second"), 
        (["B", "byte", "octet"], "8*bit"),
    "Intensity",
        # atomic_unit_of_intensity = 0.5 * ε_0 * c * atomic_unit_of_electric_field ** 2 = a_u_intensity
    "Kinematic viscosity",
        # stokes = centimeter ** 2 / second = St
    "Length",
        (["m", "meter", "metre"]),
        (["angstrom", "Å", "ångström", "Å"], "1e-10*meter"),
        (["micron", "micrometer", "µ"]),
        (["fermi", "femtometer", "fm"]),
        (["light_year", "ly", "lightyear"], "speed_of_light*julian_year"), 
        (["astronomical_unit", "au"], "149597870700*meter"),
        (["parsec", "pc"], "1/tansec*astronomical_unit"),
        (["nautical_mile", "nmi"], "1852*meter"), 
        (["bohr", "a_0", "a0", "bohr_radius", "atomic_unit_of_length", "a_u_length"], "hbar/(alpha*m_e*c)"),
        (["x_unit_Cu", "Xu_Cu"], "K_alpha_Cu_d_220*d_220/1537.4"), 
        (["x_unit_Mo", "Xu_Mo"], "K_alpha_Mo_d_220*d_220/707.831"), 
        (["angstrom_star", "Å_star"], "K_alpha_W_d_220*d_220/0.2090100"), 
        ("planck_length", "(hbar*gravitational_constant/c**3)**0.5"),
    "Logaritmic Units of dimensionless quantity",
        # decibelmilliwatt = 1e-3 watt; logbase: 10; logfactor: 10 = dBm
        # decibelmicrowatt = 1e-6 watt; logbase: 10; logfactor: 10 = dBu
        # decibel = 1 ; logbase: 10; logfactor: 10 = dB
        # decade = 1 ; logbase: 10; logfactor: 1
        # octave = 1 ; logbase: 2; logfactor: 1 = oct
        # neper = 1 ; logbase: 2.71828182845904523536028747135266249775724709369995; logfactor: 0.5 = Np
    "Luminosity",
        # candela = [luminosity] = cd = candle
    "Luminance",
        # nit = candela / meter ** 2
        # stilb = candela / centimeter ** 2
        # lambert = 1 / π * candela / centimeter ** 2
    "Luminous flux",
        # lumen = candela * steradian = lm
    "Magnetic dipole moment",
        # bohr_magneton = e * hbar / (2 * m_e) = µ_B = mu_B
        # nuclear_magneton = e * hbar / (2 * m_p) = µ_N = mu_N
    "Magnetic flux",
        (["Wb", "weber"], "volt*second"),
        # unit_pole = µ_0 * biot * centimeter
    "Magnetic field",
        # tesla = weber / meter ** 2 = T
        # gamma = 1e-9 * tesla = γ
    "Magnetomotive force",
        # ampere_turn = ampere = At
        # biot_turn = biot
        # gilbert = 1 / (4 * π) * biot_turn = Gb
    "Mass",
        (["g", "gram"]),
        # metric_ton = 1e3 * kilogram = t = tonne
        # unified_atomic_mass_unit = atomic_mass_constant = u = amu
        # dalton = atomic_mass_constant = Da
        # grain = 64.79891 * milligram = gr
        # gamma_mass = microgram
        # carat = 200 * milligram = ct = karat
        # planck_mass = (hbar * c / gravitational_constant) ** 0.5
    "Molar entropy",
        # entropy_unit = calorie / kelvin / mole = eu
    "Power",
        (["W", "watt"], "joule/second"),
        # volt_ampere = volt * ampere = VA
        # horsepower = 550 * foot * force_pound / second = hp = UK_horsepower = hydraulic_horsepower
        # boiler_horsepower = 33475 * Btu / hour                            # unclear which Btu
        # metric_horsepower = 75 * force_kilogram * meter / second
        # electrical_horsepower = 746 * watt
        # refrigeration_ton = 12e3 * Btu / hour = _ = ton_of_refrigeration  # approximate, no exact definition
        # standard_liter_per_minute = atmosphere * liter / minute = slpm = slm
        # conventional_watt_90 = K_J90 ** 2 * R_K90 / (K_J ** 2 * R_K) * watt = W_90
    "Pressure",
        # pascal = newton / meter ** 2 = Pa
        # barye = dyne / centimeter ** 2 = Ba = barie = barad = barrie = baryd
        # bar = 1e5 * pascal
        # technical_atmosphere = kilogram * g_0 / centimeter ** 2 = at
        # torr = atm / 760
        # pound_force_per_square_inch = force_pound / inch ** 2 = psi
        # kip_per_square_inch = kip / inch ** 2 = ksi
        # millimeter_Hg = millimeter * Hg * g_0 = mmHg = mm_Hg = millimeter_Hg_0C
        # centimeter_Hg = centimeter * Hg * g_0 = cmHg = cm_Hg = centimeter_Hg_0C
        # inch_Hg = inch * Hg * g_0 = inHg = in_Hg = inch_Hg_32F
        # inch_Hg_60F = inch * Hg_60F * g_0
        # inch_H2O_39F = inch * water_39F * g_0
        # inch_H2O_60F = inch * water_60F * g_0
        # foot_H2O = foot * water * g_0 = ftH2O = feet_H2O
        # centimeter_H2O = centimeter * water * g_0 = cmH2O = cm_H2O
        # sound_pressure_level = 20e-6 * pascal = SPL
    "Radiation",
        # becquerel = counts_per_second = Bq
        # curie = 3.7e10 * becquerel = Ci
        # rutherford = 1e6 * becquerel = Rd
        # gray = joule / kilogram = Gy
        # sievert = joule / kilogram = Sv
        # rads = 0.01 * gray
        # rem = 0.01 * sievert
        # roentgen = 2.58e-4 * coulomb / kilogram = _ = röntgen  # approximate, depends on medium
    "Resistance",
        (["Ω", "ohm"], "volt/ampere"),
        (["abohm", "abΩ"], "1e-9*ohm"), 
        (["mean_international_ohm", "Ω_it", "ohm_it"], "1.00049*ohm"),
        (["US_international_ohm", "Ω_US", "ohm_US"], "1.000495*ohm"),
        (["conventional_ohm_90", "Ω_90", "ohm_90"], "R_K/R_K90*ohm"),
    "Solid angle",
        (["steradian", "sr"], "radian**2"),
        (["square_degree", "sq_deg", "sqdeg"], "(π/180)**2*sr"), 
    "Temperature",
        # kelvin = [temperature]; offset: 0 = K = degK = °K = degree_Kelvin = degreeK  # older names supported for compatibility
        (["°C", "celsius", "degC", "degreeC", "degree_Celsius"], "kelvin; offset: 273.15"),
        # degree_Rankine = 5 / 9 * kelvin; offset: 0 = °R = rankine = degR = degreeR
        # degree_Fahrenheit = 5 / 9 * kelvin; offset: 233.15 + 200 / 9 = °F = fahrenheit = degF = degreeF
        # degree_Reaumur = 4 / 5 * kelvin; offset: 273.15 = °Re = reaumur = degRe = degreeRe = degree_Réaumur = réaumur
        # atomic_unit_of_temperature = E_h / k = a_u_temp
        # planck_temperature = (hbar * c ** 5 / gravitational_constant / k ** 2) ** 0.5
    "Time",
        (["s", "sec", "second"]), 
        # minute = 60 * second = min
        # hour = 60 * minute = hr
        # day = 24 * hour = d
        # week = 7 * day
        # fortnight = 2 * week
        # year = 365.25 * day = a = yr = julian_year
        # month = year / 12
        # century = 100 * year = _ = centuries
        # millennium = 1e3 * year = _ = millennia
        # eon = 1e9 * year
        # shake = 1e-8 * second
        # svedberg = 1e-13 * second
        # atomic_unit_of_time = hbar / E_h = a_u_time
        # gregorian_year = 365.2425 * day
        # sidereal_year = 365.256363004 * day                # approximate, as of J2000 epoch
        # tropical_year = 365.242190402 * day                # approximate, as of J2000 epoch
        # common_year = 365 * day
        # leap_year = 366 * day
        # sidereal_day = day / 1.00273790935079524           # approximate
        # sidereal_month = 27.32166155 * day                 # approximate
        # tropical_month = 27.321582 * day                   # approximate
        # synodic_month = 29.530589 * day = _ = lunar_month  # approximate
        # planck_time = (hbar * gravitational_constant / c ** 5) ** 0.5
    "Torque",
        # foot_pound = foot * force_pound = ft_lb = footpound
    "Velocity",
        # knot = nautical_mile / hour = kt = knot_international = international_knot
        # mile_per_hour = mile / hour = mph = MPH
        # kilometer_per_hour = kilometer / hour = kph = KPH
        # kilometer_per_second = kilometer / second = kps
        # meter_per_second = meter / second = mps
        # foot_per_second = foot / second = fps
    "Viscosity",
        (["poise", "P"], "0.1*Pa*second"),
        ("reyn", "psi*second"),
    "Volume",
        (["L", "liter", "l", "litre"], "decimeter**3"), 
        (["cubic_centimeter", "cc"], "centimeter**3"),
        (["lambda", "λ"], "microliter"), 
        ("stere", "meter**3"),
    "Wavenumber",
        (["reciprocal_centimeter", "cm_1", "kayser"], "1/cm"), 
]

# #### UNIT GROUPS ####
# # Mostly for length, area, volume, mass, force
# # (customary or specialized units)
#
# @group USCSLengthInternational
#     thou = 1e-3 * inch = th = mil_length
#     inch = yard / 36 = in = international_inch = inches = international_inches
#     hand = 4 * inch
#     foot = yard / 3 = ft = international_foot = feet = international_feet
#     yard = 0.9144 * meter = yd = international_yard  # since Jul 1959
#     mile = 1760 * yard = mi = international_mile
#
#     circular_mil = π / 4 * mil_length ** 2 = cmil
#     square_inch = inch ** 2 = sq_in = square_inches
#     square_foot = foot ** 2 = sq_ft = square_feet
#     square_yard = yard ** 2 = sq_yd
#     square_mile = mile ** 2 = sq_mi
#
#     cubic_inch = in ** 3 = cu_in
#     cubic_foot = ft ** 3 = cu_ft = cubic_feet
#     cubic_yard = yd ** 3 = cu_yd
# @end
#
# @group USCSLengthSurvey
#     link = 1e-2 * chain = li = survey_link
#     survey_foot = 1200 / 3937 * meter = sft
#     fathom = 6 * survey_foot
#     rod = 16.5 * survey_foot = rd = pole = perch
#     chain = 4 * rod
#     furlong = 40 * rod = fur
#     cables_length = 120 * fathom
#     survey_mile = 5280 * survey_foot = smi = us_statute_mile
#     league = 3 * survey_mile
#
#     square_rod = rod ** 2 = sq_rod = sq_pole = sq_perch
#     acre = 10 * chain ** 2
#     square_survey_mile = survey_mile ** 2 = _ = section
#     square_league = league ** 2
#
#     acre_foot = acre * survey_foot = _ = acre_feet
# @end
#
# @group USCSDryVolume
#     dry_pint = bushel / 64 = dpi = US_dry_pint
#     dry_quart = bushel / 32 = dqt = US_dry_quart
#     dry_gallon = bushel / 8 = dgal = US_dry_gallon
#     peck = bushel / 4 = pk
#     bushel = 2150.42 cubic_inch = bu
#     dry_barrel = 7056 cubic_inch = _ = US_dry_barrel
#     board_foot = ft * ft * in = FBM = board_feet = BF = BDFT = super_foot = superficial_foot = super_feet = superficial_feet
# @end
#
# @group USCSLiquidVolume
#     minim = pint / 7680
#     fluid_dram = pint / 128 = fldr = fluidram = US_fluid_dram = US_liquid_dram
#     fluid_ounce = pint / 16 = floz = US_fluid_ounce = US_liquid_ounce
#     gill = pint / 4 = gi = liquid_gill = US_liquid_gill
#     pint = quart / 2 = pt = liquid_pint = US_pint
#     fifth = gallon / 5 = _ = US_liquid_fifth
#     quart = gallon / 4 = qt = liquid_quart = US_liquid_quart
#     gallon = 231 * cubic_inch = gal = liquid_gallon = US_liquid_gallon
# @end
#
# @group USCSVolumeOther
#     teaspoon = fluid_ounce / 6 = tsp
#     tablespoon = fluid_ounce / 2 = tbsp
#     shot = 3 * tablespoon = jig = US_shot
#     cup = pint / 2 = cp = liquid_cup = US_liquid_cup
#     barrel = 31.5 * gallon = bbl
#     oil_barrel = 42 * gallon = oil_bbl
#     beer_barrel = 31 * gallon = beer_bbl
#     hogshead = 63 * gallon
# @end
#
# @group Avoirdupois
#     dram = pound / 256 = dr = avoirdupois_dram = avdp_dram = drachm
#     ounce = pound / 16 = oz = avoirdupois_ounce = avdp_ounce
#     pound = 7e3 * grain = lb = avoirdupois_pound = avdp_pound
#     stone = 14 * pound
#     quarter = 28 * stone
#     bag = 94 * pound
#     hundredweight = 100 * pound = cwt = short_hundredweight
#     long_hundredweight = 112 * pound
#     ton = 2e3 * pound = _ = short_ton
#     long_ton = 2240 * pound
#     slug = g_0 * pound * second ** 2 / foot
#     slinch = g_0 * pound * second ** 2 / inch = blob = slugette
#
#     force_ounce = g_0 * ounce = ozf = ounce_force
#     force_pound = g_0 * pound = lbf = pound_force
#     force_ton = g_0 * ton = _ = ton_force = force_short_ton = short_ton_force
#     force_long_ton = g_0 * long_ton = _ = long_ton_force
#     kip = 1e3 * force_pound
#     poundal = pound * foot / second ** 2 = pdl
# @end
#
# @group AvoirdupoisUK using Avoirdupois
#     UK_hundredweight = long_hundredweight = UK_cwt
#     UK_ton = long_ton
#     UK_force_ton = force_long_ton = _ = UK_ton_force
# @end
#
# @group AvoirdupoisUS using Avoirdupois
#     US_hundredweight = hundredweight = US_cwt
#     US_ton = ton
#     US_force_ton = force_ton = _ = US_ton_force
# @end
#
# @group Troy
#     pennyweight = 24 * grain = dwt
#     troy_ounce = 480 * grain = toz = ozt
#     troy_pound = 12 * troy_ounce = tlb = lbt
# @end
#
# @group Apothecary
#     scruple = 20 * grain
#     apothecary_dram = 3 * scruple = ap_dr
#     apothecary_ounce = 8 * apothecary_dram = ap_oz
#     apothecary_pound = 12 * apothecary_ounce = ap_lb
# @end
#
# @group ImperialVolume
#     imperial_minim = imperial_fluid_ounce / 480
#     imperial_fluid_scruple = imperial_fluid_ounce / 24
#     imperial_fluid_drachm = imperial_fluid_ounce / 8 = imperial_fldr = imperial_fluid_dram
#     imperial_fluid_ounce = imperial_pint / 20 = imperial_floz = UK_fluid_ounce
#     imperial_gill = imperial_pint / 4 = imperial_gi = UK_gill
#     imperial_cup = imperial_pint / 2 = imperial_cp = UK_cup
#     imperial_pint = imperial_gallon / 8 = imperial_pt = UK_pint
#     imperial_quart = imperial_gallon / 4 = imperial_qt = UK_quart
#     imperial_gallon = 4.54609 * liter = imperial_gal = UK_gallon
#     imperial_peck = 2 * imperial_gallon = imperial_pk = UK_pk
#     imperial_bushel = 8 * imperial_gallon = imperial_bu = UK_bushel
#     imperial_barrel = 36 * imperial_gallon = imperial_bbl = UK_bbl
# @end
#
# @group Printer
#     pica = inch / 6 = _ = printers_pica
#     point = pica / 12 = pp = printers_point = big_point = bp
#     didot = 1 / 2660 * m
#     cicero = 12 * didot
#     tex_point = inch / 72.27
#     tex_pica = 12 * tex_point
#     tex_didot = 1238 / 1157 * tex_point
#     tex_cicero = 12 * tex_didot
#     scaled_point = tex_point / 65536
#     css_pixel = inch / 96 = px
#
#     pixel = [printing_unit] = _ = dot = pel = picture_element
#     pixels_per_centimeter = pixel / cm = PPCM
#     pixels_per_inch = pixel / inch = dots_per_inch = PPI = ppi = DPI = printers_dpi
#     bits_per_pixel = bit / pixel = bpp
# @end
#
# @group Textile
#     tex = gram / kilometer = Tt
#     dtex = decitex
#     denier = gram / (9 * kilometer) = den = Td
#     jute = pound / (14400 * yard) = Tj
#     aberdeen = jute = Ta
#     RKM  = gf / tex
#
#     number_english = 840 * yard / pound = Ne = NeC = ECC
#     number_meter = kilometer / kilogram = Nm
# @end
#
#
# #### CGS ELECTROMAGNETIC UNITS ####
#
# # === Gaussian system of units ===
# @group Gaussian
#     franklin = erg ** 0.5 * centimeter ** 0.5 = Fr = statcoulomb = statC = esu
#     statvolt = erg / franklin = statV
#     statampere = franklin / second = statA
#     gauss = dyne / franklin = G
#     maxwell = gauss * centimeter ** 2 = Mx
#     oersted = dyne / maxwell = Oe = ørsted
#     statohm = statvolt / statampere = statΩ
#     statfarad = franklin / statvolt = statF
#     statmho = statampere / statvolt
# @end
# # Note this system is not commensurate with SI, as ε_0 and µ_0 disappear;
# # some quantities with different dimensions in SI have the same
# # dimensions in the Gaussian system (e.g. [Mx] = [Fr], but [Wb] != [C]),
# # and therefore the conversion factors depend on the context (not in pint sense)
# [gaussian_charge] = [length] ** 1.5 * [mass] ** 0.5 / [time]
# [gaussian_current] = [gaussian_charge] / [time]
# [gaussian_electric_potential] = [gaussian_charge] / [length]
# [gaussian_electric_field] = [gaussian_electric_potential] / [length]
# [gaussian_electric_displacement_field] = [gaussian_charge] / [area]
# [gaussian_electric_flux] = [gaussian_charge]
# [gaussian_electric_dipole] = [gaussian_charge] * [length]
# [gaussian_electric_quadrupole] = [gaussian_charge] * [area]
# [gaussian_magnetic_field] = [force] / [gaussian_charge]
# [gaussian_magnetic_field_strength] = [gaussian_magnetic_field]
# [gaussian_magnetic_flux] = [gaussian_magnetic_field] * [area]
# [gaussian_magnetic_dipole] = [energy] / [gaussian_magnetic_field]
# [gaussian_resistance] = [gaussian_electric_potential] / [gaussian_current]
# [gaussian_resistivity] = [gaussian_resistance] * [length]
# [gaussian_capacitance] = [gaussian_charge] / [gaussian_electric_potential]
# [gaussian_inductance] = [gaussian_electric_potential] * [time] / [gaussian_current]
# [gaussian_conductance] = [gaussian_current] / [gaussian_electric_potential]
# @context Gaussian = Gau
#     [gaussian_charge] -> [charge]: value / k_C ** 0.5
#     [charge] -> [gaussian_charge]: value * k_C ** 0.5
#     [gaussian_current] -> [current]: value / k_C ** 0.5
#     [current] -> [gaussian_current]: value * k_C ** 0.5
#     [gaussian_electric_potential] -> [electric_potential]: value * k_C ** 0.5
#     [electric_potential] -> [gaussian_electric_potential]: value / k_C ** 0.5
#     [gaussian_electric_field] -> [electric_field]: value * k_C ** 0.5
#     [electric_field] -> [gaussian_electric_field]: value / k_C ** 0.5
#     [gaussian_electric_displacement_field] -> [electric_displacement_field]: value / (4 * π / ε_0) ** 0.5
#     [electric_displacement_field] -> [gaussian_electric_displacement_field]: value * (4 * π / ε_0) ** 0.5
#     [gaussian_electric_dipole] -> [electric_dipole]: value / k_C ** 0.5
#     [electric_dipole] -> [gaussian_electric_dipole]: value * k_C ** 0.5
#     [gaussian_electric_quadrupole] -> [electric_quadrupole]: value / k_C ** 0.5
#     [electric_quadrupole] -> [gaussian_electric_quadrupole]: value * k_C ** 0.5
#     [gaussian_magnetic_field] -> [magnetic_field]: value / (4 * π / µ_0) ** 0.5
#     [magnetic_field] -> [gaussian_magnetic_field]: value * (4 * π / µ_0) ** 0.5
#     [gaussian_magnetic_flux] -> [magnetic_flux]: value / (4 * π / µ_0) ** 0.5
#     [magnetic_flux] -> [gaussian_magnetic_flux]: value * (4 * π / µ_0) ** 0.5
#     [gaussian_magnetic_field_strength] -> [magnetic_field_strength]: value / (4 * π * µ_0) ** 0.5
#     [magnetic_field_strength] -> [gaussian_magnetic_field_strength]: value * (4 * π * µ_0) ** 0.5
#     [gaussian_magnetic_dipole] -> [magnetic_dipole]: value * (4 * π / µ_0) ** 0.5
#     [magnetic_dipole] -> [gaussian_magnetic_dipole]: value / (4 * π / µ_0) ** 0.5
#     [gaussian_resistance] -> [resistance]: value * k_C
#     [resistance] -> [gaussian_resistance]: value / k_C
#     [gaussian_resistivity] -> [resistivity]: value * k_C
#     [resistivity] -> [gaussian_resistivity]: value / k_C
#     [gaussian_capacitance] -> [capacitance]: value / k_C
#     [capacitance] -> [gaussian_capacitance]: value * k_C
#     [gaussian_inductance] -> [inductance]: value * k_C
#     [inductance] -> [gaussian_inductance]: value / k_C
#     [gaussian_conductance] -> [conductance]: value / k_C
#     [conductance] -> [gaussian_conductance]: value * k_C
# @end
#
# # === ESU system of units ===
# #   (where different from Gaussian)
# #   See note for Gaussian system too
# @group ESU using Gaussian
#     statweber = statvolt * second = statWb
#     stattesla = statweber / centimeter ** 2 = statT
#     stathenry = statweber / statampere = statH
# @end
# [esu_charge] = [length] ** 1.5 * [mass] ** 0.5 / [time]
# [esu_current] = [esu_charge] / [time]
# [esu_electric_potential] = [esu_charge] / [length]
# [esu_magnetic_flux] = [esu_electric_potential] * [time]
# [esu_magnetic_field] = [esu_magnetic_flux] / [area]
# [esu_magnetic_field_strength] = [esu_current] / [length]
# [esu_magnetic_dipole] = [esu_current] * [area]
# @context ESU = esu
#     [esu_magnetic_field] -> [magnetic_field]: value * k_C ** 0.5
#     [magnetic_field] -> [esu_magnetic_field]: value / k_C ** 0.5
#     [esu_magnetic_flux] -> [magnetic_flux]: value * k_C ** 0.5
#     [magnetic_flux] -> [esu_magnetic_flux]: value / k_C ** 0.5
#     [esu_magnetic_field_strength] -> [magnetic_field_strength]: value / (4 * π / ε_0) ** 0.5
#     [magnetic_field_strength] -> [esu_magnetic_field_strength]: value * (4 * π / ε_0) ** 0.5
#     [esu_magnetic_dipole] -> [magnetic_dipole]: value / k_C ** 0.5
#     [magnetic_dipole] -> [esu_magnetic_dipole]: value * k_C ** 0.5
# @end
#
#
# #### CONVERSION CONTEXTS ####
#
# @context(n=1) spectroscopy = sp
#     # n index of refraction of the medium.
#     [length] <-> [frequency]: speed_of_light / n / value
#     [frequency] -> [energy]: planck_constant * value
#     [energy] -> [frequency]: value / planck_constant
#     # allow wavenumber / kayser
#     [wavenumber] <-> [length]: 1 / value
# @end
#
# @context boltzmann
#     [temperature] -> [energy]: boltzmann_constant * value
#     [energy] -> [temperature]: value / boltzmann_constant
# @end
#
# @context energy
#     [energy] -> [energy] / [substance]: value * N_A
#     [energy] / [substance] -> [energy]: value / N_A
#     [energy] -> [mass]: value / c ** 2
#     [mass] -> [energy]: value * c ** 2
# @end
#
# @context(mw=0,volume=0,solvent_mass=0) chemistry = chem
#     # mw is the molecular weight of the species
#     # volume is the volume of the solution
#     # solvent_mass is the mass of solvent in the solution
#
#     # moles -> mass require the molecular weight
#     [substance] -> [mass]: value * mw
#     [mass] -> [substance]: value / mw
#
#     # moles/volume -> mass/volume and moles/mass -> mass/mass
#     # require the  molecular weight
#     [substance] / [volume] -> [mass] / [volume]: value * mw
#     [mass] / [volume] -> [substance] / [volume]: value / mw
#     [substance] / [mass] -> [mass] / [mass]: value * mw
#     [mass] / [mass] -> [substance] / [mass]: value / mw
#
#     # moles/volume -> moles requires the solution volume
#     [substance] / [volume] -> [substance]: value * volume
#     [substance] -> [substance] / [volume]: value / volume
#
#     # moles/mass -> moles requires the solvent (usually water) mass
#     [substance] / [mass] -> [substance]: value * solvent_mass
#     [substance] -> [substance] / [mass]: value / solvent_mass
#
#     # moles/mass -> moles/volume require the solvent mass and the volume
#     [substance] / [mass] -> [substance]/[volume]: value * solvent_mass / volume
#     [substance] / [volume] -> [substance] / [mass]: value / solvent_mass * volume
#
# @end
#
# @context textile
#     # Allow switching between Direct count system (i.e. tex) and
#     # Indirect count system (i.e. Ne, Nm)
#     [mass] / [length] <-> [length] / [mass]: 1 / value
# @end
#
#
# #### SYSTEMS OF UNITS ####
#
# @system SI
#     second
#     meter
#     kilogram
#     ampere
#     kelvin
#     mole
#     candela
# @end
#
# @system mks using international
#     meter
#     kilogram
#     second
# @end
#
# @system cgs using international, Gaussian, ESU
#     centimeter
#     gram
#     second
# @end
#
# @system atomic using international
#     # based on unit m_e, e, hbar, k_C, k
#     bohr: meter
#     electron_mass: gram
#     atomic_unit_of_time: second
#     atomic_unit_of_current: ampere
#     atomic_unit_of_temperature: kelvin
# @end
#
# @system Planck using international
#     # based on unit c, gravitational_constant, hbar, k_C, k
#     planck_length: meter
#     planck_mass: gram
#     planck_time: second
#     planck_current: ampere
#     planck_temperature: kelvin
# @end
#
# @system imperial using ImperialVolume, USCSLengthInternational, AvoirdupoisUK
#     yard
#     pound
# @end
#
# @system US using USCSLiquidVolume, USCSDryVolume, USCSVolumeOther, USCSLengthInternational, USCSLengthSurvey, AvoirdupoisUS
#     yard
#     pound
# @end

class QUnitMenu(QMenu):
    unitSelected = pyqtSignal(str)
    
    def __init__(self, *args, **kwargs):
        super(QUnitMenu, self).__init__(*args, **kwargs)

        # TODO tweak presentation with QStyleOptionMenuItem

        for item in base_units:
            if item=="":
                self.addSeparator()
            else:
                self.AddUnit(item, self)
        
        self.addSeparator()
        
        constantsMenu = QMenu("Constants", self)
        self.addAction(constantsMenu.menuAction())
        for item in constants:
            self.AddUnit(item, constantsMenu)

        otherMenu = QMenu("Other", self)
        self.addAction(otherMenu.menuAction())
        submenu = otherMenu
        for item in units:
            if isinstance(item, str):
                submenu = QMenu(item, otherMenu)
                otherMenu.addAction(submenu.menuAction())
            else:
                self.AddUnit(item, submenu)
    
    def AddUnit(self, item, menu):
        unit = ""
        description = None
        if isinstance(item, tuple):
            unit, description = item
        else:
            unit = item
        
        if isinstance(unit, list):
            text = f"{'/'.join(unit)}"
        else:
            text = f"{unit}"
        if description is not None:
            text += f" ({description})"

        action = QAction(parent=menu, text=text)
        action.unit = item
        action.triggered.connect(self.selectUnitAction)
        menu.addAction(action)
        
    def selectUnitAction(self):
        item = self.sender().unit
        
        if isinstance(item, tuple):
            unit, = item
        else:
            unit = item
        
        if isinstance(unit, list):
            unit = unit[0]
        
        self.unitSelected.emit(unit)
