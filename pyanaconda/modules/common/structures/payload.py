#
# DBus structures for the payload data.
#
# Copyright (C) 2020 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 31 Milk Street #960789 Boston, MA
# 02196 USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#

from dasbus.structure import DBusData
from dasbus.typing import *  # pylint: disable=wildcard-import

from pyanaconda.core.constants import (
    DNF_DEFAULT_REPO_COST,
    REPO_ORIGIN_USER,
    URL_TYPE_BASEURL,
)
from pyanaconda.core.path import join_paths

__all__ = ["RepoConfigurationData", "SSLConfigurationData"]


class SSLConfigurationData(DBusData):
    """Structure with SSL configuration settings."""

    def __init__(self):
        self._ca_cert_path = ""
        self._client_cert_path = ""
        self._client_key_path = ""

    @property
    def ca_cert_path(self) -> Str:
        """Get CA certificate path."""
        return self._ca_cert_path

    @ca_cert_path.setter
    def ca_cert_path(self, ca_cert_path: Str):
        self._ca_cert_path = ca_cert_path

    @property
    def client_cert_path(self) -> Str:
        """Get client certificate path."""
        return self._client_cert_path

    @client_cert_path.setter
    def client_cert_path(self, client_cert_path: Str):
        self._client_cert_path = client_cert_path

    @property
    def client_key_path(self) -> Str:
        """Get client key path."""
        return self._client_key_path

    @client_key_path.setter
    def client_key_path(self, client_key_path: Str):
        self._client_key_path = client_key_path

    def is_empty(self):
        """Is this configuration empty?

        :rtype: bool
        """
        return not any([
            self._ca_cert_path,
            self._client_cert_path,
            self._client_key_path]
        )

    def __repr__(self):
        """Convert this data object to a string."""
        if not self.is_empty():
            return super().__repr__()

        # Don't list attributes if none of them are set.
        return "{}()".format(self.__class__.__name__)


class RepoConfigurationData(DBusData):
    """Structure to hold repository configuration."""

    def __init__(self):
        self._name = ""
        self._origin = REPO_ORIGIN_USER
        self._enabled = True
        self._url = ""
        self._type = URL_TYPE_BASEURL
        self._ssl_verification_enabled = True
        self._ssl_configuration = SSLConfigurationData()
        self._proxy = ""
        self._cost = DNF_DEFAULT_REPO_COST
        self._exclude_packages = []
        self._included_packages = []
        self._installation_enabled = False

    @classmethod
    def from_directory(cls, directory_path):
        """Generate RepoConfigurationData url from directory path.

        This will basically add file:/// to the directory and set it to url with a proper type.

        :param str directory_path: directory which will be used to create url
        :return: RepoConfigurationData instance
        """
        data = RepoConfigurationData()

        data.url = join_paths("file:///", directory_path)

        return data

    @classmethod
    def from_url(cls, url):
        """Create a new configuration for the specified URL.

        :param str url: a URL of the installation source
        :return RepoConfigurationData: a new configuration
        """
        data = RepoConfigurationData()
        data.url = url
        return data

    @property
    def name(self) -> Str:
        """Get name of this repository.

        If name is not set it will be generated by source.
        """
        return self._name

    @name.setter
    def name(self, name: Str):
        self._name = name

    @property
    def origin(self) -> Str:
        """The origin of the repository.

        Supported values:
            SYSTEM    Provided by the system.
            USER      Specified by a user.
            TREEINFO  Generated from a .treeinfo file.

        :return: a type of the origin
        """
        return self._origin

    @origin.setter
    def origin(self, value: Str):
        self._origin = value

    @property
    def enabled(self) -> Bool:
        """Is the repository enabled?

        :return: True or False
        """
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    @property
    def url(self) -> Str:
        """Get link to the repository."""
        return self._url

    @url.setter
    def url(self, url: Str):
        self._url = url

    @property
    def type(self) -> Str:
        """Get type of the url.

        Possible values:
        - BASEURL
        - MIRRORLIST
        - METALINK
        """
        return self._type

    @type.setter
    def type(self, url_type: Str):
        self._type = url_type

    @property
    def ssl_verification_enabled(self) -> Bool:
        """Is ssl verification enabled?

        You can disable SSL verification to reach server with certificate
        which is not part of installation environment.
        """
        return self._ssl_verification_enabled

    @ssl_verification_enabled.setter
    def ssl_verification_enabled(self, ssl_verification_enabled: Bool):
        self._ssl_verification_enabled = ssl_verification_enabled

    @property
    def ssl_configuration(self) -> SSLConfigurationData:
        """Inner structure for SSL configuration.

        See SSLConfigurationData for more details.
        """
        return self._ssl_configuration

    @ssl_configuration.setter
    def ssl_configuration(self, ssl_configuration: SSLConfigurationData):
        self._ssl_configuration = ssl_configuration

    @property
    def proxy(self) -> Str:
        """Get proxy URL for this repository.

        :return: a proxy URL
        """
        return self._proxy

    @proxy.setter
    def proxy(self, proxy: Str):
        self._proxy = proxy

    @property
    def cost(self) -> Int:
        """Cost value of this repository.

        The relative cost of accessing this repository. This value is compared when the
        priorities of two repositories are the same. The repository with the lowest cost is picked.

        Default value is 1000.
        """
        return self._cost

    @cost.setter
    def cost(self, cost: Int):
        self._cost = cost

    @property
    def excluded_packages(self) -> List[Str]:
        """Packages which won't be fetched from the repository.

        A list of package names and globs that must not be fetched from this repository.
        This is useful if multiple repositories provide the same package and you
        want to make sure it is not fetched from a particular repository during installation.
        """
        return self._exclude_packages

    @excluded_packages.setter
    def excluded_packages(self, excluded_packages: List[Str]):
        self._exclude_packages = excluded_packages

    @property
    def included_packages(self) -> List[Str]:
        """Get packages which only should be installed from the repository.

        A list of package names and globs that can be pulled from this repository.
        Any other packages provided by the repository not on this list will be ignored.
        This is useful if you want to install just a single package or set of packages
        from a repository while including all other packages the repository provides.
        """
        return self._included_packages

    @included_packages.setter
    def included_packages(self, included_packages: List[Str]):
        self._included_packages = included_packages

    @property
    def installation_enabled(self) -> Bool:
        """Should the repository be installed to the target system?

        The installer will generate a repo file with a configuration
        of this repository and write it to the target system.

        :return: True or False
        """
        return self._installation_enabled

    @installation_enabled.setter
    def installation_enabled(self, value: Bool):
        self._installation_enabled = value
