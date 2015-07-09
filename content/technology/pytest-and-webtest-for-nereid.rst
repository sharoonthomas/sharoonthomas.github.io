Using pytest and webtest with nereid
====================================

:date: 2015-07-09
:slug: python-and-webtest-for-nereid
:tags: tryton, python, testing, nereid

I came across webtest_ a few weeks back when hacking on a flask project and
I instantly knew that most nereid tests were functional tests and they
could be better written with webtest_. Since pytest_ has become the
preferred way of writing tests in Tryton_, this post combines both to
write better and cleaner nereid_ tests using pytest_ and webtest_.

The examples below assume that you have a version of nereid 3.4.0.6 or
greater.
   
Quick Start
-----------

The most important object in WebTest is a TestApp, the wrapper for WSGI
applications. It also allows you to perform HTTP requests on it, much like the
``test_client`` in nereid tests. To use it, you simply instantiate it with 
a WSGI application, which in this case would be the nereid test app.


Create a test app

.. code-block:: python

    >>> from webtest import TestApp
    >>> from nereid.testing import get_app
    >>> app = TestApp(get_app())

Then you can get the response of a HTTP GET within a transaction using

.. code-block:: python

    >>> resp = app.get('/')

And check the results, like response's status

.. code-block:: python

    >>> assert resp.status == '200 OK'
    >>> assert resp.status_int == 200

Response's headers

.. code-block:: python

    >>> assert resp.content_type == 'text/html'
    >>> assert resp.content_length > 0

Fixtures
--------

Testing a database driven application like nereid, built over a full-stack
framework requires extensive setup and teardown functions. Fixtures_ in
pytest_ are a dramatic improvement where they are implemented in a modular
manner with explicit names. 

If you are familiar with x-unit style testing in nereid, this is what was
done in every ``setup_defaults`` method in unit test classes. You will
instantly notice that pytest fixtures for nereid are modular and reusable
even in other fixtures while ``setup_defaults`` usually ended up being
long methods.

A fixture with the scope as session

.. code-block:: python

    import pytest
    from webtest import TestApp

    @pytest.fixture(scope='session', autouse=True)
    def install_module(request):
        """Install tryton module in specified database.
        """
        from trytond.tests import test_tryton
        test_tryton.install_module('module_name')

A fixture that returns a web test application.

.. code-block:: python

    @pytest.fixture
    def app():
        """
        Return  a webtest TestApp instance for a Nereid testing
        application
        """
        from nereid.testing import get_app
        return TestApp(get_app())


A fixture to create a company

.. code-block:: python

    @pytest.fixture()
    def company(request):
        Party = Pool().get('party.party')
        Company = Pool().get('company.company')
        Country = Pool().get('country.country')
        Subdivision = Pool().get('country.subdivision')
        Currency = Pool().get('currency.currency')

        companies = Company.search([])
        if companies:
            return companies[0]

        usd, = Currency.create([{
            'name': 'US Dollar',
            'code': 'USD',
            'symbol': '$',
        }])
        country_us, = Country.create([{
            'name': 'United States',
            'code': 'US',
        }])
        subdivision_florida, = Subdivision.create([{
            'name': 'Florida',
            'code': 'US-FL',
            'country': country_us.id,
            'type': 'state'
        }])
        subdivision_california, = Subdivision.create([{
            'name': 'California',
            'code': 'US-CA',
            'country': country_us.id,
            'type': 'state'
        }])
        company_party, = Party.create([{
            'name': 'ABC Corp.',
            'addresses': [('create', [{
                'name': 'ABC Corp.',
                'street': '247 High Street',
                'zip': '94301-1041',
                'city': 'Palo Alto',
                'country': country_us.id,
                'subdivision': subdivision_california.id,
            }])],
            'contact_mechanisms': [('create', [{
                'type': 'phone',
                'value': '123456789'
            }])]
        }])
        employee_party, = Party.create([{
            'name': 'Prakash Pandey',
        }])
        company, = Company.create([{
            'party': company_party.id,
            'currency': usd.id,
        }])
        return company

