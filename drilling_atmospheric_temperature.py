# Python Script to Calculate Heat Energy Removal and Number of Holes Required

# Issues:
# Oversimplification of heat transfer:
#       The current model assumes constant heat transfer along the entire depth of the hole, which
#       is not realistic. The temperature difference between the air and the ground will decrease
#       at higher and lower depths than the neutral temperature zone (20m)

# Import necessary libraries
import math

# Constants and Assumptions

# Atmospheric Parameters
AREA_MILES = 1  # Area in square miles
DELTA_T = 1  # Temperature change in Celsius
AIR_SPECIFIC_HEAT = 1005  # Specific heat capacity of air at constant pressure in J/(kg·°C)
AIR_DENSITY = 1.225  # Air density at sea level in kg/m³ (standard atmosphere)

# Conversion Factors
MILE_TO_METER = 1609.34  # 1 mile in meters
SQUARE_MILE_TO_SQUARE_METER = MILE_TO_METER ** 2  # 1 square mile in square meters
HOURS_IN_DAY = 24
SECONDS_IN_HOUR = 3600
SECONDS_IN_DAY = HOURS_IN_DAY * SECONDS_IN_HOUR
SECONDS_IN_MONTH = SECONDS_IN_DAY * 30

# Hole Parameters
HOLE_DIAMETER_INCHES = 1  # Hole diameter in inches
HOLE_DIAMETER_METERS = HOLE_DIAMETER_INCHES * 0.0254  # 1 inch = 0.0254 meters
HOLE_DEPTH_METERS = 400  # Hole depth in meters
AIR_VELOCITY = 10  # Air velocity in m/s (practical airflow rate)
AIR_TEMPERATURE = 30  # Air temperature in °C
GROUND_TEMPERATURE = 20  # Ground temperature in °C
TEMPERATURE_DIFFERENCE = AIR_TEMPERATURE - GROUND_TEMPERATURE  # ΔT in °C

# Air Properties at 30°C
AIR_VISCOSITY = 1.85e-5  # Dynamic viscosity in Pa·s
AIR_THERMAL_CONDUCTIVITY = 0.0263  # Thermal conductivity in W/(m·K)
AIR_PRANDTL_NUMBER = 0.707  # Prandtl number (dimensionless)
AIR_DENSITY = 1.164  # Air density at 30°C in kg/m³

# Fan Efficiency
FAN_EFFICIENCY = 0.7  # 70% efficiency

# Ground Properties
GROUND_THERMAL_CONDUCTIVITY = 2.0  # W/(m·K), typical value for soil

# Step 1: Calculate the Mass of Air over 1 Square Mile
def calculate_air_mass(area_miles):
    # Convert area to square meters
    area_meters = area_miles * SQUARE_MILE_TO_SQUARE_METER
    # Calculate mass per unit area (Pressure / gravity)
    pressure = 101325  # Atmospheric pressure in Pascals
    gravity = 9.81  # Gravity in m/s²
    mass_per_unit_area = pressure / gravity  # kg/m²
    # Total mass of air
    total_mass = mass_per_unit_area * area_meters  # kg
    return total_mass, area_meters

# Step 2: Calculate the Energy Required to Lower Temperature by 1°C
def calculate_energy_required(mass, delta_T, specific_heat):
    energy_required = mass * specific_heat * delta_T  # Joules
    return energy_required

# Step 3: Calculate Heat Transfer per Hole
def calculate_heat_transfer_per_hole():
    # Calculate surface area of the hole (lateral surface area)
    circumference = math.pi * HOLE_DIAMETER_METERS
    surface_area = circumference * HOLE_DEPTH_METERS  # m²

    # Calculate thermal resistance of air and ground
    r_air = HOLE_DIAMETER_METERS / (2 * AIR_THERMAL_CONDUCTIVITY * surface_area)
    r_ground = math.log((HOLE_DIAMETER_METERS + 1) / HOLE_DIAMETER_METERS) / (2 * math.pi * GROUND_THERMAL_CONDUCTIVITY * HOLE_DEPTH_METERS)

    # Total thermal resistance
    r_total = r_air + r_ground

    # Calculate heat transfer
    heat_transfer_per_hole = TEMPERATURE_DIFFERENCE / r_total  # Watts

    return heat_transfer_per_hole

# Step 4: Calculate Energy Removed by One Hole in One Month
def calculate_energy_removed_per_hole(heat_transfer_per_hole):
    energy_removed_per_hole = heat_transfer_per_hole * SECONDS_IN_MONTH  # Joules
    return energy_removed_per_hole

# Step 5: Calculate Number of Holes Required
def calculate_number_of_holes(total_energy_required, energy_removed_per_hole):
    number_of_holes = total_energy_required / energy_removed_per_hole
    return number_of_holes

# Step 6: Main Function to Perform Calculations
def main():
    # Step 1
    total_mass, area_meters = calculate_air_mass(AREA_MILES)
    print(f"Total mass of air over {AREA_MILES} square mile(s): {total_mass:.2e} kg")
    print(f"Total area in square meters: {area_meters:.2e} m²\n")

    # Step 2
    total_energy_required = calculate_energy_required(total_mass, DELTA_T, AIR_SPECIFIC_HEAT)
    print(f"Total energy required to lower temperature by {DELTA_T}°C: {total_energy_required:.2e} Joules\n")

    # Step 3
    heat_transfer_per_hole = calculate_heat_transfer_per_hole()
    print(f"Conductive heat transfer per hole: {heat_transfer_per_hole:.2f} Watts")

    # Step 4
    energy_removed_per_hole = calculate_energy_removed_per_hole(heat_transfer_per_hole)
    print(f"Energy removed per hole in one month: {energy_removed_per_hole:.2e} Joules\n")

    # Step 5
    number_of_holes = calculate_number_of_holes(total_energy_required, energy_removed_per_hole)
    print(f"Number of holes required: {number_of_holes:.2f}")

    # Additional Output for Practicality
    # Calculate area per hole
    # TODO instead of this, we should see how close they can be without affecting each other's heat transfer
    area_per_hole = area_meters / number_of_holes  # m²/hole
    spacing_between_holes = math.sqrt(area_per_hole)  # meters
    print(f"Area per hole: {area_per_hole:.2f} m²/hole")
    print(f"Spacing between holes: {spacing_between_holes:.2f} meters\n")

    # Operational Energy Consumption
    # Calculate power required to move air (simplified)
    hole_radius = HOLE_DIAMETER_METERS / 2
    cross_sectional_area = math.pi * (hole_radius ** 2)
    volumetric_flow_rate = cross_sectional_area * AIR_VELOCITY  # m³/s
    mass_flow_rate = volumetric_flow_rate * AIR_DENSITY  # kg/s
    fan_power = (mass_flow_rate * (AIR_VELOCITY ** 2)) / (2 * FAN_EFFICIENCY)  # Watts
    print(f"Fan power required per hole: {fan_power:.2f} Watts")

# Run the main function
if __name__ == "__main__":
    main()
