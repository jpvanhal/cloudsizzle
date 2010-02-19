====================
Smart-M3 experiences
====================

Bugs:

* XML special characters cause smart-m3 discard the triplet

* Anything resembling namespace (with ":") causes smart-m3 to crash if the
  namespace is not defined

* Wildcard removals do not exist even though API documentation claims so.

Documentation:

* WQL is not documented. Apart from Ora Lassilas PhD thesis. And that does
  not contain the syntax used by Smart-M3

Smart-M3 platform and its concepts
==================================

The basic concepts of Smart-M3 were easy to learn, though this might be
tilted by the extensive tutorials given to us.  But the concept of RDF
Triplets forming a network is simple enough.

Installation
============

The platform itself was tricky to install to say the least. Compilation
instructions got better along the way.  Still even now, running the system
consists of strange dbus incantations.  We are not sure whether they are
optimal.  They just work.

Knowledge processor programming
===============================

We adapted the kpwrapper interface developed by Eemeli Kantola in a very
early phase of programming.  Basically this relieved us from having to do
handle transactions manually.  kpwrapper inserts (or removes) a list of
triplets as one single transaction which was good enough for us. 
Transactions themselves are not very valuable because of lack of
synchronization primitives.

Kpwrapper had some slight bugs in handling of entity types (url vs. literal)
but those were fixed.  Kpwrapper also provided a natural place for doing the
necessary escaping of XML special characters.  More specifically it was
subclassed.

In addition a pooling interface was developed atop kpwrapper. This opens
connections in pool, so that they're not opened and closed continually.  It
is unknown whether this had any performance impact.  It is possible though
that this is responsible for the frequent sib-tcp hangs we are experiencing. 
But that could have any number of reasons.  Another more direct advantage
was that this made opening and closing the SIB connections much less
tedious.  Actually it was condensed to one single line of "with"-language
structure of Python in every function.

Later is was found that the guy working in the Room on Google Calendar had
also done his own abstraction layer providing pretty much similar services. 
Good thing we did not go and reinvent the wheel a third time.

So as a summary, kpwrapper made low level Triplet programming pretty easy.
The addition of connection pooling removed the tedium of opening connections
all the time.

Queries and Subscriptions
=========================

Generating the necessary queries for easy. Mostly because we had to confine
ourselves to template queries.  Nobody could really understand WQL, and it
seemed risky to invest more time in investigating that.  Moreso after the
disaster of trying to create formal ontologies for use with Python-interface
generator.  That just crashed Smart-M3 and debugging seemed too hard.

So the queries were simple enough. Python side abstraction for generating
simple recursive queries that walk through the network was implemented. 
This made it possible to retrieve normal-looking information structures from
Smart-M3.

Subscriptions were provided by kpwrapper. They might actually be somewhat
buggy.  All answers don't seem to be arriving.  Whether this a bug in
Smart-M3 or somewhere in the abstraction layers is unknown.  Likely culprit
would be the threading used to handle subscriptions.

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
Kantolas asilib to access the information.  This itself was tied to the
structure of ASI and could be hard to map to some other service.  The
triplets generated from the translation are more generic.  All functions
requiring real time access to ASI required something similar to
publish-subscribe networking.  Even so it was pretty loosely coupled.

Also having a storage layer between the parts makes the system more
resilient towards short outages in the background services.  A direct
translation layer would not provide this.

All this is very much overshadowed by the tendency of Smart-M3 to hang at
inopportune moments.
