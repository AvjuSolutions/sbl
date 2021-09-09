/*
 * The Clear BSD License
 * Copyright (c) 2015, Freescale Semiconductor, Inc.
 * Copyright 2016 NXP
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted (subject to the limitations in the disclaimer below) provided
 * that the following conditions are met:
 *
 * o Redistributions of source code must retain the above copyright notice, this list
 *   of conditions and the following disclaimer.
 *
 * o Redistributions in binary form must reproduce the above copyright notice, this
 *   list of conditions and the following disclaimer in the documentation and/or
 *   other materials provided with the distribution.
 *
 * o Neither the name of the copyright holder nor the names of its
 *   contributors may be used to endorse or promote products derived from this
 *   software without specific prior written permission.
 *
 * NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE.
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
 * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef __USB_DEVICE_HID_GENERIC_H__
#define __USB_DEVICE_HID_GENERIC_H__

/*******************************************************************************
 * Definitions
 ******************************************************************************/

typedef struct _usb_device_hid_generic_struct
{
    uint32_t buffer[2][USB_HID_GENERIC_IN_BUFFER_LENGTH >> 2];
    uint8_t bufferIndex;
    uint8_t idleRate;
} usb_device_hid_generic_struct_t;

/*******************************************************************************
 * API
 ******************************************************************************/

extern usb_status_t USB_DeviceHidGenericInit(usb_device_composite_struct_t *deviceComposite);
extern usb_status_t USB_DeviceHidGenericCallback(class_handle_t handle, uint32_t event, void *param);
extern usb_status_t USB_DeviceHidGenericSetConfigure(class_handle_t handle, uint8_t configure);
extern usb_status_t USB_DeviceHidGenericSetInterface(class_handle_t handle,
                                                     uint8_t interface,
                                                     uint8_t alternateSetting);

#endif /* __USB_DEVICE_HID_GENERIC_H__ */