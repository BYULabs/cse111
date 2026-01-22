"""Calculates water pressure at a house given parameters of the water tower.
Returns water pressure in kilopascals and psi."""

PVC_SCHED80_INNER_DIAMETER = 0.28687 # (meters)  11.294 inches
PVC_SCHED80_FRICTION_FACTOR = 0.013  # (unitless)
SUPPLY_VELOCITY = 1.65               # (meters / second)
HDPE_SDR11_INNER_DIAMETER = 0.048692 # (meters)  1.917 inches
HDPE_SDR11_FRICTION_FACTOR = 0.018   # (unitless)
HOUSEHOLD_VELOCITY = 1.75            # (meters / second)
WATER_DENSITY = 998.2                # density of water (998.2 kilogram / meter^3)
EARTH_ACCELERATION_OF_GRAVITY = 9.8066500
WATER_DYNAMIC_VISCOSITY = 0.0010016


def main():
    """Prompts the user for water system parameters and calculates water
    pressure at the house in both kilopascals and psi."""
    tower_height = float(input("Height of water tower (meters): "))
    tank_height = float(input("Height of water tank walls (meters): "))
    length1 = float(input("Length of supply pipe from tank to lot (meters): "))
    quantity_angles = int(input("Number of 90° angles in supply pipe: "))
    length2 = float(input("Length of pipe from supply to house (meters): "))

    water_height = water_column_height(tower_height, tank_height)
    pressure = pressure_gain_from_water_height(water_height)
    diameter = PVC_SCHED80_INNER_DIAMETER
    friction = PVC_SCHED80_FRICTION_FACTOR
    velocity = SUPPLY_VELOCITY
    reynolds = reynolds_number(diameter, velocity)
    loss = pressure_loss_from_pipe(diameter, length1, friction, velocity)
    pressure += loss
    loss = pressure_loss_from_fittings(velocity, quantity_angles)
    pressure += loss
    loss = pressure_loss_from_pipe_reduction(diameter,
            velocity, reynolds, HDPE_SDR11_INNER_DIAMETER)
    pressure += loss
    diameter = HDPE_SDR11_INNER_DIAMETER
    friction = HDPE_SDR11_FRICTION_FACTOR
    velocity = HOUSEHOLD_VELOCITY
    loss = pressure_loss_from_pipe(diameter, length2, friction, velocity)
    pressure += loss
    pressure_psi = convert_kpa_to_psi(pressure)
    print(f"Pressure at house: {pressure:.1f} kilopascals")
    print(f"Pressure at house: {pressure_psi:.1f} psi")


def water_column_height(tower_height, tank_height):
    """Calculate the height of the water column from the tower and tank.
    
    Args:
        tower_height: Height of the water tower in meters.
        tank_height: Height of the water tank walls in meters.
    
    Returns:
        The total water column height in meters.
    """
    return tower_height + 3 * tank_height / 4


def pressure_gain_from_water_height(height):
    """Calculate the pressure gain from the water column height.
    
    Args:
        height: Height of the water column in meters.
    
    Returns:
        The pressure gained in kilopascals.
    """
    return WATER_DENSITY * EARTH_ACCELERATION_OF_GRAVITY * height / 1000


def pressure_loss_from_pipe(pipe_diameter, pipe_length, friction_factor,
                            fluid_velocity):
    """Calculate the pressure loss due to friction in the pipe.
    
    Args:
        pipe_diameter: Inner diameter of the pipe in meters.
        pipe_length: Length of the pipe in meters.
        friction_factor: Friction factor of the pipe material (unitless).
        fluid_velocity: Velocity of fluid flowing through pipe in m/s.
    
    Returns:
        The pressure loss in kilopascals.
    """
    numerator = -friction_factor * pipe_length * WATER_DENSITY * \
                fluid_velocity ** 2
    denominator = 2000 * pipe_diameter
    return numerator / denominator


def pressure_loss_from_fittings(fluid_velocity, quantity_fittings):
    """Calculate the pressure loss from pipe fittings and angles.
    
    Args:
        fluid_velocity: Velocity of fluid flowing through pipe in m/s.
        quantity_fittings: Number of 90-degree angles in the pipe.
    
    Returns:
        The pressure loss in kilopascals.
    """
    return -.04 * WATER_DENSITY * fluid_velocity ** 2 * \
           quantity_fittings / 2000


def reynolds_number(hydraulic_diameter, fluid_velocity):
    """Calculate the Reynolds number for the fluid flow.
    
    Args:
        hydraulic_diameter: Hydraulic diameter of the pipe in meters.
        fluid_velocity: Velocity of fluid flowing through pipe in m/s.
    
    Returns:
        The Reynolds number (unitless).
    """
    return (WATER_DENSITY * hydraulic_diameter * fluid_velocity) / \
           WATER_DYNAMIC_VISCOSITY


def pressure_loss_from_pipe_reduction(larger_diameter, fluid_velocity,
                                      reynolds_number, smaller_diameter):
    """Calculate the pressure loss from a pipe diameter reduction.
    
    Args:
        larger_diameter: Diameter of the larger pipe in meters.
        fluid_velocity: Velocity of fluid flowing through pipe in m/s.
        reynolds_number: Reynolds number for the flow (unitless).
        smaller_diameter: Diameter of the smaller pipe in meters.
    
    Returns:
        The pressure loss in kilopascals.
    """
    k = (.1 + 50 / reynolds_number) * \
        ((larger_diameter / smaller_diameter) ** 4 - 1)
    return -k * WATER_DENSITY * fluid_velocity ** 2 / 2000


def convert_kpa_to_psi(kpa):
    """Convert pressure from kilopascals to pounds per square inch.
    
    Args:
        kpa: Pressure in kilopascals.
    
    Returns:
        Pressure converted to psi.
    """
    return kpa * 0.145038


if __name__ == "__main__":
    main()
