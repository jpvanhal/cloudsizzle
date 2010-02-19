# -*- coding: utf-8 -*-
#
# Copyright (c) 2009-2010 CloudSizzle Team
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""
This module contains an extended ASIConnection class with methods related
to managing friends.

"""
from asilib import ASIConnection, build_param_string

__author__ = 'bpang@cc.hut.fi'


class ASIFriendsConnection(ASIConnection):
    """ASIConnection extended with methods related to managing friends."""

    @property
    def user_id(self):
        """Return the user's user id, when logged in."""
        return self.session['entry']['user_id']


    def add_friend(self, friend_id):
        """Adds another user as friend of the user represented by this session.

        This method is also used for accepting a friend request.

        Arguments:
        friend_id -- The user id of the friend to connect to this user.

        """
        return self.do_request(
            ASIConnection.people_url + '/' + self.user_id + '/@friends',
            post_params=build_param_string(friend_id=friend_id), method='POST')


    def remove_friend(self, friend_id):
        """Break up with a friend of this user.

        Arguments:
        friend_id -- The user id of the friend to be broken up with.

        """
        return self.do_request(
            ASIConnection.people_url + '/' + self.user_id + '/@friends' +
            '/' + friend_id, method='DELETE')


    def get_pending_friend_requests(self):
        """Return the pending friend request of this user."""
        return self.do_request(
            ASIConnection.people_url + '/' + self.user_id +
            '/@pending_friend_requests', method='GET')


    def reject_friend_request(self, friend_id):
        """Reject a friend request made by another user.

        Arguments:
        friend_id -- The user id of the user whose friend request is rejected.

        """
        return self.do_request(
            ASIConnection.people_url + '/' + self.user_id +
            '/@pending_friend_requests' + '/' + friend_id, method='DELETE')
