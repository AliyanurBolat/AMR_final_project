import time
import smbus
import sys
sys.path.append('/home/pi/TurboPi/')
import HiwonderSDK.mecanum as mecanum
import Ultrasound
import motor_controller_class

LINE_FOLLOWER_I2C_ADDR = 0x78

bus = smbus.SMBus(1)
chassis = mecanum.MecanumChassis()
up_motor = motor_controller_class.DCMotorController()

ultra = Ultrasound()
distance_sensor_enabled = True
object_detected = False

def wire_write_byte(val):
    try:
        bus.write_byte(LINE_FOLLOWER_I2C_ADDR, val)
        return True
    except Exception as e:
        print("I2C Write Error:", e)
        return False

def wire_read_data_byte(reg):
    try:
        wire_write_byte(reg)
        val = bus.read_byte(LINE_FOLLOWER_I2C_ADDR)
        return val
    except Exception as e:
        print("I2C Read Error:", e)
        return None

def move_forward():
    chassis.set_velocity(35, 90, 0)

def move_slight_forward(duration=0.4):
    chassis.set_velocity(35, 90, 0)
    time.sleep(duration)
    stop()

def stop():
    chassis.set_velocity(0, 0, 0)

def left():
    chassis.set_velocity(35, 110, 0)

def right():
    chassis.set_velocity(35, 20, 0)

def turn_left():
    chassis.set_velocity(35, 130, 0)

def turn_right():
    chassis.set_velocity(35, 30, 0)

def mini_left():
    chassis.set_velocity(35, 115, 0)

def mini_right():
    chassis.set_velocity(35, 15, 0)

def line_follow():
    data = wire_read_data_byte(1)
    if data is None:
        return None

    s1 = data & 0x01
    s2 = (data >> 1) & 0x01
    s3 = (data >> 2) & 0x01
    s4 = (data >> 3) & 0x01

    print(f"Sensors: {s1} {s2} {s3} {s4}")

    if s1 == 1 and s2 == 1 and s3 == 1 and s4 == 1:
        return 'stop'

    if s1 == 0 and s4 == 0 and s2 == 1 and s3 == 1:
        move_forward()
    elif s1 == 1 and s2 == 1 and s3 == 0 and s4 == 0:
        left()
    elif s4 == 1 and s3 == 1 and s2 == 0 and s1 == 0:
        right()
    elif s1 == 1 and s2 == 1 and s3 == 1 and s4 == 0:
        turn_left()
    elif s1 == 0 and s2 == 1 and s3 == 1 and s4 == 1:
        turn_right()
    elif s1 == 1 and s2 == 0 and s3 == 0 and s4 == 0:
        mini_left()
    elif s1 == 0 and s2 == 0 and s3 == 0 and s4 == 1:
        mini_right()
    else:
        stop()

    return 'ok'

def main():
    global distance_sensor_enabled, object_detected

    try:
        while True:
            if distance_sensor_enabled and not object_detected:
                distance_mm = ultra.get_distance()
                distance_cm = distance_mm / 10.0
                print(f"Distance: {distance_cm:.1f} cm")

                if distance_cm <= 4.0:
                    print("Object detected!")
                    object_detected = True
                    stop()
                    time.sleep(1)
                    move_slight_forward(0.5)
                    up_motor.forward(5)
                    distance_sensor_enabled = False

            result = line_follow()

            if result == 'stop':
                stop()
                up_motor.reverse(5)
                break

            time.sleep(0.1)

    except KeyboardInterrupt:
        stop()

if __name__ == "__main__":
    main()
