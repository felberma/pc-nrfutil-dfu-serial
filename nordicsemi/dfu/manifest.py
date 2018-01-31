#
# Copyright (c) 2016 Nordic Semiconductor ASA
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.
#
#   3. Neither the name of Nordic Semiconductor ASA nor the names of other
#   contributors to this software may be used to endorse or promote products
#   derived from this software without specific prior written permission.
#
#   4. This software must only be used in or with a processor manufactured by Nordic
#   Semiconductor ASA, or in or with a processor manufactured by a third party that
#   is used in combination with a processor manufactured by Nordic Semiconductor.
#
#   5. Any software provided in binary or object form under this license must not be
#   reverse engineered, decompiled, modified and/or disassembled.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# Python libraries
import json

class FWMetaData(object):
    def __init__(self,
                 is_debug=None,
                 hw_version=None,
                 fw_version=None,
                 softdevice_req=None,
                 sd_size=None,
                 bl_size=None
                 ):
        """
        The FWMetaData data model.

        :param bool is_debug:  debug mode on
        :param int hw_version:  hardware version
        :param int fw_version:  application or bootloader version
        :param list softdevice_req: softdevice requirements
        :param int sd_size SoftDevice size
        :param int bl_size Bootloader size
        :return:FWMetaData
        """
        self.is_debug = is_debug
        self.hw_version = hw_version
        self.fw_version = fw_version
        self.softdevice_req = softdevice_req
        self.sd_size = sd_size
        self.bl_size = bl_size


class Firmware(object):
    def __init__(self,
                 bin_file=None,
                 dat_file=None,
                 info_read_only_metadata=None):
        """
        The firmware datamodel

        :param str bin_file: Firmware binary file
        :param str dat_file: Firmware .dat file (init packet for Nordic DFU)
        :param int info_read_only_metadata: The metadata about this firwmare image
        :return:
        """
        self.dat_file = dat_file
        self.bin_file = bin_file

        if info_read_only_metadata:
            self.info_read_only_metadata = FWMetaData(**info_read_only_metadata)
        else:
            self.info_read_only_metadata = None


class SoftdeviceBootloaderFirmware(Firmware):
    def __init__(self,
                 bin_file=None,
                 dat_file=None,
                 info_read_only_metadata=None):
        """
        The SoftdeviceBootloaderFirmware data model

        :param str bin_file: Firmware binary file
        :param str dat_file: Firmware .dat file (init packet for Nordic DFU)
        :param int info_read_only_metadata: The metadata about this firwmare image
        :return: SoftdeviceBootloaderFirmware
        """
        super(SoftdeviceBootloaderFirmware, self).__init__(
            bin_file,
            dat_file,
            info_read_only_metadata)

class Manifest:
    def __init__(self,
                 application=None,
                 bootloader=None,
                 softdevice=None,
                 softdevice_bootloader=None):
        """
        The Manifest data model.

        :param dict application: Application firmware in package
        :param dict bootloader: Bootloader firmware in package
        :param dict softdevice: Softdevice firmware in package
        :param dict softdevice_bootloader: Combined softdevice and bootloader firmware in package
        :return: Manifest
        """
        self.softdevice_bootloader = \
            SoftdeviceBootloaderFirmware(**softdevice_bootloader) if softdevice_bootloader else None

        self.softdevice = Firmware(**softdevice) if softdevice else None
        self.bootloader = Firmware(**bootloader) if bootloader else None
        self.application = Firmware(**application) if application else None

    @staticmethod
    def from_json(data):
        """
        Parses a manifest according to Nordic DFU package specification.

        :param str data: The manifest in string format
        :return: Manifest
        """
        kwargs = json.loads(data)
        return Manifest(**kwargs['manifest'])
