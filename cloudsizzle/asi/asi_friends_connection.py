"""This module contains an extended ASIConnection class with methods related
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
