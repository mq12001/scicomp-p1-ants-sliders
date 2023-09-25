# Ants-Sliders Project for Scientific Computing
#### Meredith Alley
Fall 2023

In this project, we were instructed to read and attempt to replicate the findings of "Modelling the Formation of Trail Networks by Foraging Ants", a paper from 1993 by James Watmough and Leah Edelstein-Keshet. 

Some example images from that paper include:

![image](https://github.com/olincollege/scicomp-p1-ants-sliders/assets/95325894/5514fad4-e492-4c50-a02b-5a72f632a8a7)
![image](https://github.com/olincollege/scicomp-p1-ants-sliders/assets/95325894/db687abc-9007-4d1e-af98-5141c3b6ff0d)
![image](https://github.com/olincollege/scicomp-p1-ants-sliders/assets/95325894/fe56df71-83b2-4cc0-a5af-b75132de4f26)
![image](https://github.com/olincollege/scicomp-p1-ants-sliders/assets/95325894/f41ad7b0-1d6c-4c78-8112-74c874dfd6c0)

## For those that have read the paper
If you haven't read this paper or don't have previous knowledge of this project, you may find the "General Description" section more helpful.

In creating my model, I made a few essential deviations from what is described in the original paper.

### Model Differences

First, I did away with the idea of the turning kernel. One of the turning methods they used in the paper resembled a normal distribution, and I wanted to make turning adjustable. So, instead of writing prescriptive "turning kernels", I made the ants' random decision making fall into a normal distribution, with rounding that ensures that as the ironically-named "turning_kernel" variable increases (by user control), so does the ants' inclination to go forward.

```
self.velocity = round(
                self.velocity + np.random.normal(scale=turning_kernel)) % 8
```

Second, I didn't implement the forking algorithms described in the paper. By restricting my ants' pheromone sensors to the areas in front of and beside them (and not behind), I found that the situation in which a forking algorithm would be necessary is an edge case, and my non-implementation didn't visibly affect the output pathways of my ants.

Third (as mentioned above), I restricted my ants' sensors to the five directions that could be said to be 'in front' of them, rather than the three that could be said to be 'behind'. Ants can still explore behind themselves (in the very rare case that their normally distributed wandering would allow), but I found this to be a very elegant solution to the issue of ants backtracking or getting trapped in a small cluster.

```
for angle in [0, 1, 7, 6, 2]:  # Only checking these 5 directions
            # Check angle relative to whole grid instead of to the individual ant
            checked_angle = (self.velocity+angle) % 8
```

Fourth, I wrapped the edges of my simulation, effectively creating an infinite plane/torus for my ants to navigate. I found that as the simulation went on, it led to different results, but I was interested in what a simulation like this would look like when reaching equilibrium with a set amount of agents generated at the beginning, rather than a set number that are continuously generated in the model as others ran off of the edges and were removed.

### Visual Differences
First, I represented both the pheromone trails and the actual ants, where the paper only made the pheromone trails with a strength of 2 or more visible. I was using the package pygame and found it didn't slow the processing time immensely or confuse the visuals.

Second, I added some color! Below, see images of my implementation, with various initial conditions:


![image](https://github.com/olincollege/scicomp-p1-ants-sliders/assets/95325894/67ed7ea6-7f48-48dc-b3ba-93ad99a537fd)
![image](https://github.com/olincollege/scicomp-p1-ants-sliders/assets/95325894/4e786b2f-23cf-444f-8c5c-5f92a1f4dbbb)
![image](https://github.com/olincollege/scicomp-p1-ants-sliders/assets/95325894/46de6d7d-e916-4b9a-941a-8600c8db5f34)
![image](https://github.com/olincollege/scicomp-p1-ants-sliders/assets/95325894/9bf8b642-7bc9-400c-8dce-84a4676f1338)







## General Description
