import turtle
import matplotlib.pyplot as plt
import pandas as pd
import math

# Function to draw an arrowhead in the middle of the ray
def draw_arrowhead(t, origin, end, midpoint, is_reflected=False):
    t.penup()
    t.goto(midpoint)  # Move to the midpoint of the ray
    if is_reflected:
        t.setheading(t.towards(end))  # Reverse direction for reflected ray
    else:
        t.setheading(t.towards(origin))  # Standard arrow direction
    t.right(150)
    t.pendown()
    t.forward(10)
    t.backward(10)
    t.left(300)
    t.forward(10)
    t.backward(10)
    t.setheading(0)  # Reset heading
 
# Function to label the angles near the rays
def label_angle(t, angle, position, label_type):
    t.penup()
    offset = 0  # Increased offset for better visibility
    if label_type == "Incident":
        t.goto(position[0] - offset, position[1] + offset)
        t.color("black")
        t.write(f"θ={angle}°", align="right", font=("Arial", 12, "normal"))
    elif label_type == "Reflected":
        t.goto(position[0] + offset, position[1] + offset)
        t.color("black")
        t.write(f"θ={angle}°", align="left", font=("Arial", 12, "normal"))
 
# Function to simulate reflection using Turtle
def reflection(angles):
    # Setup Turtle screen with increased size
    turtle.setup(650, 650)  # Increased width and height
    screen = turtle.Screen()
    screen.title("Reflection of Light")
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
 
    # Draw mirror (horizontal black line)
    t.penup()
    t.goto(-300, 0)  # Extended mirror length
    t.pendown()
    t.pensize(3)
    t.color("black")
    t.forward(600)  # Draw from (-450,0) to (450,0)
 
    # Draw normal (vertical blue line)
    t.penup()
    t.goto(0, -300)  # Extended normal length
    t.pendown()
    t.pensize(1)
    t.color("blue")
    t.goto(0, 300)  # Draw from (0,-350) to (0,350)
 
    # Label the normal
    t.penup()
    t.goto(-30, 300)
    t.color("blue")
    t.write("Normal", align="left", font=("Arial", 14, "normal"))
    t.goto(-300, 300)
    t.write("Incident", align="left", font=("Arial", 14, "normal"))
    t.goto(230, 300)
    t.write("Reflected", align="left", font=("Arial", 14, "normal"))
   
    # Define colors for different rays
    colors = ["red", "green", "purple", "orange", "brown"]
 
    # Length of the rays
    ray_length = 250  # Increased ray length for better visibility
 
    for i, angle in enumerate(angles):
        color = colors[i % len(colors)]  # Cycle through colors if more than 5 angles
 
        # Convert angle to radians
        theta_rad = math.radians(angle)
 
        # Calculate incident ray start point
        x_incident_start = -ray_length * math.cos(theta_rad)
        y_incident_start = ray_length * math.sin(theta_rad)
 
        # Calculate reflected ray end point
        x_reflected_end = ray_length * math.cos(theta_rad)
        y_reflected_end = ray_length * math.sin(theta_rad)
 
        # Draw incident ray from (x_incident_start, y_incident_start) to (0,0)
        t.penup()
        t.goto(x_incident_start, y_incident_start)
        t.pendown()
        t.color(color)
        t.goto(0, 0)  # Point of incidence
 
        # Calculate midpoint for the incident ray
        midpoint_incident = ((x_incident_start + 0) / 2, (y_incident_start + 0) / 2)
 
        # Draw arrowhead for incident ray in the middle
        draw_arrowhead(t, (0,0), (x_incident_start, y_incident_start), midpoint_incident)
 
        # Label angle for incident ray at the start
        label_angle(t, angle, (x_incident_start, y_incident_start), "Incident")
 
        # Draw reflected ray from (0,0) to (x_reflected_end, y_reflected_end)
        t.penup()
        t.goto(0, 0)
        t.pendown()
        t.color(color)
        t.goto(x_reflected_end, y_reflected_end)
 
        # Calculate midpoint for the reflected ray
        midpoint_reflected = ((0 + x_reflected_end) / 2, (0 + y_reflected_end) / 2)
 
        # Draw arrowhead for reflected ray in the middle (with reversed direction)
        draw_arrowhead(t, (0,0), (x_reflected_end, y_reflected_end), midpoint_reflected, is_reflected=True)
 
        # Label angle for reflected ray at the end
        label_angle(t, angle, (x_reflected_end, y_reflected_end), "Reflected")
 
    # Finish drawing
    screen.mainloop()
 
# Function to plot graph using Matplotlib
def plot_graph(data, title):
    plt.figure(figsize=(8,6))
    plt.plot(data['Incident Angle'], data['Reflected Angle'], marker='o', linestyle='-', color='blue')
    plt.title(title)
    plt.xlabel('Incident Angle (degrees)')
    plt.ylabel('Reflected Angle (degrees)')
    plt.xlim(0, 90)
    plt.ylim(0, 90)
    plt.xticks(range(0, 91, 10))
    plt.yticks(range(0, 91, 10))
    plt.grid(True)
    plt.show()
 
# Function to handle reflection data and save to CSV
def handle_reflection():
    try:
        # Input angles and ensure exactly 5 values
        input_angles = input("Enter 5 angles for incident rays (0° < θ < 90°) separated by commas: ")
        angles = [float(angle.strip()) for angle in input_angles.split(',')]
        if len(angles) != 5:
            print("Error: Please enter exactly 5 angles.")
            return
 
        # Validate angles (0 < angle < 90)
        for angle in angles:
            if angle <= 0 or angle >= 90:
                print("Error: Angles should be between 0° and 90°.")
                return
 
        # Draw reflection diagram
        reflection(angles)
 
        # Save data to CSV
        df = pd.DataFrame({
            'Incident Angle': angles,
            'Reflected Angle': angles  # Reflection has the same angle
        })
        df.to_csv('Light_Exp.csv', mode='w', index=False)  # 'w' mode to overwrite file
        print("Data saved to 'Light_Exp.csv'.")
 
        # Plot graph
        plot_graph(df, 'Reflection of Light: Incident vs. Reflected Angles')
 
    except ValueError:
        print("Error: Invalid input. Please enter numeric angles separated by commas.")
