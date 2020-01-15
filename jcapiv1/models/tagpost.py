# coding: utf-8

"""
    JumpCloud APIs

     JumpCloud's V1 API. This set of endpoints allows JumpCloud customers to manage commands, systems, & system users.  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class Tagpost(object):
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
        'external_dn': 'str',
        'external_source_type': 'str',
        'externally_managed': 'bool',
        'group_gid': 'str',
        'group_name': 'str',
        'name': 'str',
        'regular_expressions': 'list[str]',
        'send_to_ldap': 'bool',
        'systems': 'list[str]',
        'systemusers': 'list[str]'
    }

    attribute_map = {
        'external_dn': 'externalDN',
        'external_source_type': 'externalSourceType',
        'externally_managed': 'externallyManaged',
        'group_gid': 'groupGid',
        'group_name': 'groupName',
        'name': 'name',
        'regular_expressions': 'regularExpressions',
        'send_to_ldap': 'sendToLDAP',
        'systems': 'systems',
        'systemusers': 'systemusers'
    }

    def __init__(self, external_dn=None, external_source_type=None, externally_managed=None, group_gid=None, group_name=None, name=None, regular_expressions=None, send_to_ldap=None, systems=None, systemusers=None):  # noqa: E501
        """Tagpost - a model defined in Swagger"""  # noqa: E501

        self._external_dn = None
        self._external_source_type = None
        self._externally_managed = None
        self._group_gid = None
        self._group_name = None
        self._name = None
        self._regular_expressions = None
        self._send_to_ldap = None
        self._systems = None
        self._systemusers = None
        self.discriminator = None

        if external_dn is not None:
            self.external_dn = external_dn
        if external_source_type is not None:
            self.external_source_type = external_source_type
        if externally_managed is not None:
            self.externally_managed = externally_managed
        if group_gid is not None:
            self.group_gid = group_gid
        if group_name is not None:
            self.group_name = group_name
        self.name = name
        if regular_expressions is not None:
            self.regular_expressions = regular_expressions
        if send_to_ldap is not None:
            self.send_to_ldap = send_to_ldap
        if systems is not None:
            self.systems = systems
        if systemusers is not None:
            self.systemusers = systemusers

    @property
    def external_dn(self):
        """Gets the external_dn of this Tagpost.  # noqa: E501


        :return: The external_dn of this Tagpost.  # noqa: E501
        :rtype: str
        """
        return self._external_dn

    @external_dn.setter
    def external_dn(self, external_dn):
        """Sets the external_dn of this Tagpost.


        :param external_dn: The external_dn of this Tagpost.  # noqa: E501
        :type: str
        """

        self._external_dn = external_dn

    @property
    def external_source_type(self):
        """Gets the external_source_type of this Tagpost.  # noqa: E501


        :return: The external_source_type of this Tagpost.  # noqa: E501
        :rtype: str
        """
        return self._external_source_type

    @external_source_type.setter
    def external_source_type(self, external_source_type):
        """Sets the external_source_type of this Tagpost.


        :param external_source_type: The external_source_type of this Tagpost.  # noqa: E501
        :type: str
        """

        self._external_source_type = external_source_type

    @property
    def externally_managed(self):
        """Gets the externally_managed of this Tagpost.  # noqa: E501


        :return: The externally_managed of this Tagpost.  # noqa: E501
        :rtype: bool
        """
        return self._externally_managed

    @externally_managed.setter
    def externally_managed(self, externally_managed):
        """Sets the externally_managed of this Tagpost.


        :param externally_managed: The externally_managed of this Tagpost.  # noqa: E501
        :type: bool
        """

        self._externally_managed = externally_managed

    @property
    def group_gid(self):
        """Gets the group_gid of this Tagpost.  # noqa: E501


        :return: The group_gid of this Tagpost.  # noqa: E501
        :rtype: str
        """
        return self._group_gid

    @group_gid.setter
    def group_gid(self, group_gid):
        """Sets the group_gid of this Tagpost.


        :param group_gid: The group_gid of this Tagpost.  # noqa: E501
        :type: str
        """

        self._group_gid = group_gid

    @property
    def group_name(self):
        """Gets the group_name of this Tagpost.  # noqa: E501


        :return: The group_name of this Tagpost.  # noqa: E501
        :rtype: str
        """
        return self._group_name

    @group_name.setter
    def group_name(self, group_name):
        """Sets the group_name of this Tagpost.


        :param group_name: The group_name of this Tagpost.  # noqa: E501
        :type: str
        """

        self._group_name = group_name

    @property
    def name(self):
        """Gets the name of this Tagpost.  # noqa: E501

        A unique name for the Tag.  # noqa: E501

        :return: The name of this Tagpost.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Tagpost.

        A unique name for the Tag.  # noqa: E501

        :param name: The name of this Tagpost.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def regular_expressions(self):
        """Gets the regular_expressions of this Tagpost.  # noqa: E501


        :return: The regular_expressions of this Tagpost.  # noqa: E501
        :rtype: list[str]
        """
        return self._regular_expressions

    @regular_expressions.setter
    def regular_expressions(self, regular_expressions):
        """Sets the regular_expressions of this Tagpost.


        :param regular_expressions: The regular_expressions of this Tagpost.  # noqa: E501
        :type: list[str]
        """

        self._regular_expressions = regular_expressions

    @property
    def send_to_ldap(self):
        """Gets the send_to_ldap of this Tagpost.  # noqa: E501


        :return: The send_to_ldap of this Tagpost.  # noqa: E501
        :rtype: bool
        """
        return self._send_to_ldap

    @send_to_ldap.setter
    def send_to_ldap(self, send_to_ldap):
        """Sets the send_to_ldap of this Tagpost.


        :param send_to_ldap: The send_to_ldap of this Tagpost.  # noqa: E501
        :type: bool
        """

        self._send_to_ldap = send_to_ldap

    @property
    def systems(self):
        """Gets the systems of this Tagpost.  # noqa: E501

        An array of system ids that are associated to the Tag.  # noqa: E501

        :return: The systems of this Tagpost.  # noqa: E501
        :rtype: list[str]
        """
        return self._systems

    @systems.setter
    def systems(self, systems):
        """Sets the systems of this Tagpost.

        An array of system ids that are associated to the Tag.  # noqa: E501

        :param systems: The systems of this Tagpost.  # noqa: E501
        :type: list[str]
        """

        self._systems = systems

    @property
    def systemusers(self):
        """Gets the systemusers of this Tagpost.  # noqa: E501

        An array of system user ids that are associated to the Tag.  # noqa: E501

        :return: The systemusers of this Tagpost.  # noqa: E501
        :rtype: list[str]
        """
        return self._systemusers

    @systemusers.setter
    def systemusers(self, systemusers):
        """Sets the systemusers of this Tagpost.

        An array of system user ids that are associated to the Tag.  # noqa: E501

        :param systemusers: The systemusers of this Tagpost.  # noqa: E501
        :type: list[str]
        """

        self._systemusers = systemusers

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
        if issubclass(Tagpost, dict):
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
        if not isinstance(other, Tagpost):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other