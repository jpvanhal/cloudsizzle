# Copyright (c) 2009, Nokia Corp.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Nokia nor the names of its contributors may be
#       used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED THE COPYRIGHT HOLDERS AND CONTRIBUTORS ''AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import re
import kpwrapper
from kpwrapper import Triple as _Triple, wrap_if_not_none, SIBConnection, bnode, literal, uri, _any, get_class
from urllib import quote, unquote

__all__ = ['Triple', 'SIBConnection', 'bnode', 'literal', 'uri']

def escape(string):
    """Escape XML special characters with hexadecimal codes.
    
    For example:
    >>> escape('<a href="/somepage?a=1&b=2">Hello \\'world\\'!</a>')
    '%3Ca href=%22/somepage?a=1%26b=2%22%3EHello %27world%27!%3C/a%3E'

    Percent sign is also escaped:
    >>> escape('%')
    '%25'

    """
    string = string.replace('%', '%25')
    string = string.replace('<', '%3C')
    string = string.replace('>', '%3E')
    string = string.replace('&', '%26')
    string = string.replace('"', '%22')
    string = string.replace("'", '%27')
    return string

def unescape(string):
    """Unescape XML special characters escaped with hexadecimal codes.
    
    For example:
    >>> unescape('%3Ca href=%22/somepage?a=1%26b=2%22%3EHello %27world%27!%3C/a%3E')
    '<a href="/somepage?a=1&b=2">Hello \\'world\\'!</a>'
    
    Percent sign is also unescaped:
    >>> unescape('%25')
    '%'
                
    """
    string = string.replace('%25', '%')
    string = string.replace('%3C', '<')
    string = string.replace('%3E', '>')
    string = string.replace('%26', '&')
    string = string.replace('%22', '"')
    string = string.replace('%27', "'")
    return string

# The following code is pretty much copied from kpwrapper module. from_tuple and
# to_tuple methods are overriden in order to escape and unescape triple data.
class Triple(_Triple):
    @staticmethod
    def from_tuple(tuple):
        subject = tuple[0][0]
        predicate = tuple[0][1]
        object = tuple[0][2]
        if subject:
            subject = unquote(subject)
        if predicate:
            predicate = unquote(predicate)
        if object:
            object = unquote(object)
        s_type = get_class(tuple[1]) if len(tuple)==3 else str
        p_type = str
        o_type = get_class(tuple[2] if len(tuple)==3 else tuple[1])

        return Triple(wrap_if_not_none(s_type, subject),
                      wrap_if_not_none(p_type, predicate),
                      wrap_if_not_none(o_type, object))

    def to_tuple(self, default_stype = 'uri', default_otype = 'literal'):
        def get_typestr(obj, default=None):
            if isinstance(obj, type) and issubclass(obj, _any):
                return obj.__name__
            elif isinstance(obj, _any):
                return obj.__class__.__name__
            else:
                return default

        tuple = ((wrap_if_not_none(quote, wrap_if_not_none(str, self.subject)),
                  wrap_if_not_none(quote, wrap_if_not_none(str, self.predicate)),
                  wrap_if_not_none(quote, wrap_if_not_none(str, self.object))),)

        s_typestr = get_typestr(self.subject, default_stype)
        if s_typestr is not None:
            tuple += (s_typestr,)

        tuple += (get_typestr(self.object, default_otype),)
        return tuple

kpwrapper.Triple = Triple

