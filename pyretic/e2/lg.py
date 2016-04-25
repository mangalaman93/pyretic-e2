##########################################################
# Computer Networks course project, CS6250, Georgia Tech #
##########################################################

import commands

class LoadGenerator(object):
    """Generates artificial load for E2 hosts"""
    @staticmethod
    def src(destip, destport, tcp=True, num_request=0):
        nping = commands.getoutput("which nping")
        args = "--tcp"
        if not tcp:
            args = "--udp "
        if nping:
            return "{} {}--rate 1 -c {} -p {} {}".format(nping, args, num_request, destport, destip)
        else:
            raise Exception("nping not found!")

    @staticmethod
    def dest(port):
        ncat = commands.getoutput("which ncat")
        if ncat:
            return "{} -l {} --keep-open --exec \"/bin/cat\"".format(ncat, port)
        else:
            raise Exception("ncat not found!")
