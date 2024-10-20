"""A Python Pulumi program"""

import pulumi
import pulumi_digitalocean as digitalocean
from infrastructure.consts import REGION
from infrastructure.config import config

# Set provider
provider = digitalocean.Provider(
    "digitalocean-provider",
    spaces_access_id=config.SPACES_ACCESS_KEY_ID.get_secret_value(),
    spaces_secret_key=config.SPACES_SECRET_ACCESS_KEY.get_secret_value(),
    token=config.DIGITALOCEAN_TOKEN.get_secret_value(),
)

asic_li = digitalocean.Domain("asic-li", name="asic.li")
versioneer_dev = digitalocean.Domain("versioneer-dev", name="versioneer.dev")
praestes_io = digitalocean.Domain("praestes-io", name="praestes.io")
goforms_dev = digitalocean.Domain("goforms-dev", name="goforms.dev")

digitalocean.DnsRecord(
    "server",
    name="server",
    domain=asic_li.id,
    type="A",
    value=str(config.ASIC_SERVER_HETZNER_HOST),
)
digitalocean.DnsRecord(
    "hetzner",
    name="hetzner",
    domain=asic_li.id,
    type="A",
    value=str(config.ASIC_SERVER_HETZNER_HOST),
)
digitalocean.DnsRecord(
    "forms",
    name="forms",
    domain=asic_li.id,
    type="A",
    value=str(config.ASIC_SERVER_HETZNER_HOST),
)
digitalocean.DnsRecord(
    "goforms-dev",
    name="@",
    domain=goforms_dev.id,
    type="A",
    value=str(config.ASIC_SERVER_HETZNER_HOST),
)

# ===================================
# MX Google Suite
# ===================================

digitalocean.DnsRecord(
    "mx-1",
    name="@",
    domain=asic_li.id,
    type="MX",
    priority=1,
    value="ASPMX.L.GOOGLE.COM.",
)
digitalocean.DnsRecord(
    "mx-2",
    name="@",
    domain=asic_li.id,
    type="MX",
    priority=5,
    value="ALT1.ASPMX.L.GOOGLE.COM.",
)
digitalocean.DnsRecord(
    "mx-3",
    name="@",
    domain=asic_li.id,
    type="MX",
    priority=5,
    value="ALT2.ASPMX.L.GOOGLE.COM.",
)
digitalocean.DnsRecord(
    "mx-4",
    name="@",
    domain=asic_li.id,
    type="MX",
    priority=10,
    value="ALT3.ASPMX.L.GOOGLE.COM.",
)
digitalocean.DnsRecord(
    "mx-5",
    name="@",
    domain=asic_li.id,
    type="MX",
    priority=10,
    value="ALT4.ASPMX.L.GOOGLE.COM.",
)

# ===================================
# SPACES (s3 buckets / object stores)
# ===================================

digitalocean.SpacesBucket("data", region=REGION.FRA1.value, opts=pulumi.ResourceOptions(provider=provider))
digitalocean.SpacesBucket("quickwit", region=REGION.FRA1.value, opts=pulumi.ResourceOptions(provider=provider))

# Example with CORS
# digitalocean.SpacesBucket(
#     "TODO",
#     region=REGION.FRA1.value,
#     opts=pulumi.ResourceOptions(provider=provider),
#     cors_rules=[
#         digitalocean.SpacesBucketCorsRuleArgs(
#             allowed_headers=["*"],
#             allowed_methods=["GET", "POST", "PUT", "DELETE"],
#             allowed_origins=["*"],
#             max_age_seconds=0,
#         )
#     ],
# )
