"""Moving industries and usages from free text to tokens.

Both fields used to store the label a site had typed into the registry, so
renaming a term orphaned every content item using it. Profile version 1100
stores a stable token instead; this upgrade rewrites the values already on
content and drops the now-meaningless labels from the registry.
"""

from collective.casestudy import logger
from plone import api
from Products.GenericSetup.tool import SetupTool


#: Old industry label to the token that replaces it.
INDUSTRIES: dict[str, str] = {
    "NGO": "ngo",
    "Education": "education",
    "Government": "gov",
    "Corporate": "corporate",
    "Media": "media",
}


#: Old usage label to the token that replaces it.
USAGES: dict[str, str] = {
    "Portal": "portal",
    "Intranet": "intranet",
    "Knowledge Base": "kb",
    "Other": "other",
}


def upgrade_case_study_vocabs(context: SetupTool) -> None:
    """Upgrade existing Case Study contents.

    A value that is not in the mapping is left alone: it is either already a
    token, or one this package never shipped.

    :param context: The setup tool running the upgrade step. Unused.
    """
    brains = api.content.find(portal_type="CaseStudy")
    logger.info(f"Found {len(brains)} Case Study items")
    for brain in brains:
        content = brain.getObject()
        logger.info(f"- Processing {content.absolute_url()}")
        # Usages
        current = content.usages
        values = [USAGES.get(value, value) for value in current]
        content.usages = values
        logger.info(f"-- Usages: from {', '.join(current)} to {', '.join(values)}")
        current = content.industry
        # Industry
        value = INDUSTRIES.get(current, current)
        content.industry = value
        logger.info(f"-- Industries: from {current} to {value}")
        content.reindexObject(idxs=["industry", "usages"])
        logger.info("-- Reindexed content")

    logger.info("Upgrade concluded")


def remove_old_values_from_registry(context: SetupTool) -> None:
    """Drop the superseded labels from the site registry.

    Only the labels this package shipped are removed; terms a site added
    itself stay.

    :param context: The setup tool running the upgrade step. Unused.
    """
    logger.info("Update vocabularies in site registry")
    for key_suffix, vocab in [("industries", INDUSTRIES), ("usages", USAGES)]:
        key = f"casestudy.{key_suffix}"
        to_remove = list(vocab)
        current = api.portal.get_registry_record(key)
        filtered = [item for item in current if item not in to_remove]
        api.portal.set_registry_record(key, filtered)
        logger.info(f"-- {key}: from {','.join(current)} to {','.join(filtered)}")
    logger.info("Upgrade concluded")
