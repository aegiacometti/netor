Purpose of the project
======================

This is a very simple compilation of several OpenSource packages, which by using scripts
custom scripts help to start the journey of network automation and orchestration, without
having to learn from the very beginning how to configure all of them.

Because I think that this is the most important thing in the adoption of any new thing
... make it easier to start using them.

So, the scripts won't be nice, they are very simple and they work fine, in fact, they
are very easy to read. They catch some typing errors but pay attention when you write.
Anyway, do not worry, you won't break anything at this point.

The tools that integrate at the moment are:

- Ansible
- SaltStack
- TinyDB

As I move forward I will try to integrate other packages and functionalities.

But, remember, this project is only to help start using Ansible and SaltStack, in order
to see what you can get out of them, and after that, you should start learning about those two projects which are amazing.


Motivation
**********

After trying several network tools that claim to be essentials to networking, as you already
may know, there is no tool that will really work as you need, or even as they claim. They
may be useful for some tasks, but at some point, I always ended quitting after hours of trying
and talking with the official support. Every tool is beautiful in the PPTs and demos, but
then when you deploy it is when the adventure starts.

Having real support from providers is so slow and even sometimes you don't have time to wait
and you do it on your own. (THIS TOOL WILL NOT BE DIFFERENT, but at least is fun to learn
and develop in an OpenSource environment) :)

A couple of years ago I started to learn Python and I love it, I used it to create a couple
of scripts that helped me a lot to support several network-related projects deployments.

Later on, I learned about Ansible and it was "wow" I really love this!

In the path of learning network automation and orchestration with Ansible and SaltStack,
I found my self having to configure different files in different locations and in a
completely different manner. There are great tutorials on how to lear and use them, but
nothing to help you to integrate them, in order to make it easier to start "playing".

Because to be honest, both Ansible and SaltStack are great. Ansible is simple to start using
it for simple things, but SaltStack from my point of view is incredible, has similar functions
and a lot of very cool capabilities but it is very hard to start using it.

So, as I love to learn and to build things, I decided to start this adventure of learning
and develop a personal tool using Python, in an OpenSource manner.


Limitations
***********

* Tested on Linux and macOS. Don't support Windows, since Ansible and SaltStack do not support them.
* Only supports Python 3.
* If you change you ``netor_home_directory`` you have to update the PATH environment variable in order to look for the scripts in the correct folder.


Thank you notes
***************

These passionate individuals that are always there to help, teach and guide us.

* Python3 for network engineers: with Kirk's online trainings I started this journey of learning Python, with network orientation: Kirk Byers <ktbyers@twb-tech.com>
* NAPALM: David Barroso dbarrosop@dravetech.com, Mircea Ulinic ping@mirceaulinic.net, and Kirk Byers ktbyers@twb-tech.com
* TinyDB: Markus Siemens markus@m-siemens.de
* Ansible and SaltStack teams
* OpenSource community in general
