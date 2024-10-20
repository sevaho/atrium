import pulumi
import pulumi_github as github
from infrastructure.config import config

provider = github.Provider(
    "github-provider",
    token=config.GITHUB_TOKEN.get_secret_value(),
)
