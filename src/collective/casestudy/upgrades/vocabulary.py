from collective.casestudy import logger
from plone import api


INDUSTRIES = {
    "NGO": "ngo",
    "Education": "education",
    "Government": "gov",
    "Corporate": "corporate",
    "Media": "media",
}


USAGES = {
    "Portal": "portal",
    "Intranet": "intranet",
    "Knowledge Base": "kb",
    "Other": "other",
}


def upgrade_case_study_vocabs(context):
    """Upgrade existing Case Study contents."""
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


def remove_old_values_from_registry(context):
    logger.info("Update vocabularies in site registry")
    for key_suffix, vocab in [("industries", INDUSTRIES), ("usages", USAGES)]:
        key = f"casestudy.{key_suffix}"
        to_remove = [item for item in vocab]
        current = api.portal.get_registry_record(key)
        filtered = [item for item in current if item not in to_remove]
        api.portal.set_registry_record(key, filtered)
        logger.info(f"-- {key}: from {','.join(current)} to {','.join(filtered)}")
    logger.info("Upgrade concluded")
