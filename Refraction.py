import pygame
import math

#screen setting
WIDTH,HEIGHT=800,600
screen= pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Refraction Simulation")
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW=(255,255,0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
VIOLET=(255,0,255)
ORANGE = (255, 165, 0)
ray_origin = (100, 100)
boundary_y = HEIGHT // 2



# Function to draw an arrow in the middle of a line
def draw_arrow_middle(surface, color, start_pos, end_pos, arrow_size=10):
    mid_pos = ((start_pos[0] + end_pos[0]) / 2, (start_pos[1] + end_pos[1]) / 2)
    angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
    pygame.draw.line(surface, color, start_pos, end_pos, 2)
    left_arrow = (
        mid_pos[0] - arrow_size * math.cos(angle - math.pi / 6),
        mid_pos[1] - arrow_size * math.sin(angle - math.pi / 6),
    )
    right_arrow = (
        mid_pos[0] - arrow_size * math.cos(angle + math.pi / 6),
        mid_pos[1] - arrow_size * math.sin(angle + math.pi / 6),
    )
    pygame.draw.polygon(surface, color, [mid_pos, left_arrow, right_arrow])

# Function to calculate the refraction angle
def calculate_refraction_angle(n1, n2, angle_of_incidence):
    theta1_rad = math.radians(angle_of_incidence)
    try:
        theta2_rad = math.asin((n1 / n2) * math.sin(theta1_rad))
        return math.degrees(theta2_rad)
    except ValueError:
        return None
        
def get_refraction():
    
    # Menu for selecting the scenario
    print("Choose a refraction scenario:")
    print("1. Rarer to Denser")
    print("2. Denser to Rarer")
    choice = input("Enter 1 or 2: ")

    def get_refractive_indices():

        n1 = float(input("Enter the refractive index of Medium 1: "))
        n2 = float(input("Enter the refractive index of Medium 2: "))
        
        if choice == "1" and n1 >= n2:
            print("Error: For 'Rarer to Denser,' Medium 1 should have a lower refractive index than Medium 2.")
        elif choice == "2" and n1 <= n2:
            print("Error: For 'Denser to Rarer,' Medium 1 should have a higher refractive index than Medium 2.")
        else:
            return n1, n2

        print("Please re-enter the refractive indices.")
        return get_refractive_indices()

    n1, n2 = get_refractive_indices()
    angle_of_incidence = float(input("Enter the angle of incidence in degrees: "))

    label_incident, label_refracted = ("Rarer", "Denser") if choice == "1" else ("Denser", "Rarer")

    pygame.init()
    font = pygame.font.Font(None, 24)

    #normal dotted line
    clock = pygame.time.Clock()
    dot_radius = 2
    spacing =2
    normal_x=300
    start_pos = (normal_x,boundary_y - 150 )  # Start at the left middle of the window
    end_pos = (normal_x,boundary_y + 150)
    distance = math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
    angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])


    # Calculate the refraction angle
    angle_of_refraction = (calculate_refraction_angle(n1, n2, angle_of_incidence))

    ## Position for labels on the right side of the screen
    label_incident_pos = (WIDTH - 70, boundary_y - 50)
    label_refracted_pos = (WIDTH - 70, boundary_y + 20)

    #main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(WHITE)

        # Draw interface line (boundary between media)
        pygame.draw.line(screen, BLUE, (0, boundary_y), (WIDTH, boundary_y), 2)
        interface_text = font.render("Interface", True, BLACK)
        screen.blit(interface_text, (WIDTH // 2 - 40, boundary_y + 10))

        # write normal line
        pygame.draw.line(screen, GRAY, start_pos, end_pos, 1)
        normal_text = font.render("Normal", True, BLACK)
        screen.blit(normal_text, (normal_x - 20, boundary_y - 180))

        pygame.draw.line(screen, BLUE, (0, boundary_y),(WIDTH, boundary_y),2)
        for i in range(int(distance / (dot_radius * 2 + spacing))):
            dot_x = start_pos[0] + i * (dot_radius * 2 + spacing) * math.cos(angle)
            dot_y = start_pos[1] + i * (dot_radius * 2 + spacing) * math.sin(angle)
            pygame.draw.circle(screen, RED, (int(dot_x), int(dot_y)), dot_radius)

        #incident ray drawing
        incident_ray_length = 250
        incidence_x = WIDTH // 2 - incident_ray_length * math.sin(math.radians(angle_of_incidence))
        incidence_y = HEIGHT // 2 - incident_ray_length * math.cos(math.radians(angle_of_incidence))
        

    ##    # The incident ray should land on the boundary at boundary_y
        incident_ray_end =(normal_x, boundary_y)  # Align with the normal line for intersection
        
        
        # Display refractive indices and details on the simulation
        details_text = [
            f"Refractive Index of Medium 1 (n1): {n1}",
            f"Angle of Incidence:{angle_of_incidence}°",
        ]
        for i, text in enumerate(details_text):
            line_text = font.render(text, True, BLACK)
            screen.blit(line_text, (5,5 + i * 20))

        # Draw labels for rarer and denser media on the right side of the screen
        incident_label = font.render(label_incident, True, BLACK)
        refracted_label = font.render(label_refracted, True, BLACK)
        screen.blit(incident_label, label_incident_pos)
        screen.blit(refracted_label, label_refracted_pos)

        if angle_of_refraction is not None:
            
            if math.radians(angle_of_incidence) == math.radians(0) :
                deviation_text = font.render("NO DEVIATION", True, VIOLET)
                screen.blit(deviation_text, (incident_ray_end[0] + 150, incident_ray_end[1] - 50))
                details_text2 = [
                    f"Refractive Index of Medium 2 (n2): {n2}",
                    f"Angle of Refraction:{round(angle_of_refraction), 0}°" 
                ]
                for i, text in enumerate(details_text2):
                        line_text = font.render(text, True, BLACK)
                        screen.blit(line_text, (500,5 + i * 20))
                        pygame.draw.line(screen, YELLOW, (normal_x, boundary_y+300),(HEIGHT//2, boundary_y), 2)
                refracted_ray_length = 250
                refracted_ray_start = (incident_ray_end[0], boundary_y)
                refracted_ray_end = (
                                        refracted_ray_start[0] + refracted_ray_length * math.sin(math.radians(angle_of_refraction)),
                                            refracted_ray_start[1] + refracted_ray_length * math.cos(math.radians(angle_of_refraction))
                                    )
                draw_arrow_middle(screen, ORANGE, refracted_ray_start, refracted_ray_end)
                
                incident_ray_start= ( normal_x , HEIGHT //10 )
                incident_ray_end=( normal_x,
                                    boundary_y)
                draw_arrow_middle(screen, GREEN, incident_ray_start, incident_ray_end)             
            elif math.radians(angle_of_incidence) == math.radians(90) :
                    deviation_text = font.render("NO DEVIATION", True, VIOLET)
                    screen.blit(deviation_text, (incident_ray_end[0] + 150, incident_ray_end[1] - 50))
                    details_text2 = [
                    f"Refractive Index of Medium 2 (n2): {n2}",
                    f"Angle of Refraction:90°" 
                    ]
                    for i, text in enumerate(details_text2):
                        line_text = font.render(text, True, BLACK)
                        screen.blit(line_text, (500,5 + i * 20))
                        pygame.draw.line(screen, YELLOW, (normal_x, boundary_y),(WIDTH-150, boundary_y), 2)
                    refracted_ray_start=(normal_x, boundary_y)
                    refracted_ray_end= ( WIDTH - 150, boundary_y)
                    draw_arrow_middle(screen, ORANGE, refracted_ray_start, refracted_ray_end)
                    
                    incident_ray_start= (50, boundary_y)
                    incident_ray_end=(normal_x, WIDTH // 3 +35)
                    draw_arrow_middle(screen, GREEN, incident_ray_start, incident_ray_end)  
            else:
                # Draw incident ray
                pygame.draw.line(screen, GREEN, (incidence_x-100, incidence_y ), (WIDTH //2 - 100, HEIGHT //2 ), 2)
                draw_arrow_middle(screen, GREEN, (incidence_x-100, incidence_y ), (WIDTH //2 - 100, HEIGHT //2 ))
                
    
                refracted_ray_length = 300
                refracted_ray_start = (incident_ray_end[0], boundary_y)
                refracted_ray_end = (
                    refracted_ray_start[0] + refracted_ray_length * math.sin(math.radians(angle_of_refraction)),
                        refracted_ray_start[1] + refracted_ray_length * math.cos(math.radians(angle_of_refraction))
                )
                details_text2 = [
                    f"Refractive Index of Medium 2 (n2): {n2}",
                    f"Angle of Refraction:{angle_of_refraction}°" 
                ]
                for i, text in enumerate(details_text2):
                        line_text = font.render(text, True, BLACK)
                        screen.blit(line_text, (500,5 + i * 20))
                pygame.draw.line(screen, YELLOW, refracted_ray_start, refracted_ray_end, 2)
                draw_arrow_middle(screen, ORANGE, refracted_ray_start, refracted_ray_end)
        else:
            if math.radians(angle_of_incidence) == math.radians(0) :
                deviation_text = font.render("NO DEVIATION", True, VIOLET)
                screen.blit(deviation_text, (incident_ray_end[0] + 150, incident_ray_end[1] - 50))
                details_text2 = [
                    f"Refractive Index of Medium 2 (n2): {n2}",
                    f"Angle of Refraction:{angle_of_refraction}°" 
                ]
                for i, text in enumerate(details_text2):
                        line_text = font.render(text, True, BLACK)
                        screen.blit(line_text, (500,5 + i * 20))
                        pygame.draw.line(screen, YELLOW, (normal_x, boundary_y+300),(HEIGHT//2, boundary_y), 2)
                refracted_ray_length = 300
                refracted_ray_start = (incident_ray_end[0], boundary_y)
                refracted_ray_end = (
                                        refracted_ray_start[0] + refracted_ray_length * math.sin(math.radians(angle_of_refraction)) ,
                                        refracted_ray_start[1] + refracted_ray_length * math.cos(math.radians(angle_of_refraction))
                                    )
                draw_arrow_middle(screen, ORANGE, refracted_ray_start, refracted_ray_end)
                            
                incident_ray_start= ( normal_x , HEIGHT //10 )
                incident_ray_end=( normal_x,
                                    boundary_y)
                draw_arrow_middle(screen, GREEN, incident_ray_start, incident_ray_end)       
            elif math.radians(angle_of_incidence) == math.radians(90) :
                    deviation_text = font.render("NO DEVIATION", True, VIOLET)
                    screen.blit(deviation_text, (incident_ray_end[0] + 150, incident_ray_end[1] - 50))
                    details_text2 = [
                    f"Refractive Index of Medium 2 (n2): {n2}",
                    f"Angle of Refraction:90°" 
                    ]
                    for i, text in enumerate(details_text2):
                        line_text = font.render(text, True, BLACK)
                        screen.blit(line_text, (500,5 + i * 20))
                        pygame.draw.line(screen, YELLOW, (normal_x, boundary_y),(WIDTH-150, boundary_y), 2)
                    refracted_ray_start=(normal_x, boundary_y)
                    refracted_ray_end= ( WIDTH - 150, boundary_y)
                    draw_arrow_middle(screen, ORANGE, refracted_ray_start, refracted_ray_end)
                    
                    incident_ray_start= (50, boundary_y)
                    incident_ray_end=(normal_x, WIDTH // 3 +35)
                    draw_arrow_middle(screen, GREEN, incident_ray_start, incident_ray_end) 
            else:
                # Draw incident ray
                pygame.draw.line(screen, GREEN, (incidence_x-100, incidence_y ), (WIDTH //2 - 100, HEIGHT //2 ), 2)
                draw_arrow_middle(screen, GREEN, (incidence_x-100, incidence_y ), (WIDTH //2 - 100, HEIGHT //2 ))

                reflection_text = font.render("Total Internal Reflection", True, VIOLET)
                screen.blit(reflection_text, (incident_ray_end[0]+150, incident_ray_end[1] - 50))

                # Draw reflected ray
                reflected_ray_length = 300
                reflected_ray_start = (normal_x, boundary_y)
                reflected_ray_end = (
                    incident_ray_end[0] + reflected_ray_length * math.sin(math.radians(angle_of_incidence)),
                    incident_ray_end[1] - reflected_ray_length * math.cos(math.radians(angle_of_incidence))
                    )
                
                pygame.draw.line(screen, YELLOW, reflected_ray_start, reflected_ray_end, 2)
                
                details_text2 = [
                    f"Refractive Index of Medium 2 (n2): {n2}",
                    f"Angle of Refraction:{angle_of_incidence}°" 
                ]
                for i, text in enumerate(details_text2):
                        line_text = font.render(text, True, BLACK)
                        screen.blit(line_text, (500,5 + i * 20))
                draw_arrow_middle(screen, ORANGE, reflected_ray_start, reflected_ray_end)
                
    ##        draw_arrow_middle(screen, ORANGE, refracted_ray_start, refracted_ray_end)
    
        pygame.display.flip()

    #pygame.quit()
