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


class WorkdayRequest(object):
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
        'object_id': 'str'
    }

    attribute_map = {
        'name': 'name',
        'object_id': 'objectId'
    }

    def __init__(self, name=None, object_id=None):  # noqa: E501
        """WorkdayRequest - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._object_id = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if object_id is not None:
            self.object_id = object_id

    @property
    def name(self):
        """Gets the name of this WorkdayRequest.  # noqa: E501


        :return: The name of this WorkdayRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this WorkdayRequest.


        :param name: The name of this WorkdayRequest.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def object_id(self):
        """Gets the object_id of this WorkdayRequest.  # noqa: E501


        :return: The object_id of this WorkdayRequest.  # noqa: E501
        :rtype: str
        """
        return self._object_id

    @object_id.setter
    def object_id(self, object_id):
        """Sets the object_id of this WorkdayRequest.


        :param object_id: The object_id of this WorkdayRequest.  # noqa: E501
        :type: str
        """

        self._object_id = object_id

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
        if issubclass(WorkdayRequest, dict):
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
        if not isinstance(other, WorkdayRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
