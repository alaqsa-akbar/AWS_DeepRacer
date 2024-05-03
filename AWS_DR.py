import math

class Reward():
    def __init__(self):
        self.reward = 0
        self.speed_reward = 0
        self.optimal_path_reward = 0
        self.max_speed = 3
        self.min_speed = 1.5
        self.progress_reward = 0
        self.TOTAL_STEPS = 300


    def get_optimal_path(self, params):
        '''
        Optimal path reward function
        '''

        # Getting the parameters
        waypoints = params['waypoints']
        closest_waypoints = params['closest_waypoints']
        x = params['x']
        y = params['y']
        heading = params['heading']

        waypoint = closest_waypoints[1] + 5
        if waypoint >= len(waypoints):
            waypoint %= len(waypoints)

        optimal_heading = math.degrees(math.atan2(waypoints[waypoint][1] - y, waypoints[waypoint][0] - x))
        diff = abs(heading - optimal_heading)
        if diff > 180:
            diff = 360 - diff
        
        return 10 - diff/18


    def get_optimal_speed(self, params):
        '''
        Optimal speed reward function
        '''
        closest_waypoints = params['closest_waypoints']
        waypoints = params['waypoints']

        waypoint_1 = closest_waypoints[1]
        waypoint_2 = closest_waypoints[1] + 5
        if waypoint_2 >= len(waypoints):
            waypoint_2 %= len(waypoints)
        
        angle_between = math.degrees(math.atan2(waypoints[waypoint_2][1] - waypoints[waypoint_1][1], waypoints[waypoint_2][0] - waypoints[waypoint_1][0]))
        if angle_between > 180:
            angle_between = 360 - angle_between

        return self.max_speed - angle_between * (self.max_speed - self.min_speed)/180

    def reward_function(self, params):    
        '''
        Reward function
        '''

        # If crashed
        if not params['all_wheels_on_track']:
            self.reward = 1e-3
            return self.reward

        # Parameters
        speed = params['speed']
        waypoints = params['closest_waypoints']
        progress = params['progress']
        steps = params['steps']


        # Slow down around crucial corners
        # if waypoints in list(range(26, 40)) or waypoints in list(range(78, 86)):
        #     if speed > 2:
        #         self.speed_reward = 0.1

        # Reward for speed, tries not to go below 1.5 m/s
        # self.speed_reward = max(0.1, 5*(speed-1.23)**3)
        optimal_speed = self.get_optimal_speed(params)
        speed_diff = abs(optimal_speed - speed)
        self.speed_reward = max(1e-3, math.exp(10*(0.3 - speed_diff)))

        # Optimal path reward
        self.optimal_path_reward = self.get_optimal_path(params)

        # Progress reward
        if steps % 100 == 0 and progress > (steps/self.TOTAL_STEPS) * 100:
            self.progress_reward += 5

        self.reward = self.speed_reward + self.optimal_path_reward + self.progress_reward

        return self.reward
    
reward = Reward()


# Define the main function
def reward_function(params):
    return float(reward.reward_function(params))