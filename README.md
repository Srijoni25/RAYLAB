# RAYLAB
“Python simulator for light reflection and refraction with ray diagrams, Snell’s law, and total internal reflection.”
it is a Python simulator that demonstrates how light behaves when it reflects off a surface and refracts between two media. A menu lets you choose Reflection or Refraction. Reflection draws ray diagrams with Turtle, plots incident vs. reflected angles with Matplotlib, and saves the data to a CSV file. Refraction calculates angles with Snell’s law, handles total internal reflection, and animates the rays with Pygame.

## REQUIREMENTS

pygame, matplotlib, pandas

Install them with: pip install pygame matplotlib pandas

## HOW TO RUN

python Main.py

## PROJECT FILES
- **Main.py**: the entry point. It shows a menu where you choose Reflection (A), Refraction (B), or Quit (Q) and runs the matching module.
- **Reflection.py**: takes five incident angles, draws the incident and reflected rays with Turtle, plots incident vs. reflected angles with Matplotlib, and saves the data to a CSV file with Pandas.
- **Refraction.py**: takes the refractive indices of two media and an angle of incidence, calculates the refraction angle with Snell's law, handles total internal reflection, and animates the rays with Pygame.
- **Light_Exp.csv**: a sample output file with the incident and reflected angles from a run of the reflection mode. It's regenerated (overwritten) each time you run Reflection.

## FUTURE WORK: Diffraction
