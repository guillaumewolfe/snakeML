# state_representation/state.py

def get_state(snake_positions, reward_position, frame_x, frame_y, frame_width, frame_height, cell_size):
    head_x, head_y = snake_positions[0]
    apple_x, apple_y = reward_position

    # Distances to walls
    distance_to_left_wall = head_x
    distance_to_right_wall = (frame_width // cell_size) - head_x - 1
    distance_to_top_wall = head_y
    distance_to_bottom_wall = (frame_height // cell_size) - head_y - 1

    # Distances to apple
    distance_to_apple_x = apple_x - head_x
    distance_to_apple_y = apple_y - head_y

    # Possible directions
    can_move_up = 1 if head_y > 0 else 0
    can_move_down = 1 if head_y < (frame_height // cell_size) - 1 else 0
    can_move_left = 1 if head_x > 0 else 0
    can_move_right = 1 if head_x < (frame_width // cell_size) - 1 else 0

    # Flattened positions of snake segments
    snake_body = []
    for segment in snake_positions[1:]:
        snake_body.extend([segment[0], segment[1]])

    # Create the state vector
    state = [
        head_x, head_y, apple_x, apple_y,
        distance_to_left_wall, distance_to_right_wall, distance_to_top_wall, distance_to_bottom_wall,
        distance_to_apple_x, distance_to_apple_y,
        can_move_up, can_move_down, can_move_left, can_move_right
    ] + snake_body

    return state
