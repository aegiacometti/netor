Purpose of the project
======================

This is a very simple compilation of several OpenSource packages, which by using scripts
custom scripts help to start the journey of network automation and orchestration, without
having to learn from the very beginning how to configure all of them.

Because i think that this is the most important thing in the adoption of any new thing
... make it easier to start using them.

So, they scripts won't be nice, they are very simple and they work fine, in fact, they
 are very easy to read. They catch some typing errors, but pay attention when you write.
  Anyway, do not worry, you won't break anything at this point.

The tools that integrates at the moment are:

- Ansible
- SaltStack
- TinyDB

As i move forward i will try to integrate other packages and functionalities.

But, remember, this project is only to help start using Ansible and SaltStack, in order
to see what you can get out of them, after you should start learning about those two
projects which are amazing.

Project code at https://github.com/aegiacometti/netor

Project documentation at https://readthedocs.org/projects/netor/


Motivation
**********

After trying several network tools that claim to be essentials to networking, as you already
may know, there is no tool that will really work as you need, or even as they claim. They
may be useful for some tasks, but at some point i always ended quiting after hours of trying
and talking with the official support. Every tool is beautiful in the PPTs and demos, but
then when you deploy it is when the adventure starts.

Having real support from providers is so slow and even sometimes you don't have time to wait
and you do it by your own. (THIS TOOL WILL NOT BE DIFFERENT, but at least is fun to learn
and develop in an OpenSource environment) :)

A couple of years ago i started to learn Python and i love it, i used it to create a couple
of scripts that helped my a lot to support several network related projects deployments.

Later on, i learnt about Ansible and it was "wow" i really love this!

In the path of learning network automation and orchestration with Ansible and SaltStack,
i found my self having to configure different files in different locations and in a
completely different manner. There are great tutorials on how to lear and use them, but
nothing to help you to integrate them, in order to make it easier to start "playing".

Because to be honest, both Ansible and SaltStack are great. Ansible is simple to start using
it for simple things, but SaltStack from my point of view is incredible, has similar functions
and a lot of very cool capabilities but it is very hard to start using it.

So, as i love to learn and to build things, i decided to start this adventure of learning
and develop a personal tool using Python, in an OpenSource manner.


Limitations
***********

* Only tested on Linux.
* If you change you ``netor_home_directory`` you have to update the PATH environment variable
in order to look for the scripts in the correct folder.


Thank you notes
***************

These passionate individuals that are always there to help, teach and gide us.

* NAPALM: David Barroso dbarrosop@dravetech.com, Mircea Ulinic ping@mirceaulinic.net and Kirk Byers ktbyers@twb-tech.com
* TinyDB: Markus Siemens markus@m-siemens.de
* OpenSource community in general


