# coding: utf-8

"""
    JumpCloud APIs

     JumpCloud's V2 API. This set of endpoints allows JumpCloud customers to manage objects, groupings and mappings and interact with the JumpCloud Graph.  # noqa: E501

    OpenAPI spec version: 2.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from jcapiv2.models.graph_object import GraphObject  # noqa: F401,E501


class GraphConnection(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        '_from': 'GraphObject',
        'to': 'GraphObject'
    }

    attribute_map = {
        '_from': 'from',
        'to': 'to'
    }

    def __init__(self, _from=None, to=None):  # noqa: E501
        """GraphConnection - a model defined in Swagger"""  # noqa: E501

        self.__from = None
        self._to = None
        self.discriminator = None

        if _from is not None:
            self._from = _from
        self.to = to

    @property
    def _from(self):
        """Gets the _from of this GraphConnection.  # noqa: E501


        :return: The _from of this GraphConnection.  # noqa: E501
        :rtype: GraphObject
        """
        return self.__from

    @_from.setter
    def _from(self, _from):
        """Sets the _from of this GraphConnection.


        :param _from: The _from of this GraphConnection.  # noqa: E501
        :type: GraphObject
        """

        self.__from = _from

    @property
    def to(self):
        """Gets the to of this GraphConnection.  # noqa: E501


        :return: The to of this GraphConnection.  # noqa: E501
        :rtype: GraphObject
        """
        return self._to

    @to.setter
    def to(self, to):
        """Sets the to of this GraphConnection.


        :param to: The to of this GraphConnection.  # noqa: E501
        :type: GraphObject
        """
        if to is None:
            raise ValueError("Invalid value for `to`, must not be `None`")  # noqa: E501

        self._to = to

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(GraphConnection, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, GraphConnection):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other