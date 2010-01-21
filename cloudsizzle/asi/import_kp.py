from asi import ASIConnection
# This probably not a public interface, but we need to use it
# because we want to copy all users not synchronize a single user
from asibsync.sib_agent import to_rdf_instance
from kpwrapper import SIBConnection, Triple, bnode, uri, literal
#from cloudsizzle import settings

def import_asi():
    # These are used to construct the URIs in RDF
    RDF_BASE_URI = 'http://cos.alpha.sizl.org/people'
    RDF_BASE_TYPE = 'Person'

    sc = SIBConnection('ASI to SIB dump', method='preconfigured')
    
    # Get ASI parameters from home directory, no wrapper doing this
    import os
    conf = {}
    execfile(os.getenv('HOME', '.') + '/.asirc', conf)
    if not ('asi_app_params' in conf):
        print('asi_app_params not defined.')
        sys.exit(1)
    ac = ASIConnection(**conf['asi_app_params'])
    ac.open()
    
    print "Fetching users from ASI"
    users = ac.find_users()
    # This will choke on users that do not have an id
    # All users should probably have one, but we need to work
    # nevertheless.
    # Either need to convert the triplets one by one or patch
    # asibsync
    print "Converting ASI output to Triplets"
    user_triplets = to_rdf_instance(users, RDF_BASE_URI, RDF_BASE_TYPE, 'id')
    
    # This alone is not enough, old triplets need to be removed first
    # Perhaps add a 'data owner' triplets identifying all subjects
    # that can be removed? Or just query for all triplets, find ones
    # containing RDF_BASE_URI and remove them
    print "Inserting Triplets to SIB"
    sc.insert(user_triplets)
