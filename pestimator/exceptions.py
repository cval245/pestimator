class ApplTypeNotAvailableForCountry(BaseException):
    # applType not available for country
    pass


class ISACountryNotAvailableForCountry(BaseException):
    # isa country needs to be available for country
    pass


class ApplTypePCTNotSupportedException(BaseException):
    # applType pct not supported
    pass


class ApplTypePCTNationalPhaseNotSupportedException(BaseException):
    # applType pct national phase not supported
    pass
