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


class DuoApplicationUpdateReq(object):
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
        'api_host': 'str',
        'integration_key': 'str',
        'name': 'str',
        'secret_key': 'str'
    }

    attribute_map = {
        'api_host': 'apiHost',
        'integration_key': 'integrationKey',
        'name': 'name',
        'secret_key': 'secretKey'
    }

    def __init__(self, api_host=None, integration_key=None, name=None, secret_key=None):  # noqa: E501
        """DuoApplicationUpdateReq - a model defined in Swagger"""  # noqa: E501

        self._api_host = None
        self._integration_key = None
        self._name = None
        self._secret_key = None
        self.discriminator = None

        if api_host is not None:
            self.api_host = api_host
        if integration_key is not None:
            self.integration_key = integration_key
        if name is not None:
            self.name = name
        if secret_key is not None:
            self.secret_key = secret_key

    @property
    def api_host(self):
        """Gets the api_host of this DuoApplicationUpdateReq.  # noqa: E501


        :return: The api_host of this DuoApplicationUpdateReq.  # noqa: E501
        :rtype: str
        """
        return self._api_host

    @api_host.setter
    def api_host(self, api_host):
        """Sets the api_host of this DuoApplicationUpdateReq.


        :param api_host: The api_host of this DuoApplicationUpdateReq.  # noqa: E501
        :type: str
        """

        self._api_host = api_host

    @property
    def integration_key(self):
        """Gets the integration_key of this DuoApplicationUpdateReq.  # noqa: E501


        :return: The integration_key of this DuoApplicationUpdateReq.  # noqa: E501
        :rtype: str
        """
        return self._integration_key

    @integration_key.setter
    def integration_key(self, integration_key):
        """Sets the integration_key of this DuoApplicationUpdateReq.


        :param integration_key: The integration_key of this DuoApplicationUpdateReq.  # noqa: E501
        :type: str
        """

        self._integration_key = integration_key

    @property
    def name(self):
        """Gets the name of this DuoApplicationUpdateReq.  # noqa: E501


        :return: The name of this DuoApplicationUpdateReq.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this DuoApplicationUpdateReq.


        :param name: The name of this DuoApplicationUpdateReq.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def secret_key(self):
        """Gets the secret_key of this DuoApplicationUpdateReq.  # noqa: E501


        :return: The secret_key of this DuoApplicationUpdateReq.  # noqa: E501
        :rtype: str
        """
        return self._secret_key

    @secret_key.setter
    def secret_key(self, secret_key):
        """Sets the secret_key of this DuoApplicationUpdateReq.


        :param secret_key: The secret_key of this DuoApplicationUpdateReq.  # noqa: E501
        :type: str
        """

        self._secret_key = secret_key

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
        if issubclass(DuoApplicationUpdateReq, dict):
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
        if not isinstance(other, DuoApplicationUpdateReq):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
