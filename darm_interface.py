import rospy

scale = 0.1

def move_to_pose(group, rate, waypoints):
	(plan, fraction) = group.compute_cartesian_path(waypoints, 0.01, 0.0)
        group.execute(plan, wait=True)
	group.stop()
	group.clear_pose_targets()
	rate.sleep()

def inc_z(group, rate):
	rospy.loginfo("[Decon] Increase ARM's z...")
	wpose = group.get_current_pose().pose
        wpose.position.z += scale
	wpose.orientation.w = 1
	move_to_pose(group, rate, [wpose])
        rate.sleep()

def dec_z(group, rate):
	rospy.loginfo("[Decon] Decrease ARM's z...")
	wpose = group.get_current_pose().pose
	wpose.position.z -= scale
	wpose.orientation.w = 1
	move_to_pose(group, rate, [wpose])
	rate.sleep()

def inc_x(group, rate):
	rospy.loginfo("[Decon] Increase ARM's x...")
        wpose = group.get_current_pose().pose
        wpose.position.x += scale
 	wpose.orientation.w = 1
        move_to_pose(group, rate, [wpose])
	rate.sleep()

def dec_x(group, rate):
	rospy.loginfo("[Decon] Decrease ARM's x...")
        wpose = group.get_current_pose().pose
        wpose.position.x -= scale
        wpose.orientation.w = 1
        move_to_pose(group, rate, [wpose])
	rate.sleep()

def inc_y(group, rate):
	rospy.loginfo("[Decon] Increase ARM's y...")
        wpose = group.get_current_pose().pose
        wpose.position.y += scale
        wpose.orientation.w = 1
        move_to_pose(group, rate, [wpose])
	rate.sleep()

def dec_y(group, rate):
	rospy.loginfo("[Decon] Decrease ARM's y...")
        wpose = group.get_current_pose().pose
        wpose.position.y -= scale
        wpose.orientation.w = 1
        move_to_pose(group, rate, [wpose])
	rate.sleep()

def move(group, rate, x_offset, y_offset, z_offset):
	
	#X offset
	while x_offset >= scale:
		inc_x(group, rate)
		x_offset -= scale
	while x_offset*-1 >= scale:
		dec_x(group, rate)
		x_offset += scale
	#Y offset
	while y_offset >= scale:
		inc_y(group, rate)
		y_offset -= scale
	while y_offset*-1 >= scale:
		dec_y(group, rate)
		y_offset += scale
	#Z offset
	while z_offset >= scale:
		inc_z(group, rate)
		z_offset -= scale
	while z_offset*-1 >= scale:
		dec_z(group, rate)
		z_offset += scale
	
