====================
Smart-M3 experiences
====================


Smart-M3 platform and its concepts
==================================

The basic concepts of Smart-M3 were easy to learn, though this might be
tilted by the extensive tutorials given to us.  But the concept of RDF
triplets forming a network is simple enough.


Installation
============

The platform itself was tricky to install to say the least. There are several
modules that need to be compiled separately and in order. A single Makefile to
compile everything would have been nice. Also compilation is not as smooth in
Fedora as in Debian based distributions (Package dependencies were a bit
different; Python version was not detected correctly).  Compilation instructions
got better along the way.

Starting up the platform was also a bit difficult as there was no instructions
on how to do that.  Luckily there was a post on Smart-M3's Sourceforge forums
about this. Also there were some problems with D-Bus since we were using
Smart-M3 over SSH.  We found out that it tried to use the D-Bus over the SSH
instead of D-Bus on the server.  Still even now, running the system consists of
strange D-Bus incantations.  We are not sure whether they are optimal.  They
just work.


Knowledge processor programming
===============================

We adapted the ``kpwrapper`` interface developed by Eemeli Kantola in a very
early phase of programming.  Basically this brings a much simpler and pythonic
API than the one delivered by Smart-M3, and this also relieved us from having
to handle transactions manually.  ``kpwrapper`` inserts (or removes) a list of
triplets as one single transaction which was good enough for us.
Transactions themselves are not very valuable because of lack of
synchronization primitives.

``kpwrapper`` had some slight bugs in handling of entity types (URL vs. literal)
but we wrote a patch that was later applied by Eemeli to ``kpwrapper``.
``kpwrapper`` also provided a natural place for doing the necessary escaping of
XML special characters.  More specifically it was sub-classed.

In addition a pooling interface was developed atop ``kpwrapper``. This opens
connections in pool, so that they're not opened and closed continually.  It
is unknown whether this had any performance impact.  It is possible though
that this is responsible for the frequent ``sib-tcp`` hangs we are experiencing.
But that could have any number of reasons.  Another more direct advantage
was that this made opening and closing the SIB connections much less
tedious.  Actually it was condensed to one single line of ``with`` language
structure of Python in every function.

Later is was found that the guy working in the Room on Google Calendar had
also done his own abstraction layer providing pretty much similar services.
Good thing we did not go and reinvent the wheel a third time.

So as a summary, ``kpwrapper`` made low level triplet programming pretty easy.
The addition of connection pooling removed the tedium of opening connections
all the time.


Queries and subscriptions
=========================

Generating the necessary queries was easy.  Mostly because we had to confine
ourselves to template queries.  Nobody could really understand WQL, and it
seemed risky to invest more time in investigating that.  More so after the
disaster of trying to create formal ontologies for use with Python interface
generator.  That just crashed Smart-M3 and debugging seemed too hard.

So the queries were simple enough. Although we could only use template queries
with all filtering, processing and combining of query results on the Python
side. Python side abstraction for simple recursive queries that walk through
the network was implemented. This made it possible to retrieve
normal-looking information structures from Smart-M3.

Subscriptions were provided by ``kpwrapper``. Subscription queries were easy to
made and handling of their change information was simple as they were only a
list of triples that were added to or removed from SIB.

Subscriptions might actually be somewhat buggy.  All answers don't seem to be
arriving.  But this was likely a bug in our own code caused by a race
condition that was fixed later on.


Loose coupling
==============

Loose coupling might be useful. Unfortunately the continuously hanging
connections tended to overshadow this.

Certainly using Smart-M3 encouraged (or forced) a style of programming where
there are translation layers between parts.  Noppa could have changed
completely (say, add a broken pagination system) and only changes would have
been needed in the scraper if the information itself had not changed
structure.  Here the scraper already provided such layer though.  For the
ASI case the advantage the situation is larger.  We were using a Eemeli
Kantola's ``asilib`` to access the information.  This itself was tied to the
structure of ASI and could be hard to map to some other service.  The
triplets generated from the translation are more generic.  All functions
requiring real time access to ASI required something similar to
publish-subscribe networking.  Even so it was pretty loosely coupled.

Also having a storage layer between the parts makes the system more
resilient towards short outages in the background services.  A direct
translation layer would not provide this.

All this is very much overshadowed by the tendency of Smart-M3 to hang at
inopportune moments.


Problems with Smart-M3
======================

General:

* It would be nice to have a more flexible query language like SPARQL. WQL
  might have been the answer, but it's not documented apart from Ora Lassila's
  PhD thesis. And that does not contain the syntax used by Smart-M3.

Bugs:

* XML special characters cause Smart-M3 discard the triplet. A work-around was
  written for this.

* Anything resembling namespace (with ":") causes Smart-M3 to crash if the
  namespace is not defined

* Wildcard removals do not exist even though API documentation claims so.

* sib-tcp becomes unresponsive randomly
