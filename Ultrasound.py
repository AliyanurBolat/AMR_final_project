import smbus2 as smbus
import time

class Ultrasound:
    # I2C address and register definitions
    ULTRASOUND_I2C_ADDR = 0x77
    
    # Registers
    DISDENCE_L = 0    # Distance low byte (mm)
    DISDENCE_H = 1    # Distance high byte
    RGB_WORK_MODE = 2 # RGB mode (0: user mode, 1: breathing mode)
    
    # RGB1 color registers
    RGB1_R = 3
    RGB1_G = 4
    RGB1_B = 5
    
    # RGB2 color registers
    RGB2_R = 6
    RGB2_G = 7
    RGB2_B = 8
    
    # RGB1 breathing cycle registers
    RGB1_R_BREATHING_CYCLE = 9
    RGB1_G_BREATHING_CYCLE = 10
    RGB1_B_BREATHING_CYCLE = 11
    
    # RGB2 breathing cycle registers
    RGB2_R_BREATHING_CYCLE = 12
    RGB2_G_BREATHING_CYCLE = 13
    RGB2_B_BREATHING_CYCLE = 14
    
    # RGB modes
    RGB_WORK_SIMPLE_MODE = 0
    RGB_WORK_BREATHING_MODE = 1
    
    def __init__(self, bus_number=1):
        """Initialize I2C bus"""
        self.bus = smbus.SMBus(bus_number)
    
    def write_byte(self, reg, value):
        """Write a single byte to the specified register"""
        try:
            self.bus.write_byte_data(self.ULTRASOUND_I2C_ADDR, reg, value)
            return True
        except Exception as e:
            print(f"I2C write error: {e}")
            return False
    
    def write_data_array(self, reg, data):
        """Write multiple bytes to consecutive registers"""
        try:
            self.bus.write_i2c_block_data(self.ULTRASOUND_I2C_ADDR, reg, data)
            return True
        except Exception as e:
            print(f"I2C block write error: {e}")
            return False
    
    def read_data_array(self, reg, length):
        """Read multiple bytes from consecutive registers"""
        try:
            return self.bus.read_i2c_block_data(self.ULTRASOUND_I2C_ADDR, reg, length)
        except Exception as e:
            print(f"I2C block read error: {e}")
            return []
    
    def set_breathing_mode(self, r1, g1, b1, r2, g2, b2):
        """
        Set RGB LEDs to breathing mode
        r1, g1, b1: RGB1 breathing periods (x100ms)
        r2, g2, b2: RGB2 breathing periods (x100ms)
        """
        # Set mode to breathing
        self.write_byte(self.RGB_WORK_MODE, self.RGB_WORK_BREATHING_MODE)
        
        # Set breathing cycles
        breathing_data = [r1, g1, b1, r2, g2, b2]
        self.write_data_array(self.RGB1_R_BREATHING_CYCLE, breathing_data)
    
    def set_color(self, r1, g1, b1, r2, g2, b2):
        """
        Set RGB LED colors
        r1, g1, b1: RGB1 color values (0-255)
        r2, g2, b2: RGB2 color values (0-255)
        """
        # Set mode to simple color
        self.write_byte(self.RGB_WORK_MODE, self.RGB_WORK_SIMPLE_MODE)
        
        # Set RGB values
        rgb_data = [r1, g1, b1, r2, g2, b2]
        self.write_data_array(self.RGB1_R, rgb_data)
    
    def get_distance(self):
        """Get distance in mm from the ultrasonic sensor"""
        try:
            # Read 2 bytes (low and high byte)
            data = self.read_data_array(self.DISDENCE_L, 2)
            if len(data) >= 2:
                # Combine bytes to get distance
                distance = (data[1] << 8) | data[0]
                return distance
            return 0
        except Exception as e:
            print(f"Error reading distance: {e}")
            return 0


# Example usage
if __name__ == "__main__":
    sensor = Ultrasound()
    
    try:
        # Set RGB LEDs to blue
        sensor.set_color(0, 0, 255, 0, 0, 255)
        print("RGB LEDs set to blue")
        
        # Continuous distance measurement
        print("Reading distance measurements. Press CTRL+C to exit.")
        
        while True:
            distance_mm = sensor.get_distance()
            distance_cm = distance_mm / 10.0
            
            print(f"Distance: {distance_mm} mm ({distance_cm:.1f} cm)")
            
            # Change LED colors based on distance
            if distance_mm < 200:  # Less than 20cm
                sensor.set_color(255, 0, 0, 255, 0, 0)  # Red
            elif distance_mm < 500:  # Less than 50cm
                sensor.set_color(255, 165, 0, 255, 165, 0)  # Orange
            else:
                sensor.set_color(0, 255, 0, 0, 255, 0)  # Green
                
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Turn off LEDs before exiting
        try:
            sensor.set_color(0, 0, 0, 0, 0, 0)
        except:
            pass