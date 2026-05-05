from typing import Any

import ckan.plugins.toolkit as tk
from ckan import plugins


@tk.blanket.blueprints
@tk.blanket.config_declarations
@tk.blanket.helpers
class OrcidPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    # IConfigurer
    def update_config(self, config_: Any) -> None:
        tk.add_template_directory(config_, "templates")
        tk.add_resource("assets", "orcid")
