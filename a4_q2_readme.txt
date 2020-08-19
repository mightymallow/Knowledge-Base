I decided to build my KB around the domain of operating a vehicle. The atoms
are used as an indicator of what the vehicle has done since the start of the
program and the rules outline what requirements are in place to proceed with 
the inferred action (head atom in the rule statement). This way it is possible 
to learn how to operate a vehicle and see how it was used.

For example, we can use the command:
$ tell press_key open_door
$ infer_all

This command would infer that we have unlocked the vehicle and gotten in. After 
we are in the vehicle we can use the command to start the vehicle:
$ tell insert_key turn_ignition
$ infer_all

Again our KB would infer that the car has been started. Afterwards there are various atoms that can be input to infer new actions for the vehicle. A simple example would be to accelerate and then change lanes. This can be accomplished using the command:
$ tell gas_pedal turn_signal check_blindspot turn_wheel
$ infer_all

From that command the two head atoms (actions for our KB) that would be inferred are accelerate and change_lanes. Various atoms will result in new inferred actions 
that the car performs. Once a user is done using the KB to enter atoms, we can use the command "infer_all" to see what actions were inferred. Based on this we can see
if the car was ever raced, in an accident, overheated, or topped up with fuel!
