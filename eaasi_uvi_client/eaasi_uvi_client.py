import logging
import json
import sys
import time

import requests
from requests.adapters import HTTPAdapter, Retry

MODULE_NAME = "eaas_uvi_client" if __name__ == "__main__" else __name__
logger = logging.getLogger(MODULE_NAME)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class ResultNotFound(Exception):
    """Custom exception for when no result is returned."""


class EaaSIUVIClient:

    DATA_TYPES = ("zip", "tar", "bagit+zip", "bagit+tar")

    def __init__(self, base_url, data_url, data_type="zip"):
        self.base_url = base_url
        self.api_base_url = "{}/emil/environment-proposer/api/v2".format(
            base_url.rstrip("/")
        )
        self.data_url = data_url

        self.data_type = "zip"
        if data_type in self.DATA_TYPES:
            self.data_type = data_type

        self.results = {}

    def _submit_proposal(self):
        """Submit proposal to environment-proposer endpoint and return id."""
        url = "{}/proposals".format(self.api_base_url)
        response = requests.post(
            url, json={"data_url": self.data_url, "data_type": self.data_type},
        )
        if not response.status_code == 202:
            err_msg = "Error submitting environment proposer request to URL {}. Status code: {}".format(
                url, response.status_code
            )
            raise ResultNotFound(err_msg)

        response_dict = json.loads(response.content)
        return response_dict.get("id")

    def _poll_until_result_ready(self, proposal_id):
        """Poll waitqueue endpoint until results are ready and return location_url."""
        status_url = "{}/waitqueue/{}".format(self.api_base_url, proposal_id)

        # Configure requests.Session to retry on connectivity issues and 200
        # status code, which indicates results are not yet ready.
        session = requests.Session()
        retries = Retry(total=15, backoff_factor=1, status_forcelist=[200])
        session.mount("https://", HTTPAdapter(max_retries=retries))
        session.mount("http://", HTTPAdapter(max_retries=retries))

        response = session.get(status_url, allow_redirects=False)

        if response.status_code != 303:
            err_msg = "Error reported by {}. Status code: {}. Body: {}".format(
                status_url, response.status_code, response.content
            )
            raise ResultNotFound(err_msg)

        return response.headers.get("Location")

    def _fetch_result(self, location_url):
        """Fetch result from URL returned in location header and save as dict."""
        response = requests.get(location_url)
        if not response.status_code == 200:
            err_msg = "Error fetching result from UVI. Status code: {}. Body: {}".format(
                response.status_code, response.content
            )
            raise ResultNotFound(err_msg)
        self.results = json.loads(response.content)
        return self.results

    def get_recommendations(self):
        """Submit files to UVI API and return results when ready."""
        proposal_id = self._submit_proposal()
        logger.info("Proposal {} submitted.".format(proposal_id))

        time.sleep(3)

        location_url = self._poll_until_result_ready(proposal_id)

        logger.info("Fetching result from {}".format(location_url))
        self._fetch_result(location_url)

        logger.info("Result: {}".format(self.results))
        return self.results

    def parse_suggested_environments(self):
        """Parse results returned by UVI API."""
        if not self.results:
            raise ResultNotFound("Recommendations not yet fetched from UVI.")

        suggested_environments = self.results.get("result").get("suggested")
        if not suggested_environments:
            logger.warning("No suggested environments found.")
            return
        for suggestion in suggested_environments:
            logger.info("Suggestion: {}".format(suggestion))
        return suggested_environments
