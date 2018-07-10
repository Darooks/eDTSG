class Message:
    def __init__(self):
        messageId                   = None
        eventLocation               = None
        lifetime                    = None
        eventTimeStamp              = None
        senderLocation              = None
        spreadAndAssuranceLifetime  = None
        updateSequence              = None
        _authenticEvent              = None  # My modification
        _nonAuthenticEvent           = None  # My modification

    def set_authentic_event(self):
        pass

    def set_non_authentic_event(self):
        pass
