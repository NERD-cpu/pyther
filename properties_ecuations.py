import numpy as np
import pandas as pd
import pyther as pt


size_data = 30
# properties thermodynamics

Solid_Density = "Solid Density", "[kmol/m^3]", "A+B*T+C*T^2+D*T^3+E*T^4", 0
Liquid_Density = "Liquid Density", "[kmol/m^3]", "A/B^(1+(1-T/C)^D)", 1
Vapour_Pressure = "Vapour Pressure", "[Pa]", "exp(A+B/T+C*ln(T)+D*T^E)", 2
Heat_of_Vaporization = "Heat of Vaporization", "[J/kmol]", "A*(1-Tr)^(B+C*Tr+D*Tr^2)", 3
Solid_Heat_Capacity = "Solid Heat Capacity", "[J/(kmol*K)]", "A+B*T+C*T^2+D*T^3+E*T^4", 4
Liquid_Heat_Capacity = "Liquid Heat Capacity", "[J/(kmol*K)]", "A^2/(1-Tr)+B-2*A*C*(1-Tr)-A*D*(1-Tr)^2-C^2*(1-Tr)^3/3-C*D*(1-Tr)^4/2-D^2*(1-Tr)^5/5", 5
Ideal_Gas_Heat_Capacity = "Ideal Gas Heat Capacity" "[J/(kmol*K)]", "A+B*(C/T/sinh(C/T))^2+D*(E/T/cosh(E/T))^2", 6
Second_Virial_Coefficient = "Second	Virial	Coefficient", "[m^3/kmol]", "A+B/T+C/T^3+D/T^8+E/T^9", 7
Liquid_Viscosity = "Liquid	Viscosity", "[kg/(m*s)]", "exp(A+B/T+C*ln(T)+D*T^E)", 8
Vapour_Viscosity = "Vapour	Viscosity", "[kg/(m*s)]", "A*T^B/(1+C/T+D/T^2)", 9
Liquid_Thermal_Conductivity = "Liquid Thermal Conductivity", "[J/(m*s*K)]", "A+B*T+C*T^2+D*T^3+E*T^4", 10
Vapour_Thermal_Conductivity = "Vapour Thermal Conductivity", "[J/(m*s*K)]", "A*T^B/(1+C/T+D/T^2)", 11
Surface_Tension = "Surface Tension", "[kg/s^2]", "A*(1-Tr)^(B+C*Tr+D*Tr^2)", 12	

#----------------------------------------------------------------------------------------------------------------


def read_dppr(dppr_file):
        #self.dppr_data = pd.read_excel(dppr_file).head().set_index('Name').ix[:, 1:12]

        #dppr_data = pd.read_excel(dppr_file).set_index("Name").ix[:, 1:5]
        dppr_data = pd.read_excel(dppr_file).ix[:, 0:8]
        
        # component_names = dppr_data.index.get_values()
        return dppr_data

#print(data)


