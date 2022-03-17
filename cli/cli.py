import click
from eaasi_uvi_client import EaaSIUVIClient


@click.command()
@click.option("--eaasi-url", required=True, help="EaaSI host URL.")
@click.option("--data-url", required=True, help="Data URL for content to characterize.")
@click.option(
    "--data-type",
    default="zip",
    help='Data type. Allowed values: "zip", "tar", "bagit+zip", "bagit+tar"',
    show_default=True
)
def get_recommendations(eaasi_url, data_url, data_type):
    """Get emulation environment suggestions from EaaSI API."""
    eaas_client = EaaSIUVIClient(
        base_url=eaasi_url, data_url=data_url, data_type=data_type
    )

    # Raises requests.ConnectionError or eaas_uvi_client.ResultNotFound on error.
    eaas_client.get_recommendations()
    eaas_client.parse_suggested_environments()


if __name__ == "__main__":
    get_recommendations()
