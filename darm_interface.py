
import rospy

scale = 0.1
min_z = 0.1
max_z = 1.0
min_x = -0.1
max_x = 0.5
min_y = -0.5
max_y = 0.5

def check_bounds(pose):
	if pose.position.x < min_x:
		print("[Decon]: X less than minX...")
		return False
	if pose.position.x > max_x:
		print("[Decon]: X greater than maxX...")
		return False
	if pose.position.y < min_y:
		print("[Decon]: y less than minY...")
		return False
	if pose.position.y > max_y:
		print("[Decon]: y greater than maxY...")
		return False
	if pose.position.z < min_z:
		print("[Decon]: z less than minZ...")
		return False
	if pose.position.z > max_z:
		print("[Decon]: z greater than maxZ...")
		return False
	return True

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
	if not check_bounds(wpose):
		return
	move_to_pose(group, rate, [wpose])
        rate.sleep()

def dec_z(group, rate):
	rospy.loginfo("[Decon] Decrease ARM's z...")
	wpose = group.get_current_pose().pose
	wpose.position.z -= scale
	wpose.orientation.w = 1
	if not check_bounds(wpose):
		return
	move_to_pose(group, rate, [wpose])
	rate.sleep()

def inc_x(group, rate):
	rospy.loginfo("[Decon] Increase ARM's x...")
        wpose = group.get_current_pose().pose
        wpose.position.x += scale
	wpose.position.z += 0.015
 	wpose.orientation.w = 1
	if not check_bounds(wpose):
		return
        move_to_pose(group, rate, [wpose])
	rate.sleep()

def dec_x(group, rate):
	rospy.loginfo("[Decon] Decrease ARM's x...")
        wpose = group.get_current_pose().pose
        wpose.position.x -= scale
	wpose.position.z += 0.007
        wpose.orientation.w = 1
	if not check_bounds(wpose):
		return
        move_to_pose(group, rate, [wpose])
	rate.sleep()

def inc_y(group, rate):
	rospy.loginfo("[Decon] Increase ARM's y...")
        wpose = group.get_current_pose().pose
        wpose.position.y += scale
        wpose.orientation.w = 1
	if not check_bounds(wpose):
		return
        move_to_pose(group, rate, [wpose])
	rate.sleep()

def dec_y(group, rate):
	rospy.loginfo("[Decon] Decrease ARM's y...")
        wpose = group.get_current_pose().pose
        wpose.position.y -= scale
        wpose.orientation.w = 1
	if not check_bounds(wpose):
		return
        move_to_pose(group, rate, [wpose])
	rate.sleep()

def move(group, rate, x_offset, y_offset, z_offset):
	
	#Z offset
	while z_offset >= scale:
		inc_z(group, rate)
		z_offset -= scale
	while z_offset*-1 >= scale:
		dec_z(group, rate)
		z_offset += scale
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

	
