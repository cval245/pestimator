from enum import Enum


class TranslationRequirements(Enum):
    FULL_TRANSLATION = 'full translation',
    CLAIMS_TRANSLATION = 'claims translation',
    NO_TRANSLATION = 'no translation',


class ApplTypes(Enum):
    EP = 'ep'
    EP_VALIDATION = 'epvalidation'
    PCT = 'pct'
    PCT_NATIONAL_PHASE = 'nationalphase'
    UTILITY = 'utility'
    PROV = 'prov'
