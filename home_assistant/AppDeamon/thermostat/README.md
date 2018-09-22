Starting a project to code a PID controller in python for a thermostat. Might try and create a LQG controller but that'll require a case study.

Here are snippets of the different x.yaml files:

configuration.yaml

#Input Variables
input_number:
  command_setpoint:
    name: Boiler set point
    initial: 0
    min: 0
    max: 65
    step: 1
    unit_of_measurement: "°C"
    mode: box
  pid_kp:
    name: Kp
    min: 0
    max: 100
    step: 0.001
    mode: box
  pid_kd:
    name: Kd
    min: 0
    max: 100
    step: 0.001
    mode: box
  pid_ki:
    name: KI
    min: 0
    max: 100
    step: 0.001
    mode: box
  room_temp:
    name: Thermostat temperature
    min: 10
    max: 30
    step: 0.1
    initial: 10
  insulation_coeff:
    name: Heatloss coefficient
    min: 0
    max: 100
    step: 0.001
    mode: box
    
input_select:
  thermostat_mode:
    name: Thermostat Mode
    options:
      - "PID"
      - "Hysteresis"
      - "off"
    icon: mdi:target
    
    
 pid_thermostat:
  name: Thermostat
  entities:
    - input_number.pid_kd
    - input_number.pid_ki
    - input_number.pid_kp
    - input_number.insulation_coeff
    - sensor.Pterm
    - sensor.Iterm
    - sensor.Dterm
    - sensor.heating_error
    - sensor.heatloss
    - sensor.heating_output
    - sensor.boiler_water_temp
    - input_select.thermostat_mode
    - input_number.room_temp
    - sensor.temp_lvr
    
You'll need to go through and set the right temp input and outside temp input. If you don't have outside temp just set it to 0 and the heatloss coeff to 0.

This program doesn't yet calculate the PID variables, but sometime i'll add a function that can do it. This is the old way. 

The heatloss coeff is up to you to set. In the futur based on this : https://dsp.stackexchange.com/questions/16937/transfer-function-determination-from-input-and-output-data and https://github.com/espenhgn/mimopy.
