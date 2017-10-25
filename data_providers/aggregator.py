# coding=utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

from abc import ABCMeta, abstractmethod as abstract_method
from collections import defaultdict
from typing import Any, Hashable, Iterable, Mapping

from six import iteritems, iterkeys, with_metaclass

from data_providers import BaseDataProvider

__all__ = [
    'BaseDataProviderAggregator',
]


class BaseDataProviderAggregator(with_metaclass(ABCMeta)):
    """
    A data-provider-like object that aggregates values from
    several data providers.
    """
    def __init__(self):
        super(BaseDataProviderAggregator, self).__init__()

        self._data_providers = None

    def __getitem__(self, value):
        """
        Returns the data for the specified value.

        :param value:
            The lookup key.

        :raise:
            - :py:class:`ValueError` if the value wasn't registered
              first.
        """
        return self.aggregate_data(
            value = value,

            data = {
                key: self.data_providers[key][value]
                    for key in self.gen_routing_keys(value)
            },
        )

    @property
    def data_providers(self):
        # type: () -> Mapping[Hashable, BaseDataProvider]
        """
        Lazy-loads the data providers for this aggregator.
        """
        if self._data_providers is None:
            self._data_providers = self.create_data_providers()
        return self._data_providers

    @abstract_method
    def aggregate_data(self, value, data):
        # type: (Any, Mapping) -> Any
        """
        Aggregates the data returned by each of the data providers for
        the specified value.

        :param value:
            The value provided to :py:meth:`__getitem__`.

        :param data:
            A mapping containing the data returned by each data
            provider (corresponding to
            :py:meth:`create_data_providers`).

            Note that this value might only contain a subset of the
            data providers, depending on :py:meth:`gen_routing_keys`.
        """
        raise NotImplementedError(
            'Not implemented in {cls}.'.format(cls=type(self).__name__),
        )

    @abstract_method
    def create_data_providers(self):
        # type: () -> Mapping[Hashable, BaseDataProvider]
        """
        Creates the mapping of data providers used by this aggregator.

        :return:
            Must return a mapping, so that each data provider is mapped
            to a unique key.
        """
        raise NotImplementedError(
            'Not implemented in {cls}.'.format(cls=type(self).__name__),
        )

    # noinspection PyUnusedLocal
    def gen_routing_keys(self, value):
        # type: (Any) -> Iterable[Hashable]
        """
        Returns the keys of the data providers that should handle the
        specified value.

        :return:
            Values correspond to keys in the mapping returned by
            :py:meth:`create_data_providers`.
        """
        return iterkeys(self.data_providers)

    def group_by_routing_keys(self, values):
        # type: (Iterable) -> Mapping[Hashable, Iterable]
        """
        Groups a set of values by their routing keys.
        """
        groups = defaultdict(list)

        for v in values:
            for key in self.gen_routing_keys(v):
                groups[key].append(v)

        return groups

    def register(self, values):
        # type: (Iterable) -> None
        """
        Registers a set of values so that the data providers can plan
        out the bulk queries they need to execute against the backend.
        """
        for key, group in iteritems(self.group_by_routing_keys(values)):
            self.data_providers[key].register(group)
