# coding: utf-8

"""
    Kipartman

    Kipartman api specifications

    OpenAPI spec version: 1.0.0
    Contact: --
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ModelNew(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
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
        'description': 'str',
        'comment': 'str',
        'snapeda': 'str',
        'snapeda_uid': 'str',
        'updated': 'datetime',
        'category': 'ModelCategoryRef',
        'image': 'UploadFileRef',
        'model': 'UploadFileRef'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'comment': 'comment',
        'snapeda': 'snapeda',
        'snapeda_uid': 'snapeda_uid',
        'updated': 'updated',
        'category': 'category',
        'image': 'image',
        'model': 'Model'
    }

    def __init__(self, name=None, description=None, comment=None, snapeda=None, snapeda_uid=None, updated=None, category=None, image=None, model=None):
        """
        ModelNew - a model defined in Swagger
        """

        self._name = None
        self._description = None
        self._comment = None
        self._snapeda = None
        self._snapeda_uid = None
        self._updated = None
        self._category = None
        self._image = None
        self._model = None

        if name is not None:
          self.name = name
        if description is not None:
          self.description = description
        if comment is not None:
          self.comment = comment
        if snapeda is not None:
          self.snapeda = snapeda
        if snapeda_uid is not None:
          self.snapeda_uid = snapeda_uid
        if updated is not None:
          self.updated = updated
        if category is not None:
          self.category = category
        if image is not None:
          self.image = image
        if model is not None:
          self.model = model

    @property
    def name(self):
        """
        Gets the name of this ModelNew.

        :return: The name of this ModelNew.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ModelNew.

        :param name: The name of this ModelNew.
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this ModelNew.

        :return: The description of this ModelNew.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ModelNew.

        :param description: The description of this ModelNew.
        :type: str
        """

        self._description = description

    @property
    def comment(self):
        """
        Gets the comment of this ModelNew.

        :return: The comment of this ModelNew.
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """
        Sets the comment of this ModelNew.

        :param comment: The comment of this ModelNew.
        :type: str
        """

        self._comment = comment

    @property
    def snapeda(self):
        """
        Gets the snapeda of this ModelNew.

        :return: The snapeda of this ModelNew.
        :rtype: str
        """
        return self._snapeda

    @snapeda.setter
    def snapeda(self, snapeda):
        """
        Sets the snapeda of this ModelNew.

        :param snapeda: The snapeda of this ModelNew.
        :type: str
        """

        self._snapeda = snapeda

    @property
    def snapeda_uid(self):
        """
        Gets the snapeda_uid of this ModelNew.

        :return: The snapeda_uid of this ModelNew.
        :rtype: str
        """
        return self._snapeda_uid

    @snapeda_uid.setter
    def snapeda_uid(self, snapeda_uid):
        """
        Sets the snapeda_uid of this ModelNew.

        :param snapeda_uid: The snapeda_uid of this ModelNew.
        :type: str
        """

        self._snapeda_uid = snapeda_uid

    @property
    def updated(self):
        """
        Gets the updated of this ModelNew.

        :return: The updated of this ModelNew.
        :rtype: datetime
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """
        Sets the updated of this ModelNew.

        :param updated: The updated of this ModelNew.
        :type: datetime
        """

        self._updated = updated

    @property
    def category(self):
        """
        Gets the category of this ModelNew.

        :return: The category of this ModelNew.
        :rtype: ModelCategoryRef
        """
        return self._category

    @category.setter
    def category(self, category):
        """
        Sets the category of this ModelNew.

        :param category: The category of this ModelNew.
        :type: ModelCategoryRef
        """

        self._category = category

    @property
    def image(self):
        """
        Gets the image of this ModelNew.

        :return: The image of this ModelNew.
        :rtype: UploadFileRef
        """
        return self._image

    @image.setter
    def image(self, image):
        """
        Sets the image of this ModelNew.

        :param image: The image of this ModelNew.
        :type: UploadFileRef
        """

        self._image = image

    @property
    def model(self):
        """
        Gets the model of this ModelNew.

        :return: The model of this ModelNew.
        :rtype: UploadFileRef
        """
        return self._model

    @model.setter
    def model(self, model):
        """
        Sets the model of this ModelNew.

        :param model: The model of this ModelNew.
        :type: UploadFileRef
        """

        self._model = model

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, ModelNew):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
