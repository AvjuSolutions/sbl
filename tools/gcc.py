#
# File      : gcc.py
# This file is part of RT-Thread RTOS
# COPYRIGHT (C) 2006 - 2018, RT-Thread Development Team
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Change Logs:
# Date           Author       Notes
# 2018-05-22     Bernard      The first version

import os
import re
import platform

def GetGCCRoot(sblprofile):
    exec_path = sblprofile.EXEC_PATH
    prefix = sblprofile.PREFIX

    if prefix.endswith('-'):
        prefix = prefix[:-1]

    if exec_path == '/usr/bin':
        root_path = os.path.join('/usr/lib', prefix)
    else:
        root_path = os.path.join(exec_path, '..', prefix)

    return root_path

def CheckHeader(sblprofile, filename):
    root = GetGCCRoot(sblprofile)

    fn = os.path.join(root, 'include', filename)
    if os.path.isfile(fn):
        return True

    # Usually the cross compiling gcc toolchain has directory as:
    #
    # bin
    # lib
    # share
    # arm-none-eabi
    #    bin
    #    include
    #    lib
    #    share
    prefix = sblprofile.PREFIX
    if prefix.endswith('-'):
        prefix = prefix[:-1]

    fn = os.path.join(root, prefix, 'include', filename)
    if os.path.isfile(fn):
        return True

    return False

def GetNewLibVersion(sblprofile):
    version = 'unknown'
    root = GetGCCRoot(sblprofile)

    if CheckHeader(sblprofile, '_newlib_version.h'): # get version from _newlib_version.h file
        f = open(os.path.join(root, 'include', '_newlib_version.h'), 'r')
        if f:
            for line in f:
                if line.find('_NEWLIB_VERSION') != -1 and line.find('"') != -1:
                    version = re.search(r'\"([^"]+)\"', line).groups()[0]
            f.close()
    elif CheckHeader(sblprofile, 'newlib.h'): # get version from newlib.h
        f = open(os.path.join(root, 'include', 'newlib.h'), 'r')
        if f:
            for line in f:
                if line.find('_NEWLIB_VERSION') != -1 and line.find('"') != -1:
                    version = re.search(r'\"([^"]+)\"', line).groups()[0]
            f.close()
    return version

def GCCResult(sblprofile, str):
    import subprocess

    result = ''

    def checkAndGetResult(pattern, string):
        if re.search(pattern, string):
            return re.search(pattern, string).group(0)
        return None

    gcc_cmd = os.path.join(sblprofile.EXEC_PATH, sblprofile.CC)

    # use temp file to get more information
    f = open('__tmp.c', 'w')
    if f:
        f.write(str)
        f.close()

        # '-fdirectives-only',
        if(platform.system() == 'Windows'):
            child = subprocess.Popen([gcc_cmd, '-E', '-P', '__tmp.c'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        else:
            child = subprocess.Popen(gcc_cmd + ' -E -P __tmp.c', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        stdout, stderr = child.communicate()

        # print(stdout)
        if stderr != '':
            print(stderr)

        have_fdset = 0
        have_sigaction = 0
        have_sigevent = 0
        have_siginfo = 0
        have_sigval = 0
        version = None
        stdc = '1989'
        posix_thread = 0

        for line in stdout.split(b'\n'):
            line = line.decode()
            if re.search('fd_set', line):
                have_fdset = 1

            # check for sigal
            if re.search('struct[ \t]+sigaction', line):
                have_sigaction = 1
            if re.search('struct[ \t]+sigevent', line):
                have_sigevent = 1
            if re.search('siginfo_t', line):
                have_siginfo = 1
            if re.search('union[ \t]+sigval', line):
                have_sigval = 1

            if re.search('char\* version', line):
                version = re.search(r'\"([^"]+)\"', line).groups()[0]

            if re.findall('iso_c_visible = [\d]+', line):
                stdc = re.findall('[\d]+', line)[0]

            if re.findall('pthread_create', line):
                posix_thread = 1

        if have_fdset:
            result += '#define HAVE_FDSET 1\n'

        if have_sigaction:
            result += '#define HAVE_SIGACTION 1\n'
        if have_sigevent:
            result += '#define HAVE_SIGEVENT 1\n'
        if have_siginfo:
            result += '#define HAVE_SIGINFO 1\n'
        if have_sigval:
            result += '#define HAVE_SIGVAL 1\n'

        if version:
            result += '#define GCC_VERSION_STR "%s"\n' % version

        result += '#define STDC "%s"\n' % stdc

        if posix_thread:
            result += '#define LIBC_POSIX_THREADS 1\n'

        os.remove('__tmp.c')
    return result