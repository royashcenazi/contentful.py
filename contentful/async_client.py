import asyncio

from .client import Client


"""
contentful.async_client
~~~~~~~~~~~~~~~~~~~~~~~~

Async-friendly wrapper around :class:`Client <contentful.Client>`.

Rather than reimplementing the HTTP layer with an async library,
each API method that performs a network request is exposed as a
coroutine that runs the original (blocking) call in a background
thread via :func:`asyncio.to_thread`. This keeps the async surface
a thin wrapper around :class:`Client <contentful.Client>` and avoids
introducing a new HTTP dependency.

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


#: Methods that perform a network request and should be awaitable.
ASYNC_METHODS = (
    'space',
    'content_type',
    'content_types',
    'entry',
    'entries',
    'asset',
    'assets',
    'locales',
    'sync',
    'taxonomy_concept',
    'taxonomy_concepts',
    'taxonomy_concept_scheme',
    'taxonomy_concept_schemes',
    'create_asset_key',
)


def _make_async(method):
    async def wrapper(self, *args, **kwargs):
        return await asyncio.to_thread(method, self, *args, **kwargs)

    wrapper.__name__ = method.__name__
    wrapper.__doc__ = method.__doc__
    return wrapper


class AsyncClient(Client):
    """Async version of :class:`Client <contentful.Client>`.

    Accepts the same arguments as :class:`Client <contentful.Client>`.
    Every method that performs a network request (``entries``, ``entry``,
    ``assets``, ``sync``, etc.) becomes a coroutine that can be awaited
    without blocking the event loop.

    Usage:

        >>> import asyncio
        >>> from contentful import AsyncClient
        >>> client = AsyncClient('space_id', 'access_token')
        >>> entries = asyncio.run(client.entries())
    """


for _name in ASYNC_METHODS:
    setattr(AsyncClient, _name, _make_async(getattr(Client, _name)))
