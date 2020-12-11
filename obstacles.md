# Table of contents

* [General Overview](overview.md)
  * [Hider](hider.md)
  * [Seeker](seeker.md)
  * [Launch File](launch.md)
  * [Custom World](world.md)
* [Difficulties and Obstacles Overcome](obstacles.md)
  * [Bugs](bugs.md)
  * [Reflection](reflection.md)


## Obstacles, Pivots, and Achievments 

Given that this project was completed in a little over a month by two students, we faced a lot of obstacles and overcome them with creativity and brainstorming together. Our initial goal was to have both robots be autonomous, but halfway through, we were not sure whether we would succeed in this goal, and rather control the seeker via teleop. Thankfully, we got some much needed motivation, and we ended up succeeding all our our ambitions. 

## Making the world more advanced
We started out with a much simpler map when we were first developing the hider algorithm, which at the time only went one direction, and thus we could often predict where it would hide. We began to realize that the map needed to be more complex and larger in order to provide for more diversity in where the hider could and would hide. It would also just make the game more realistic and exciting. Mahima created a custom map that we are very proud of and that worked well for our purposes. If we were given more time, I'm sure we would advance the map and thus advance the algorithms. 

## Autonomous Seeker
With a little less than half of our time consumed by brainstorming ideas, making maps, and developing the hider algorithm, we were nervous we would not be able to write a functional autnomous seeker before the deadline. However, we perservered, and seeker is now a very strong autonomous algorithm. Once we had the openCV detection working, which we thought would be the hardest, we felt confident that if the seekers eyes are working, it would be an easy task to get it to find the seeker. We were wrong. A huge obstacle we faced was brainstorming just exactly how the seeker would find the hider. Finally, inspiration hit when we decided to think back to the game of hide and seek itself. In the seeker's position, you use your ears when your eyes are closed. For example, if you heard footsteps running behind you as the seeker, you wouldn't spend time searching every space in front of you, you would turn and search behind you. We translated this idea to the robot using lidar to generally "hear" which way the hider is going, then make an estimate of a direction to go in. Once we thought of this idea, our seeker functioned beautifully with the wall following and computer vision techniques. 

