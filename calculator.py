import traceback
"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""

def home():
    """Provide an index page with user instructions."""
    page = """
    <h1>Here's how to use this calculator page...</h1>
    <p>You perform basic math operations by visiting addresses like this:</p>
      <p><a href="http://localhost:8080/multiply/3/5">http://localhost:8080/multiply/3/5</a>   => 15</p>
      <p><a href="http://localhost:8080/add/23/42">http://localhost:8080/add/23/42</a>      => 65</p>
      <p><a href="http://localhost:8080/subtract/23/42">http://localhost:8080/subtract/23/42</a> => -19</p>
      <p><a href="http://localhost:8080/divide/22/11">http://localhost:8080/divide/22/11</a>   => 2</p>
    """

    return page


def decorate_math(math_func):
    """Provide a decortating func for math functions."""
    def return_func(*args):
        """Wrap up the math func output."""
        template = """
            <h1>{}</h1>
            <p><br /></p>
            <a href="/">Back to index</a>
        """
        try:
            res = math_func(*args)
        except ZeroDivisionError:
            raise ZeroDivisionError
        except ValueError:
            raise ValueError
        return template.format(res)

    return return_func


@decorate_math
def add(*args):
    """Return a STRING with the sum of the arguments."""
    return str(sum(map(float, args)))

# def add(*args):
#     """Return a STRING with the sum of the arguments."""
#     # TODO: Fill sum with the correct value, based on the
#     # args provided.
#     template = """
#         <h1>{}</h1>
#         <p><br /></p>
#         <a href="/">Back to index</a>
#     """
#     try:
#         total = template.format(str(sum(map(float, args))))
#     except ValueError:
#         raise ValueError
#
#     return total


@decorate_math
def divide(*args):
    """Return a STRING with the quotient of the arguments."""
    return str(float(args[0])/float(args[1]))


# def divide(*args):
#     """Return a STRING with the quotient of the arguments."""
#     template = """
#         <h1>{}</h1>
#         <p><br /></p>
#         <a href="/">Back to index</a>
#     """
#     try:
#         quotient = template.format(str(float(args[0])/float(args[1])))
#     except ZeroDivisionError:
#         raise ZeroDivisionError
#     except ValueError:
#         raise ValueError
#
#     return quotient


@decorate_math
def subtract(*args):
    """Return a STRING with the diff of the arguments."""
    return str(float(args[0]) - float(args[1]))


# def subtract(*args):
#     """Return a STRING with the diff of the arguments."""
#     template = """
#         <h1>{}</h1>
#         <p><br /></p>
#         <a href="/">Back to index</a>
#     """
#     try:
#         difference = template.format(str(float(args[0]) - float(args[1])))
#     except ValueError:
#         raise ValueError
#
#     return difference


@decorate_math
def multiply(*args):
    """Return a STRING with the product of the arguments."""
    return str(float(args[0]) * float(args[1]))


# def multiply(*args):
#     """Return a STRING with the product of the arguments."""
#     template = """
#         <h1>{}</h1>
#         <p><br /></p>
#         <a href="/">Back to index</a>
#     """
#     try:
#         product = template.format(str(float(args[0]) * float(args[1])))
#     except ValueError:
#         raise ValueError
#
#     return product


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    funcs = {
        '': home,
        'add': add,
        'divide': divide,
        'subtract': subtract,
        'multiply': multiply,
    }

    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    # pass
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "500 ZeroDivisionError"
        body = "<h1>Can't devide by zero</h1>"
        body += '<p><br /></p>'
        body += '<a href="/">Back to index</a>'
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    # pass
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
