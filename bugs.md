# Table of contents

* [General Overview](overview.md)
  * [Hider](hider.md)
  * [Seeker](seeker.md)
  * [Launch File](launch.md)
  * [Custom World](world.md)
* [Difficulties and Obstacles Overcome](obstacles.md)
  * [Bugs](bugs.md)
  * [Reflection](reflection.md)


## Bugs and Imperfect Behavior 

As with many robotics projects, not all behavior turns out perfectly 100% of the time. Though we did acheive great results, our program, like all others, is not perfect, and we would like to acknowledge that. 

### Hider does not always hide perfectly
At times, hider will not get to a great hiding place in time (meaning one where the seeker would have to extensively search using it's own wall following algorithm) before the seeker pivots and spots it with it's computer vision. To combat this, we ended up making seeker wait for longer, giving hider a bit more time to hide. 

### Bots get stuck while navigating the tricky environment with wall following
Another rare issue we noticed is that at strange angles that come up randomly, the bots would get stuck and could not wall follow. Once we reset the world, however, this issue went away and we got a good trial.

### The hider/seeker does not turn to the exact yaw
The only bug that is largely inexplicable is that sometimes the hider or seeker over or under turns when it is initially picking a direction to go in. I noticed that after resetting the model poses, sometimes the bots turn a little right after. Though this problem isn't so important, since both algorithms can make it around walls and obstacles, it is strange to see such unconsistent turning. 
