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


class PolicyTemplate(object):
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
        'activation': 'str',
        'behavior': 'str',
        'description': 'str',
        'display_name': 'str',
        'id': 'str',
        'name': 'str',
        'os_meta_family': 'str',
        'state': 'str'
    }

    attribute_map = {
        'activation': 'activation',
        'behavior': 'behavior',
        'description': 'description',
        'display_name': 'displayName',
        'id': 'id',
        'name': 'name',
        'os_meta_family': 'osMetaFamily',
        'state': 'state'
    }

    def __init__(self, activation=None, behavior=None, description=None, display_name=None, id=None, name=None, os_meta_family=None, state=''):  # noqa: E501
        """PolicyTemplate - a model defined in Swagger"""  # noqa: E501

        self._activation = None
        self._behavior = None
        self._description = None
        self._display_name = None
        self._id = None
        self._name = None
        self._os_meta_family = None
        self._state = None
        self.discriminator = None

        if activation is not None:
            self.activation = activation
        if behavior is not None:
            self.behavior = behavior
        if description is not None:
            self.description = description
        if display_name is not None:
            self.display_name = display_name
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if os_meta_family is not None:
            self.os_meta_family = os_meta_family
        if state is not None:
            self.state = state

    @property
    def activation(self):
        """Gets the activation of this PolicyTemplate.  # noqa: E501

        Requirements before the policy can be activated.  # noqa: E501

        :return: The activation of this PolicyTemplate.  # noqa: E501
        :rtype: str
        """
        return self._activation

    @activation.setter
    def activation(self, activation):
        """Sets the activation of this PolicyTemplate.

        Requirements before the policy can be activated.  # noqa: E501

        :param activation: The activation of this PolicyTemplate.  # noqa: E501
        :type: str
        """

        self._activation = activation

    @property
    def behavior(self):
        """Gets the behavior of this PolicyTemplate.  # noqa: E501

        Specifics about the behavior of the policy.  # noqa: E501

        :return: The behavior of this PolicyTemplate.  # noqa: E501
        :rtype: str
        """
        return self._behavior

    @behavior.setter
    def behavior(self, behavior):
        """Sets the behavior of this PolicyTemplate.

        Specifics about the behavior of the policy.  # noqa: E501

        :param behavior: The behavior of this PolicyTemplate.  # noqa: E501
        :type: str
        """

        self._behavior = behavior

    @property
    def description(self):
        """Gets the description of this PolicyTemplate.  # noqa: E501

        The default description for the Policy.  # noqa: E501

        :return: The description of this PolicyTemplate.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this PolicyTemplate.

        The default description for the Policy.  # noqa: E501

        :param description: The description of this PolicyTemplate.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def display_name(self):
        """Gets the display_name of this PolicyTemplate.  # noqa: E501

        The default display name for the Policy.  # noqa: E501

        :return: The display_name of this PolicyTemplate.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this PolicyTemplate.

        The default display name for the Policy.  # noqa: E501

        :param display_name: The display_name of this PolicyTemplate.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def id(self):
        """Gets the id of this PolicyTemplate.  # noqa: E501

        ObjectId uniquely identifying a Policy Template.  # noqa: E501

        :return: The id of this PolicyTemplate.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PolicyTemplate.

        ObjectId uniquely identifying a Policy Template.  # noqa: E501

        :param id: The id of this PolicyTemplate.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this PolicyTemplate.  # noqa: E501

        The unique name for the Policy Template.  # noqa: E501

        :return: The name of this PolicyTemplate.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PolicyTemplate.

        The unique name for the Policy Template.  # noqa: E501

        :param name: The name of this PolicyTemplate.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def os_meta_family(self):
        """Gets the os_meta_family of this PolicyTemplate.  # noqa: E501


        :return: The os_meta_family of this PolicyTemplate.  # noqa: E501
        :rtype: str
        """
        return self._os_meta_family

    @os_meta_family.setter
    def os_meta_family(self, os_meta_family):
        """Sets the os_meta_family of this PolicyTemplate.


        :param os_meta_family: The os_meta_family of this PolicyTemplate.  # noqa: E501
        :type: str
        """
        allowed_values = ["linux", "darwin", "windows"]  # noqa: E501
        if os_meta_family not in allowed_values:
            raise ValueError(
                "Invalid value for `os_meta_family` ({0}), must be one of {1}"  # noqa: E501
                .format(os_meta_family, allowed_values)
            )

        self._os_meta_family = os_meta_family

    @property
    def state(self):
        """Gets the state of this PolicyTemplate.  # noqa: E501

        String describing the release status of the policy template.  # noqa: E501

        :return: The state of this PolicyTemplate.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this PolicyTemplate.

        String describing the release status of the policy template.  # noqa: E501

        :param state: The state of this PolicyTemplate.  # noqa: E501
        :type: str
        """

        self._state = state

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
        if issubclass(PolicyTemplate, dict):
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
        if not isinstance(other, PolicyTemplate):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other