def property_cal(data, data_name, component, property_thermodynamics, temperature = None):
	"""
	properties thermodynamics

	Solid_Density = "Solid Density", "[kmol/m^3]", "A+B*T+C*T^2+D*T^3+E*T^4", 0
	Liquid_Density = "Liquid Density", "[kmol/m^3]", "A/B^(1+(1-T/C)^D)", 1
	Vapour_Pressure = "Vapour Pressure", "[Pa]", "exp(A+B/T+C*ln(T)+D*T^E)", 2
	Heat_of_Vaporization = "Heat of Vaporization", "[J/kmol]", "A*(1-Tr)^(B+C*Tr+D*Tr^2)", 3
	Solid_Heat_Capacity = "Solid Heat Capacity", "[J/(kmol*K)]", "A+B*T+C*T^2+D*T^3+E*T^4", 4
	Liquid_Heat_Capacity = "Liquid Heat Capacity", "[J/(kmol*K)]", "A^2/(1-Tr)+B-2*A*C*(1-Tr)-A*D*(1-Tr)^2-C^2*(1-Tr)^3/3-C*D*(1-Tr)^4/2-D^2*(1-Tr)^5/5", 5
	Ideal_Gas_Heat_Capacity = "Ideal Gas Heat Capacity" "[J/(kmol*K)]", "A+B*(C/T/sinh(C/T))^2+D*(E/T/cosh(E/T))^2", 6
	Second_Virial_Coefficient = "Second	Virial	Coefficient", "[m^3/kmol]", "A+B/T+C/T^3+D/T^8+E/T^9", 7
	Liquid_Viscosity = "Liquid	Viscosity", "[kg/(m*s)]", "exp(A+B/T+C*ln(T)+D*T^E)", 8
	Vapour_Viscosity = "Vapour	Viscosity", "[kg/(m*s)]", "A*T^B/(1+C/T+D/T^2)", 9
	Liquid_Thermal_Conductivity = "Liquid Thermal Conductivity", "[J/(m*s*K)]", "A+B*T+C*T^2+D*T^3+E*T^4", 10
	Vapour_Thermal_Conductivity = "Vapour Thermal Conductivity", "[J/(m*s*K)]", "A*T^B/(1+C/T+D/T^2)", 11
	Surface_Tension = "Surface Tension", "[kg/s^2]", "A*(1-Tr)^(B+C*Tr+D*Tr^2)", 12	
	"""

	select_constans = [x + property_thermodynamics[3] for x in range(0, 13*size_data, 13)]
	values_constans = data.ix[select_constans, 1:8].get_values()
	table_constans = pd.DataFrame(data=values_constans,index=data_name,
						 columns=["A", "B", "C", "D", "E", "T Min [K]", "T Max [K]"])

	print(table_constans)
	component_constans = table_constans.loc[component]
	print(component_constans)

	#Min, Max = np.zeros(2), np.array(2)

	A, B, C, D, E, Min, Max = component_constans.get_values()

	#print("sss = ",Min, Max)


	if temperature == None:
		Temp_vector = np.array([Temp_vector for Temp_vector in np.arange(Min, Max)])
	else:
		#print("type of temperature = ", type(temperature))
		if type(temperature) != list: temperature = [temperature]		
		
		Temperature_enter = [i if Min < np.array(i) < Max
		 else "{0} K is a temperature not valid".format(i) for i in temperature]
		Temperature_invalid = [i for i in Temperature_enter if type(i) == str]
		Temperature_valid = [i for i in Temperature_enter if type(i) != str]

		print("Temperature_enter = {0}".format(Temperature_enter))
		print("Temperature_invalid = {0}".format(Temperature_invalid))
		print("Temperature_valid = {0}".format(Temperature_valid))
		
		Temp_vector = np.array(Temperature_valid)

	if property_thermodynamics == Solid_Density:
		solid_Density = A + B * Temp_vector + C * Temp_vector ** 2 + D * Temp_vector ** 3 + E * Temp_vector **4		
		return solid_Density
	elif property_thermodynamics == Liquid_Density:
		liquid_Density = A / B ** (1 + (1 - Temp_vector / C) ** D)		
		return liquid_Density
	elif property_thermodynamics == Vapour_Pressure:
		vapour_Pressure = np.exp(A + B/Temp_vector + C * np.log(Temp_vector)+D*Temp_vector **E)		
		return vapour_Pressure
	elif property_thermodynamics == Heat_of_Vaporization:
		heat_of_Vaporization = A*(1-Tr) ** (B+C*Tr+D*Tr**2)		
		return heat_of_Vaporization
	elif property_thermodynamics == Solid_Heat_Capacity:
		solid_Heat_Capacity = A + B * Temp_vector + C * Temp_vector ** 2 + D * Temp_vector ** 3 + E * Temp_vector ** 4
		return solid_Heat_Capacity
	elif property_thermodynamics == Liquid_Heat_Capacity:
		liquid_Heat_Capacity = A ** 2 / (1-Tr) + B-2*A*C*(1-Tr)-A*D*(1-Tr)**2-C**2*(1-Tr)**3/3-C*D*(1-Tr)**4/2-D**2*(1-Tr)**5/5
		return(liquid_Heat_Capacity)
	elif property_thermodynamics == Ideal_Gas_Heat_Capacity:
		ideal_Gas_Heat_Capacity = A+B*(C/Temp_vector/np.sinh(C/Temp_vector))**2+D*(E/Temp_vector/np.cosh(E/Temp_vector))**2
		return ideal_Gas_Heat_Capacity
	elif property_thermodynamics == Second_Virial_Coefficient:
		second_Virial_Coefficient = A+B/Temp_vector+C/Temp_vector**3+D/Temp_vector**8+E/Temp_vector**9
		return second_Virial_Coefficient
	elif property_thermodynamics == Liquid_Viscosity:
		liquid_Viscosity = np.exp(A + B / Temp_vector + C * np.log(Temp_vector) + D * Temp_vector ** E)
		return liquid_Viscosity
	elif property_thermodynamics == Vapour_Viscosity:
		vapour_Viscosity = A*Temp_vector**B/(1+C/Temp_vector+D/Temp_vector**2)
		return vapour_Viscosity
	elif property_thermodynamics == Liquid_Thermal_Conductivity:
		liquid_Thermal_Conductivity = A+B*Temp_vector+C*Temp_vector**2+D*Temp_vector**3+E*Temp_vector**4
		return liquid_Thermal_Conductivity
	elif property_thermodynamics == Vapour_Thermal_Conductivity:
		vapour_Thermal_Conductivity = A*Temp_vector**B/(1+C/Temp_vector+D/Temp_vector**2)
		return vapour_Thermal_Conductivity
	elif property_thermodynamics == Surface_Tension:
		surface_Tension = A*(1-Tr)**(B+C*Tr+D*Tr*2)
		return surface_Tension


def main():

	print("-" * 79)

	dppr_file = "PureFull_mod_properties.xls"
	#print(dppr_file)
	data = read_dppr(dppr_file)
	properties_data = pt.Data_parse()

	#size_data = 30
	components_labels = [x for x in range(0, 13*size_data, 13)]
	data_name = data.ix[components_labels, 0].get_values()

	component = 'METHANE'
	#component = "ETHANE"
	#component = "3-METHYLHEPTANE"
	#component = "n-PENTACOSANE"
	#component = "ISOBUTANE"
	#component = "n-TETRADECANE"

	#components = ["METHANE", "n-TETRACOSANE"]

	temp = [180.4, 181.4, 185.3, 210, 85]
	temp = 180.4

	property_thermodynamics = property_cal(data, data_name, component, Vapour_Pressure, temp)
	#property_thermodynamics = property_cal(components, Vapour_Pressure, temp)
	#property_thermodynamics = property_cal(component, Vapour_Pressure, [180.4, 181.4, 185.3, 210, 85])
	#property_thermodynamics = property_cal(component, Vapour_Pressure)
	print(property_thermodynamics)

	print('-' * 79)

if __name__ == '__main__':
	main()
