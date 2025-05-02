import RPi.GPIO as GPIO
import time

class DCMotorController:
    """
    A class to control DC motors using the DRV8833 motor driver via Raspberry Pi GPIO pins.
    
    This controller can run the motor forward, reverse, and stop it.
    Motor speed control can be implemented using PWM if needed.
    """
    
    def __init__(self, ain1_pin, ain2_pin, gpio_mode=GPIO.BCM):
        """
        Initialize the DC motor controller.
        
        Args:
            ain1_pin (int): GPIO pin connected to AIN1 on the DRV8833
            ain2_pin (int): GPIO pin connected to AIN2 on the DRV8833
            gpio_mode: GPIO pin numbering mode (GPIO.BCM or GPIO.BOARD)
        """
        # Store pin configurations
        self.ain1_pin = ain1_pin
        self.ain2_pin = ain2_pin
        
        # Initialize GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        
        # Setup motor control pins
        GPIO.setup(self.ain1_pin, GPIO.OUT)
        GPIO.setup(self.ain2_pin, GPIO.OUT)
        
        # Initialize pins to LOW (motor stopped)
        GPIO.output(self.ain1_pin, GPIO.LOW)
        GPIO.output(self.ain2_pin, GPIO.LOW)
        
        # Track motor state
        self.is_running = False
        self.direction = "stopped"  # "forward", "reverse", or "stopped"
        
    def forward(self, duration_sec=None):
        """
        Rotate the motor forward.
        
        Args:
            duration_sec (float, optional): Duration in seconds to run the motor.
                                          If None, the motor runs until stop() is called.
        
        Returns:
            bool: True if operation was successful
        """
        print(f"▶ Motor forward" + (f" for {duration_sec} sec." if duration_sec else ""))
        
        GPIO.output(self.ain1_pin, GPIO.HIGH)
        GPIO.output(self.ain2_pin, GPIO.LOW)
        
        self.is_running = True
        self.direction = "forward"
        
        if duration_sec is not None:
            time.sleep(duration_sec)
            self.stop()
            
        return True
    
    def reverse(self, duration_sec=None):
        """
        Rotate the motor in reverse.
        
        Args:
            duration_sec (float, optional): Duration in seconds to run the motor.
                                          If None, the motor runs until stop() is called.
        
        Returns:
            bool: True if operation was successful
        """
        print(f"◀ Motor reverse" + (f" for {duration_sec} sec." if duration_sec else ""))
        
        GPIO.output(self.ain1_pin, GPIO.LOW)
        GPIO.output(self.ain2_pin, GPIO.HIGH)
        
        self.is_running = True
        self.direction = "reverse"
        
        if duration_sec is not None:
            time.sleep(duration_sec)
            self.stop()
            
        return True
    
    def stop(self):
        """
        Stop the motor (both pins LOW).
        
        Returns:
            bool: True if operation was successful
        """
        GPIO.output(self.ain1_pin, GPIO.LOW)
        GPIO.output(self.ain2_pin, GPIO.LOW)
        
        self.is_running = False
        self.direction = "stopped"
        
        print("⏹ Motor stopped")
        return True
    
    def get_status(self):
        """
        Get the current status of the motor.
        
        Returns:
            dict: Dictionary containing motor status information
        """
        return {
            "running": self.is_running,
            "direction": self.direction,
            "ain1_pin": self.ain1_pin,
            "ain2_pin": self.ain2_pin
        }
    
    def cleanup(self):
        """
        Clean up GPIO resources.
        This should be called when the program exits.
        """
        self.stop()
        # Note: We don't call GPIO.cleanup() here to avoid affecting other GPIO users
        # The caller should decide when to do a full GPIO cleanup
    
    def __del__(self):
        """
        Destructor to ensure the motor is stopped when the object is destroyed.
        """
        try:
            self.stop()
        except:
            # Ignore errors during shutdown
            pass


# Example usage
if __name__ == "__main__":
    try:
        # Create motor with pins from the original code
        motor = DCMotorController(ain1_pin=15, ain2_pin=18)
        
        # Run a sequence of movements
        motor.forward(2)
        time.sleep(1)
        motor.reverse(2)
        time.sleep(1)
        
        # Get and print motor status
        status = motor.get_status()
        print(f"Motor status: {status}")
        
        # Ensure motor is stopped
        motor.stop()
        
    except KeyboardInterrupt:
        print("Program interrupted by user")
    finally:
        # Clean up - only use GPIO.cleanup() in the main program
        GPIO.cleanup()
