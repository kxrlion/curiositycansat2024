import smbus
import time

# LSM9DS1 I2C address
LSM9DS1_ADDRESS = 0x1E

# LSM9DS1 registers
WHO_AM_I_REG = 0x0F
CTRL_REG1_XL = 0x10
CTRL_REG6_XL = 0x20
CTRL_REG1_M = 0x20
CTRL_REG4_M = 0x23
OUT_X_L_XL = 0x28
OUT_Y_L_XL = 0x2A
OUT_Z_L_XL = 0x2C
OUT_X_L_M = 0x28
OUT_Y_L_M = 0x2A
OUT_Z_L_M = 0x2C

# Create a smbus object
bus = smbus.SMBus(1)  # Use 1 for Raspberry Pi Model 3 and 4, 0 for Model 1 and 2

def read_byte(reg):
    try:
        return bus.read_byte_data(LSM9DS1_ADDRESS, reg)
    except IOError as e:
        print(f"I/O error during read operation: {e}")
        return None

def read_word(reg):
    try:
        low = bus.read_byte_data(LSM9DS1_ADDRESS, reg)
        high = bus.read_byte_data(LSM9DS1_ADDRESS, reg + 1)
        return (high << 😎 | low
    except IOError as e:
        print(f"I/O error during read operation: {e}")
        return None

def write_byte(reg, value):
    try:
        bus.write_byte_data(LSM9DS1_ADDRESS, reg, value)
    except IOError as e:
        print(f"I/O error during write operation: {e}")

def init_lsm9ds1():
    # Check the WHO_AM_I register to confirm communication with the sensor
    who_am_i = read_byte(WHO_AM_I_REG)
    if who_am_i != 0x68:
        raise Exception("LSM9DS1 not found on I2C bus")

    # Configure the accelerometer (XL) with 100 Hz data rate and ±2g scale
    write_byte(CTRL_REG1_XL, 0x50)

    # Configure the gyroscope with 238 Hz data rate and ±245 dps scale
    write_byte(CTRL_REG6_XL, 0x00)

    # Configure the magnetometer with continuous mode and high-performance mode
    write_byte(CTRL_REG1_M, 0x7C)
    write_byte(CTRL_REG4_M, 0x00)

def read_acceleration():
    x = read_word(OUT_X_L_XL)
    y = read_word(OUT_Y_L_XL)
    z = read_word(OUT_Z_L_XL)

    if x is not None and y is not None and z is not None:
        # Convert raw values to acceleration in g
        x_g = x / 16384.0
        y_g = y / 16384.0
        z_g = z / 16384.0
        return x_g, y_g, z_g
    else:
        return None

def read_magnetic_field():
    x = read_word(OUT_X_L_M)
    y = read_word(OUT_Y_L_M)
    z = read_word(OUT_Z_L_M)

    if x is not None and y is not None and z is not None:
        # Convert raw values to magnetic field strength in gauss
        x_m = x * 0.00014  # 0.00014 gauss/LSB for the default scale (+/- 4 gauss)
        y_m = y * 0.00014
        z_m = z * 0.00014
        return x_m, y_m, z_m
    else:
        return None

if _name_ == "_main_":
    try:
        init_lsm9ds1()

        while True:
            acceleration = read_acceleration()
            magnetic_field = read_magnetic_field()

            if acceleration is not None:
                print(f"Acceleration (g): X={acceleration[0]:.3f}, Y={acceleration[1]:.3f}, Z={acceleration[2]:.3f}")
            
            if magnetic_field is not None:
                print(f"Magnetic Field (gauss): X={magnetic_field[0]:.3f}, Y={magnetic_field[1]:.3f}, Z={magnetic_field[2]:.3f}")

            time.sleep(1)

    except KeyboardInterrupt:
        print("Program terminated by user.")
    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Cleanup
        bus.close()