These fixtures go into a file named ``conftest.py``. A full example can
be seen in the stripe payment gateway integration module.

Transactions through fixtures
`````````````````````````````

A common setup and teardown in every test is the starting and stopping of
a tryton transaction. pytest offers a way to write fixtures for tests that
can be enfored to be auto used.

.. code-block:: python

    class TestSomething:

        @pytest.fixture(autouse=True)
        def transaction(self, request):
            from trytond.tests.test_tryton import USER, CONTEXT, DB_NAME
            from trytond.transaction import Transaction

            Transaction().start(DB_NAME, USER, context=CONTEXT)

            def finalizer():
                Transaction().cursor.rollback()
                Transaction().stop()

            request.addfinalizer(finalizer)

        def test_party_search():
            Party = Pool().get('party.party')
            Party.search([])


The ``test_party_search`` test would be executed within a Tryton
transaction and the teardown would be the finalizer function defined in
the transaction fixture.

Writing test functions
----------------------

Once the fixtures are done, test functions could be written that have
little or no boilerplate code as in the above example.

.. code-block:: python

    def test_login(self, app, nereid_user, website):
        """
        Test the login functionality
        """
        response = app.get('/login')

        # Fill and submit the login form
        form = response.forms['login-form']
        form['email'] = nereid_user.email
        form['password'] = 'password'
        res = form.submit()

        # Ensure that the response was a redirect to home page
        assert res.status_int == 302
        assert res.location == 'http://localhost:80/'

Since the session is maintained by the app, you can now make requests as
though the user is already logged in like in a browser session.

.. code-block:: python

        response = app.get('/my-account')

Common patterns
---------------

Status code checks
``````````````````

Most expected responses from a web application are 2XX or 3XX. Webtest by
default raises an exception when the response is not one of these two.
This avoids a common pattern where you get a response first and then check
the status code.

.. code-block:: python

    app.get('/an-url-that-does-not-exist')

will automatically raise an exception indicating the response was a
``404``.

Status codes based on login
```````````````````````````

A common pattern followed in functional tests of a web application is
checking how a resource responds based on the user's login status and
permissions. Usually this involves:

* GET the resource without logging in.
* Check Response
* Log the user in
* GET the resource again
* Check Response

webtest makes this straightforward

.. code-block:: python

    app.get('/my-account', status=302)

Expect a 302 (redirect to login) when ``/my-account`` is accessed
directly.

login and test

.. code-block:: python

    app.post('/login', {'email': 'my-email@domain.com', 'password': 'pass'})
    app.get('/my-account', status=200)

An exception is raised the expected response of ``200`` is not received.

JSON responses
``````````````

webtest responses include a json property that parses and returns the
json response as a python literal.

.. code-block:: python

    response = app.get('/user-status')
    assert response.json['name'] = 'Sharoon Thomas'

Other ideas
-----------

While it is easy to write new fixtures, having reusable fixtures in
upstream modules to create chart of accounts, commonly used journals,
companies or currencies could make writing tests for downstream modules
which use them faster. The easier it is to write a test, the more likely
the developer is to write tests.

Nereid webshop is a project that could take a lot of benefit from this
pattern since it bundles templates with it. A functional test suite that
checks the entire business process from adding to cart all the way to
checkout could ensure that changes in templates by designers do not break
the functionality of the webshop. Perhaps, the test could be inherited by
modules which are themes for webshop, only making changes to tests where
functional changes exist on modules.

I hope that this post helps you write better tests for nereid with webtest
and pytest.

.. _webtest: http://webtest.readthedocs.org/en/latest/
.. _pytest: https://pytest.org/
.. _nereid: http://nereid.readthedocs.org/en/latest/
.. _Fixture: http://pytest.org/latest/fixture.html#fixture
.. _tryton: http://www.tryton.org/
