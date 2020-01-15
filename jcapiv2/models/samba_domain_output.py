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

from jcapiv2.models.samba_domain_input import SambaDomainInput  # noqa: F401,E501


class SambaDomainOutput(object):
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
        'name': 'str',
        'sid': 'str',
        'id': 'str'
    }

    attribute_map = {
        'name': 'name',
        'sid': 'sid',
        'id': 'id'
    }

    def __init__(self, name=None, sid=None, id=None):  # noqa: E501
        """SambaDomainOutput - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._sid = None
        self._id = None
        self.discriminator = None

        self.name = name
        self.sid = sid
        self.id = id

    @property
    def name(self):
        """Gets the name of this SambaDomainOutput.  # noqa: E501

        Name of this domain's WorkGroup  # noqa: E501

        :return: The name of this SambaDomainOutput.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SambaDomainOutput.

        Name of this domain's WorkGroup  # noqa: E501

        :param name: The name of this SambaDomainOutput.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def sid(self):
        """Gets the sid of this SambaDomainOutput.  # noqa: E501

        Security identifier of this domain  # noqa: E501

        :return: The sid of this SambaDomainOutput.  # noqa: E501
        :rtype: str
        """
        return self._sid

    @sid.setter
    def sid(self, sid):
        """Sets the sid of this SambaDomainOutput.

        Security identifier of this domain  # noqa: E501

        :param sid: The sid of this SambaDomainOutput.  # noqa: E501
        :type: str
        """
        if sid is None:
            raise ValueError("Invalid value for `sid`, must not be `None`")  # noqa: E501

        self._sid = sid

    @property
    def id(self):
        """Gets the id of this SambaDomainOutput.  # noqa: E501

        Unique identifier of this domain  # noqa: E501

        :return: The id of this SambaDomainOutput.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this SambaDomainOutput.

        Unique identifier of this domain  # noqa: E501

        :param id: The id of this SambaDomainOutput.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

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
        if issubclass(SambaDomainOutput, dict):
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
        if not isinstance(other, SambaDomainOutput):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other