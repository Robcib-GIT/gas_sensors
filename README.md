# gas_sensors
 Documents related to the mechanical and fluid dynamics analysis for quadruped gas nose

 "gas_visualizer" is the ROS package for gas sensing and victims visualization in the map on RViz

 To run the ROS nodes:
 -rosrun gas_visualizer gas_markers_v2.py
 -rosrun gas_visualizer victims_marker.py

 Add in RViz the Markers:
 -marker_victima
 -marker_co2
 -marker_tvoc

 This visualization shows the processed information of the three sensors, for visualization of individual measurements, add the following markers in RViz:
 -marker_s1co2
 -marker_s1tvoc
 -marker_s2co2
 -marker_s2tvoc
 -marker_s3co2
 -marker_s3tvoc
 
 
