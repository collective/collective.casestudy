from collective.casestudy import PACKAGE_NAME


class TestSetupInstall:
    def test_addon_installed(self, installer):
        assert installer.is_product_installed(PACKAGE_NAME) is True

    def test_browserlayer(self, browser_layers):
        """Test that ICaseStudyLayer is registered."""
        from collective.casestudy.interfaces import ICaseStudyLayer

        assert ICaseStudyLayer in browser_layers

    def test_latest_version(self, profile_last_version):
        """Test latest version of default profile."""
        assert profile_last_version(f"{PACKAGE_NAME}:default") == "2500"

    def test_no_dangling_upgrade_steps(self, installer):
        """Test that there are no dangling upgrade steps."""
        upgrade_info = installer.upgrade_info(PACKAGE_NAME)
        assert upgrade_info["available"] is False
