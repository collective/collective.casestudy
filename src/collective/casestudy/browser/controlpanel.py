from collective.casestudy.interfaces import _
from collective.casestudy.interfaces import ICaseStudyLayer
from collective.casestudy.interfaces import ICaseStudySettings
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface


class SettingsEditForm(RegistryEditForm):

    schema = ICaseStudySettings
    schema_prefix = "casestudy"
    label = "Case Study Settings"


class SettingsControlPanelFormWrapper(ControlPanelFormWrapper):

    form = SettingsEditForm


@adapter(Interface, ICaseStudyLayer)
class SettingsConfigletPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = ICaseStudySettings
    configlet_id = "case_study"
    configlet_category_id = "Products"
    title = _("Case Study Settings")
    group = "Products"
    schema_prefix = "casestudy"
