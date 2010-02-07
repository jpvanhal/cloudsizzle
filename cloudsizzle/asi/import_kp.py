from asilib import ASIConnection
# This probably not a public interface, but we need to use it
# because we want to copy all users not synchronize a single user
from asibsync.sib_agent import to_rdf_instance
from cloudsizzle.kp import SIBConnection, Triple, bnode, uri, literal
from cloudsizzle import settings


# These are used to construct the URIs in RDF
RDF_BASE_URI = 'http://cos.alpha.sizl.org/people'
RDF_BASE_TYPE = 'Person'


def friends_to_rdf(user, friends):
    triples = []
    for friend in friends:
        triples.append(Triple(
            '{0}/ID#{1}'.format(RDF_BASE_URI, user['id']),
            '{0}#Friend'.format(RDF_BASE_URI),
            uri('{0}/ID#{1}'.format(RDF_BASE_URI, friend['id']))
        ))
    return triples


def import_asi():
    with SIBConnection('ASI to SIB dump', method='preconfigured') as sc:

        with ASIConnection(base_url=settings.ASI_BASE_URL,
            app_name=settings.ASI_APP_NAME,
            app_password=settings.ASI_APP_PASSWORD) as ac:

            print "Fetching users from ASI"
            users = ac.find_users()
            # This will choke on users that do not have an id
            # All users should probably have one, but we need to work
            # nevertheless.
            # Either need to convert the triplets one by one or patch
            # asibsync
            print "Converting ASI output to Triplets"
            for index, user in enumerate(users):
                print index, len(users), "\r"
                try:
                    triples = to_rdf_instance(
                        user, RDF_BASE_URI, RDF_BASE_TYPE, 'id')
                    friends = ac.get_friends(user['id'])
                    triples.extend(friends_to_rdf(user, friends))
                except KeyError:
                    print "Faulty userdata for ASI:"
                    print user
                else:
                    print "Inserting the following triples:"
                    print triples
                    sc.insert(triples)

if __name__ == '__main__':
    import_asi()
