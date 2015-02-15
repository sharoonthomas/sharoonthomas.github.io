TDD, flask and the pypa sprint at pycon 2014
============================================

:date: 2014-05-09 00:00
:slug: tdd-flask-and-pypa-sprint-at-pycon-2014
:tags: python, pycon

*Thanks to a controversial post by David Hansson declaring the death of test
driven development, and the google hangout by David, Kent Beck and Martin
Fowler that I finally have gathered the courage to write this post.*

I had the opportunity to sprint with the python packaging authority (pypa) 
team on warehouse, the next generation python package repository. I 
volunteered to refactor the codebase to use more of flask. What stumped me was
the "unit tests" in the project. 

The package has 100% test coverage and the continuous integration system 
(read travis) ensures that any pull request which reduces that promptly fails.
Sounds great isn't it ? But, soon came the issues and here are a few:

**1. The false confidence of 100% coverage**

As I moved the project from manually connected URL routes to using flask 
blueprints and the route decorator, I discovered two endpoints which were well
tested but not connected to the URL Map because the contributor had forgotten
to add them and the unit test only tested that given a stubbed request a
stubbed response is returned.


**2. The abuse of mocks and the resulting brittleness**

.. image:: /images/content/technology/abuse-of-mocks.png
   :alt: Absure of mocks and the resulting brittleness

The above code tests the root view and from what I can count has 12 stubs. It
felt wrong but I wasn't sure, but I was happy to see another developer at the
sprint expressing his displeasure at the number of mocks he had to change to
make a simple improvement in the code. 

During the `hangout <https://plus.google.com/events/ci2g23mk0lh9too9bgbp3rbut0k>`_ 
today, Kent beck highlighted such use of "mocks returning mocks returning mocks"
as the primary reason why he thinks TDD becomes counterproductive.


Comments on `HN <https://news.ycombinator.com/item?id=7721768>`_
